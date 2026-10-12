# Privacy gate: a local model first, then Claude Code or Codex

For material that may not go to a cloud service as it is (student work, names, personal identity numbers): a local
model removes the personal data, the cloud agent works on the cleaned copy, and the real names are put back on your
laptop at the end.

```
originals/        your files (never leave the laptop)
   |  1. python privacy_gate.py clean originals clean     (local model: KTH GPU server or Ollama)
   v
clean/            placeholders instead of names; _privacy_report.md says what was removed or held back
   |  2. cd clean, then claude  (or codex)                 (the cloud agent sees only this folder)
   v
clean/feedback.md
   |  3. python privacy_gate.py restore clean/feedback.md
   v
clean_restored/feedback.md   with the real names; clean_KEY.json holds the key, both outside clean/
```

## Get it

In a terminal, in the folder where you will work (Windows PowerShell and macOS alike):

```
curl -O https://raw.githubusercontent.com/artkula/ML-retreat-tekmek-2026/main/4-Agents/privacy_gate/privacy_gate.py
```

On Windows PowerShell write `curl.exe` instead of `curl`. The synthetic example files are in `sample/originals`
(Code, Download ZIP on the repository page gives everything). All names and numbers in them are made up.

## Steps

1. Put copies of the files in a folder `originals`. Text files only (`.txt`, `.md`, `.csv`, `.tex`, ...): save Word
   or PDF as text first. Other files are not copied.
2. On the KTH network or the VPN:

   ```
   python privacy_gate.py clean originals clean
   ```

   Without the KTH network, with Ollama on your laptop: add `--server http://localhost:11434 --model qwen3.5:4b`.
   Cloud models are refused.
3. Read `clean/_privacy_report.md` and open the cleaned files. A file the model judged must stay at KTH (for example
   health data about a named person) is not copied; deal with it by hand.
4. Work in `clean` with the agent as usual: `cd clean`, then `claude` or `codex`. Ask it to keep the placeholders
   (PERSON_1, EMAIL_1) exactly as written.
5. Put the names back: `python privacy_gate.py restore clean/feedback.md`. The result is in `clean_restored`.

Needs Python 3 (python.org; on a Mac it is there). Only the standard library is used.

## What it does and does not do

- The local model lists names, e-mail addresses, personal identity numbers, student ids, phone numbers and similar,
  and says whether a file must stay at KTH. The script replaces every item by a placeholder, in the text and in the
  file names, and the same name gets the same placeholder in every file.
- A pattern check (e-mail, personal identity number, Swedish mobile number) runs after the model and catches what it
  missed.
- It is a filter, not a guarantee: a model can miss an unusual name or an indirect description. Read the cleaned
  files before step 4. You own the result.

## Tested on 12 October 2026 (KTH network, qwen3.8:27b on the KTH GPU server)

With the synthetic files in `sample/originals` (two lab reports with names, e-mail, personal identity number,
student id and phone number; a rubric; a request for an extension that mentions a hospital stay):

- clean, 70 s for four files: both reports cleaned, the rubric unchanged, the extension request held back
  (health data). A search of `clean/` for every name, number and address found nothing.
- Claude Code (`claude -p`, Sonnet) graded the two cleaned reports against the rubric in 20 s: 3 and 10 out of 10,
  with the error in the report of 3 points (I = b h^3 / 3) found. Codex (`codex exec`) did the same: 4.5 and 10.
- restore put the real names into the feedback in `clean_restored/`.
