"""Privacy gate: a local model removes personal data before a cloud agent (Claude Code, Codex) sees the files.

Run it from the task folder:

    python privacy_gate.py clean originals clean        originals/ -> clean/; the key goes to clean_KEY.json
    python privacy_gate.py restore clean/summary.md     the real names go back, into clean_restored/summary.md

How it works:
1. Every file in the input folder goes to a local model (by default the KTH GPU server, which answers only on the
   KTH network or the VPN). The model lists the personal data it finds and says whether the file must stay at KTH
   altogether (for example health data about a named person).
2. Each item is replaced by a placeholder (PERSON_1, EMAIL_1, ...). The cleaned files get neutral names
   (FILE_0001.md, ...), so that names in file names do not travel either. Text, Word (.docx) and Excel (.xlsx) are
   read directly, PDF with text through pypdf; the cleaned copy is plain text (.md). Legacy .doc/.xls, images and
   scans are not copied. A file the model says must stay is not copied.
3. A pattern check (e-mail addresses, Swedish personal identity numbers, some Swedish mobile-number formats) runs on
   every cleaned file and replaces what the model missed.
4. The key (placeholder to real value, neutral file name to original file name) is clean_KEY.json next to clean/,
   not inside it. restore puts the real values back into a result and writes it to clean_restored/.

It is a filter, not a guarantee, and reversible placeholders are not anonymisation: grades, affiliations and the
story in a text remain. Look at clean/ before you share it. Only approved local endpoints are used: the KTH GPU
server, or Ollama on this laptop (--server http://localhost:11434 --model qwen3.5:4b). Python 3.9 or later, standard
library only (pypdf for PDF).
"""
import argparse, json, os, re, sys, urllib.request
from pathlib import Path

SERVER = "http://fred.hallf.kth.se:11435"
MODEL = "qwen3.8:27b"
LOCAL = ("http://localhost:11434", "http://127.0.0.1:11434")
LOCAL_MODELS = {"qwen3.5:2b", "qwen3.5:4b", "qwen3.5:9b", "qwen3.5:27b"}
TEXT = {".txt", ".md", ".csv", ".tsv", ".tex", ".json", ".py", ".m", ".html", ".xml", ".yaml", ".yml"}
KINDS = {"PERSON", "EMAIL", "PHONE", "PERSONNUMMER", "STUDENT_ID", "ADDRESS", "OTHER_ID"}
CHUNK, OVERLAP = 6000, 300                     # characters per request; chunks overlap so a name is not cut

PROMPT = """You check a document before it may be sent to a cloud AI service, under university data rules.

List every piece of personal data in the text, exactly as it is written there (same spelling and case):
- PERSON: names of people (full names, and first or last names on their own)
- EMAIL, PHONE, PERSONNUMMER (Swedish personal identity number), STUDENT_ID, ADDRESS
- OTHER_ID: any other number or code that points to one person (employee number, KTH user name, ...)
Do not list course codes, public institutions, authors of published works, or generic words.

Then decide "withhold": true only if the text holds sensitive data that placeholders would not make safe, such as
health, ethnic origin, religion, political views, sexual orientation, criminal records, or details that identify a
person even without the name. Names, e-mail addresses, personal identity numbers and other identifiers are NOT a
reason to withhold: list them, they are replaced by placeholders. Give a one-sentence reason without quoting
personal data.

TEXT:
<<<
{text}
>>>"""

SCHEMA = {"type": "object", "properties": {
    "entities": {"type": "array", "items": {"type": "object", "properties": {
        "text": {"type": "string"}, "type": {"type": "string", "enum": sorted(KINDS)}},
        "required": ["text", "type"]}},
    "withhold": {"type": "boolean"}, "reason": {"type": "string"}},
    "required": ["entities", "withhold", "reason"]}

PATTERNS = [                                   # the safety net after the model
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("PERSONNUMMER", re.compile(r"\b(?:19|20)?\d{6}[-+ ]?\d{4}\b")),
    ("PHONE", re.compile(r"(?:\+46|\b0)[\s-]?7\d(?:[\s-]?\d){7}\b")),
]


def approved(server, model):
    server = server.rstrip("/")
    if server == SERVER:
        return model == MODEL
    return server in LOCAL and model in LOCAL_MODELS


