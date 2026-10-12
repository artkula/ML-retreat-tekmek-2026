"""Privacy gate: a local model removes personal data before a cloud agent (Claude Code, Codex) sees the files.

    python privacy_gate.py clean  originals  clean          originals/ -> clean/, the key stays outside clean/
    python privacy_gate.py restore clean/feedback.md        puts the real names back into clean_restored/feedback.md

How it works:
1. Every text file in the input folder goes to a local model (by default the KTH GPU server, which answers only on
   the KTH network or the VPN). The model lists the personal data it finds and says whether the file must not
   leave KTH at all (for example health data about a named person).
2. The script replaces each item with a placeholder (PERSON_1, EMAIL_1, ...) and writes the result to the output
   folder. A file the model says must stay is not copied. Other file types (Word, PDF, images) are not copied either:
   save them as text first.
3. A pattern check (e-mail addresses, Swedish personal identity numbers, phone numbers) runs on every cleaned file.
   Anything it still finds is replaced too and named in the report.
4. The key (placeholder to real value) is written next to the output folder, never inside it: the cloud agent works
   in the output folder and never sees the key. restore uses the key to put the real values back into the result
   and writes it to a third folder (clean_restored), also outside the agent's folder.

Only the Python standard library is used. Options: --server http://localhost:11434 --model qwen3.5:9b for Ollama on
your own laptop. The model can miss things: read the report and look at the cleaned files before you start the agent.
"""
import argparse, json, os, re, shutil, sys, urllib.request

SERVER = "http://fred.hallf.kth.se:11435"
MODEL = "qwen3.8:27b"
TEXT = {".txt", ".md", ".csv", ".tsv", ".tex", ".json", ".py", ".m", ".html", ".xml", ".yaml", ".yml"}
CHUNK = 6000                                   # characters per request

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
        "text": {"type": "string"}, "type": {"type": "string"}}, "required": ["text", "type"]}},
    "withhold": {"type": "boolean"}, "reason": {"type": "string"}},
    "required": ["entities", "withhold", "reason"]}

PATTERNS = [                                   # the safety net after the model
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("PERSONNUMMER", re.compile(r"\b(?:19|20)?\d{6}[-+ ]?\d{4}\b")),
    ("PHONE", re.compile(r"(?:\+46|\b0)[\s-]?7\d(?:[\s-]?\d){7}\b")),
]