def read_document(path):
    """(text, None) for a file that can be read, (None, reason) for one that cannot."""
    import zipfile, xml.etree.ElementTree as ET
    ext = path.suffix.lower()
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    try:
        if ext in TEXT:
            return path.read_text(encoding="utf-8", errors="replace"), None
        if ext == ".docx":
            with zipfile.ZipFile(path) as z:
                parts = [n for n in z.namelist() if re.fullmatch(r"word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml", n)]
                paras = []
                for n in sorted(parts, key=lambda n: n != "word/document.xml"):
                    for p in ET.fromstring(z.read(n)).iter(W + "p"):
                        paras.append("".join(t.text or "" for t in p.iter(W + "t")))
            return "\n".join(paras), None
        if ext == ".xlsx":
            with zipfile.ZipFile(path) as z:
                shared = []
                if "xl/sharedStrings.xml" in z.namelist():
                    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
                        shared.append("".join(t.text or "" for t in si.iter(S + "t")))
                lines = []
                for name in sorted(n for n in z.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)):
                    lines.append(f"## {Path(name).stem}")
                    for row in ET.fromstring(z.read(name)).iter(S + "row"):
                        cells = {}
                        for c in row.iter(S + "c"):
                            col = re.match(r"[A-Z]+", c.get("r", "")) and re.match(r"[A-Z]+", c.get("r")).group(0)
                            idx = 0
                            for ch in (col or ""):
                                idx = idx * 26 + ord(ch) - 64
                            idx = idx - 1 if col else len(cells)
                            v = c.find(S + "v")
                            val = "" if v is None else (v.text or "")
                            if c.get("t") == "s" and val.isdigit():
                                val = shared[int(val)]
                            elif c.get("t") == "inlineStr":
                                val = "".join(t.text or "" for t in c.iter(S + "t"))
                            cells[idx] = val
                        if cells:
                            lines.append("\t".join(cells.get(i, "") for i in range(max(cells) + 1)))
            return "\n".join(lines), None
        if ext == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                return None, "PDF reader missing (python -m pip install pypdf)"
            text = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(path)).pages)
            if not text.strip():
                return None, "PDF without text (a scan)"
            return text, None
    except Exception:
        return None, "could not be read"
    return None, "file type not supported"


def ask(server, model, text):
    if not approved(server, model):
        raise ValueError("endpoint or model not approved")
    body = {"model": model, "stream": False, "think": False, "format": SCHEMA,
            "options": {"temperature": 0, "num_ctx": 16384},
            "messages": [{"role": "user", "content": PROMPT.format(text=text)}]}
    req = urllib.request.Request(server.rstrip("/") + "/api/chat", json.dumps(body).encode("utf-8"),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        reply = json.loads(r.read().decode("utf-8"))["message"]["content"]
    ans = json.loads(reply)                    # check the reply strictly: a bad reply stops the gate
    if (not isinstance(ans, dict) or type(ans.get("withhold")) is not bool
            or not isinstance(ans.get("entities"), list) or not isinstance(ans.get("reason"), str)):
        raise ValueError("invalid reply")
    for e in ans["entities"]:
        if (not isinstance(e, dict) or not isinstance(e.get("text"), str) or not e["text"].strip()
                or e.get("type") not in KINDS):
            raise ValueError("invalid entity")
    return ans


def placeholder(key, kind, value):
    """The same value always gets the same placeholder, in every file."""
    for ph, v in key["map"].items():
        if v == value:
            return ph
    key["count"][kind] = key["count"].get(kind, 0) + 1
    ph = f"{kind}_{key['count'][kind]}"
    key["map"][ph] = value
    return ph


def replace_all(text, key, items):
    for value, kind in items:
        ph = placeholder(key, kind, value)
        if kind == "PERSON":                   # a full name also covers its parts: "Anna" alone, "Lindqvist" alone
            for i, part in enumerate(value.split()[:8]):
                if len(part) >= 2 and part[0].isupper() and part not in key["map"].values():
                    key["map"][ph + "abcdefgh"[i]] = part
    names = {v: ph for ph, v in key["map"].items() if not ph.startswith("FILE_")}
    if names:
        rx = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(v) for v in sorted(names, key=len, reverse=True)) + r")(?!\w)")
        text = rx.sub(lambda m: names[m.group(0)], text)
    return text


def clean(src, dst, server, model):
    source, dest = Path(src).resolve(), Path(dst).resolve()
    if not source.is_dir():
        sys.exit(f"Input must be an existing folder: {src}")
    if source == dest or source in dest.parents or dest in source.parents:
        sys.exit("Input and output folders must be separate.")
    keyfile = dest.with_name(dest.name + "_KEY.json")
    restored = dest.with_name(dest.name + "_restored")
    if os.path.lexists(dest) or os.path.lexists(keyfile) or os.path.lexists(restored):
        sys.exit(f"{dest.name}, {keyfile.name} or {restored.name} already exist. Delete them, or use a new task folder.")
    key = {"map": {}, "count": {}, "files": {}}
    dest.mkdir(parents=True)
    report = ["# Privacy gate report", "", f"Model: {model} on {server}", ""]
    files = sorted(p for p in source.rglob("*") if p.is_file())
    for n, path in enumerate(files, 1):
        if not path.resolve().is_relative_to(source):
            sys.exit("A link in the input folder points outside it. Copy the files in instead.")
        doc = f"FILE_{n:04d}"
        key["files"][doc] = str(path.relative_to(source))
        text, why = read_document(path)
        if text is None:
            report.append(f"- {doc}: NOT COPIED ({why}); review it locally")
            print(f"skip   {doc}: {why}")
            continue
        found, withhold = [], False
        starts = range(0, max(len(text), 1), CHUNK - OVERLAP)
        for i in starts:
            try:
                ans = ask(server, model, text[i:i + CHUNK])
            except (OSError, ValueError, TypeError, KeyError) as e:
                for p in dest.rglob("*"):      # no half-cleaned output is left behind
                    p.unlink() if p.is_file() else None
                sys.exit(f"Gate failed ({e.__class__.__name__}): nothing was cleaned. Check the KTH network or VPN, "
                         "then delete clean and run again.")
            found += [(e["text"].strip(), e["type"]) for e in ans["entities"] if e["text"].strip() in text]
            withhold = withhold or ans["withhold"]
        if withhold:
            report.append(f"- {doc}: NOT COPIED, sensitive content; it stays at KTH, review it locally")
            print(f"STAY   {doc}: sensitive content")
            continue
        out = replace_all(text, key, found)
        net = [(m.group(0), kind) for kind, rx in PATTERNS for m in rx.finditer(out)]
        if net:
            out = replace_all(out, key, net)
        kinds = {}
        for _, k in found + net:
            kinds[k] = kinds.get(k, 0) + 1
        (dest / f"{doc}.md").write_text(out, encoding="utf-8", newline="")
        summary = ", ".join(f"{c} {k}" for k, c in sorted(kinds.items())) or "nothing found"
        extra = f" (the pattern check found {len(net)} more)" if net else ""
        report.append(f"- {doc}.md: cleaned, {summary}{extra}")
        print(f"clean  {doc}.md: {summary}{extra}")
    keyfile.write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    report += ["", "Which FILE number is which original is in the key next to this folder. Look at the cleaned files "
               "before you share them."]
    (dest / "_privacy_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"\nGate complete: {len(files)} files. Report: {dest.name}/_privacy_report.md. Look at {dest.name}/ before you share it.")


def restore(target, keyfile=None):
    base = Path.cwd().resolve()
    cleanroot, expected, outroot = base / "clean", base / "clean_KEY.json", base / "clean_restored"
    if keyfile and Path(keyfile).resolve() != expected:
        sys.exit("Run restore from the task folder, with the key clean_KEY.json there.")
    for p in (cleanroot, expected, outroot):
        if os.path.lexists(p) and p.resolve() != p:
            sys.exit("Unsafe restore path (a link).")
    target = Path(target).resolve()
    if not target.exists() or not target.is_relative_to(cleanroot):
        sys.exit("Restore works only on files in clean/, run from the task folder.")
    mapping = json.loads(expected.read_text(encoding="utf-8"))["map"]
    rx = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(p) for p in sorted(mapping, key=len, reverse=True)) + r")(?!\w)") if mapping else None
    files = [target] if target.is_file() else sorted(target.rglob("*"))
    for item in files:
        path = item.resolve()
        if not path.is_relative_to(cleanroot):
            sys.exit("Unsafe restore input.")
        if not path.is_file() or path.suffix.lower() not in TEXT or path.name == "_privacy_report.md":
            continue
        out = outroot / path.relative_to(cleanroot)
        if os.path.lexists(out):
            sys.exit(f"{out.relative_to(base)} already exists; delete it first.")
        text = path.read_text(encoding="utf-8")
        if rx:
            text = rx.sub(lambda m: mapping[m.group(0)], text)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("x", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"Result written to clean_restored/{out.relative_to(outroot).as_posix()}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("clean"); c.add_argument("src"); c.add_argument("dst")
    c.add_argument("--server", default=SERVER); c.add_argument("--model", default=MODEL)
    r = sub.add_parser("restore"); r.add_argument("target"); r.add_argument("--key")
    a = ap.parse_args()
    if a.cmd == "clean":
        if not approved(a.server, a.model):
            sys.exit("Only the KTH GPU server or Ollama on this laptop with a local qwen3.5 model is accepted.")
        clean(a.src, a.dst, a.server, a.model)
    else:
        restore(a.target, a.key)