def ask(server, model, text):
    body = {"model": model, "stream": False, "think": False, "format": SCHEMA,
            "options": {"temperature": 0, "num_ctx": 16384},
            "messages": [{"role": "user", "content": PROMPT.format(text=text)}]}
    req = urllib.request.Request(server.rstrip("/") + "/api/chat", json.dumps(body).encode("utf-8"),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        reply = json.loads(r.read().decode("utf-8"))["message"]["content"]
    return json.loads(reply)


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
                if len(part) >= 3 and part[0].isupper() and part not in key["map"].values():
                    key["map"][ph + "abcdefgh"[i]] = part
    pairs = sorted(((v, ph) for ph, v in key["map"].items()), key=lambda p: -len(p[0]))
    for value, ph in pairs:
        text = re.sub(r"(?<!\w)" + re.escape(value) + r"(?!\w)", ph, text)
    return text


def clean(src, dst, server, model):
    if os.path.abspath(dst).startswith(os.path.abspath(src) + os.sep):
        sys.exit("The output folder must not lie inside the input folder.")
    keyfile = os.path.join(os.path.dirname(os.path.abspath(dst)), os.path.basename(os.path.abspath(dst)) + "_KEY.json")
    key = {"map": {}, "count": {}}
    if os.path.exists(keyfile):
        key = json.load(open(keyfile, encoding="utf-8"))
    os.makedirs(dst, exist_ok=True)
    report = ["# Privacy gate report", "", f"Model: {model} on {server}", ""]
    for root, _, files in os.walk(src):
        for name in sorted(files):
            path = os.path.join(root, name)
            rel = os.path.relpath(path, src)
            if os.path.splitext(name)[1].lower() not in TEXT:
                report.append(f"- {rel}: NOT COPIED (not a text file; save it as .txt or .md first)")
                print(f"skip   {rel}: not a text file")
                continue
            text = open(path, encoding="utf-8", errors="replace").read()
            found, withhold, reasons = [], False, []
            for i in range(0, len(text), CHUNK):
                try:
                    ans = ask(server, model, text[i:i + CHUNK])
                except OSError as e:
                    sys.exit(f"No answer from the local model at {server} ({e.__class__.__name__}). "
                             "Connect to the KTH network or the VPN, or use --server and --model for Ollama on this laptop.")
                found += [(e["text"].strip(), e["type"].strip().upper().replace(" ", "_"))
                          for e in ans.get("entities", []) if e.get("text", "").strip() and e["text"].strip() in text]
                if ans.get("withhold"):
                    withhold = True
                    reasons.append(ans.get("reason", ""))
            if withhold:
                report.append(f"- {rel}: NOT COPIED, must stay at KTH: {' '.join(reasons)}")
                print(f"STAY   {rel}: {' '.join(reasons)}")
                continue
            out = replace_all(text, key, found)
            net = [(m.group(0), kind) for kind, rx in PATTERNS for m in rx.finditer(out)]
            if net:
                out = replace_all(out, key, net)
            kinds = {}
            for _, k in found + net:
                kinds[k] = kinds.get(k, 0) + 1
            for ph, value in sorted(key["map"].items(), key=lambda p: -len(p[1])):   # names in file names, too
                if len(value) >= 3:
                    rel = re.sub(re.escape(value), ph, rel, flags=re.IGNORECASE)
            target = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8", newline="").write(out)
            summary = ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) or "nothing found"
            extra = f" (the pattern check found {len(net)} more)" if net else ""
            report.append(f"- {rel}: cleaned, {summary}{extra}")
            print(f"clean  {rel}: {summary}{extra}")
    json.dump(key, open(keyfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report += ["", "The key with the real values is outside this folder. Read the cleaned files before you start the agent."]
    open(os.path.join(dst, "_privacy_report.md"), "w", encoding="utf-8").write("\n".join(report) + "\n")
    print(f"\nCleaned files: {dst}\nReport: {os.path.join(dst, '_privacy_report.md')}\nKey (keep it local): {keyfile}")


def restore(target, keyfile):
    if not keyfile:
        folder = os.path.dirname(os.path.abspath(target if os.path.isdir(target) else os.path.dirname(target)))
        cands = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith("_KEY.json")]
        if len(cands) != 1:
            sys.exit("Give the key file with --key.")
        keyfile = cands[0]
    key = json.load(open(keyfile, encoding="utf-8"))
    cleandir = os.path.abspath(keyfile[:-len("_KEY.json")])
    if not os.path.abspath(target).startswith(cleandir):
        sys.exit(f"restore works only on files in {cleandir}")
    files = [target] if os.path.isfile(target) else [os.path.join(r, f) for r, _, fs in os.walk(target) for f in fs]
    for path in files:
        if os.path.splitext(path)[1].lower() not in TEXT or path.endswith("_privacy_report.md"):
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        new = text
        for ph in sorted(key["map"], key=len, reverse=True):
            new = re.sub(r"(?<!\w)" + re.escape(ph) + r"(?!\w)", key["map"][ph], new)
        if new != text:                        # outside the agent's folder, so the agent never reads real names
            outdir = keyfile[:-len("_KEY.json")] + "_restored"
            os.makedirs(outdir, exist_ok=True)
            out = os.path.join(outdir, os.path.basename(path))
            open(out, "w", encoding="utf-8", newline="").write(new)
            print(f"restored  {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("clean"); c.add_argument("src"); c.add_argument("dst")
    c.add_argument("--server", default=SERVER); c.add_argument("--model", default=MODEL)
    r = sub.add_parser("restore"); r.add_argument("target"); r.add_argument("--key")
    a = ap.parse_args()
    if a.cmd == "clean":
        if "cloud" in a.model.lower() or "ollama.com" in a.server.lower():
            sys.exit("A cloud model would send the originals out of KTH: use a local model.")
        clean(a.src, a.dst, a.server, a.model)
    else:
        restore(a.target, a.key)
