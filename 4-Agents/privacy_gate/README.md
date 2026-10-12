# Privacy gate: a local model first, then Claude Code or Codex

For material that may not go to a cloud service as it is (student work, names, personal identity numbers): a local
model on the KTH GPU server removes the personal data, the cloud agent works on the cleaned copy, and the real names
are put back on your laptop at the end. Claude can run all of it for you; you only talk to Claude.

```
privacy_gate_workspace/
  originals/        your files; they go only to the local model, never to the cloud
  clean/            the copy with placeholders (PERSON_1, EMAIL_1); the agent works here
  clean_restored/   the result with the real names put back
  clean_KEY.json    which placeholder is which name; stays on your laptop
```

## Way A: Claude runs the gate for you (recommended)

1. Download [privacy_gate_workspace.zip](https://github.com/artkula/ML-retreat-tekmek-2026/raw/main/4-Agents/privacy_gate/privacy_gate_workspace.zip)
   and unzip it, for example to your Desktop. The folder `originals` holds a synthetic example (two lab reports, a
   rubric and a request with health data) to try first; afterwards replace these files with copies of your own.
2. Open a terminal in the folder `privacy_gate_workspace`:
   - Windows: open the folder in File Explorer, right-click an empty spot, Open in Terminal.
   - Mac: right-click the folder in Finder, Services, New Terminal at Folder.
3. Type `claude` (or `codex`). Answer the first question with Yes, I trust this folder: that switches on the rules
   of the folder.
4. Tell Claude what you want, for example:

   > Clean the originals with the privacy gate, then grade the lab reports against the rubric into feedback.md, then
   > restore the names.

   Claude runs the gate, reads only the cleaned copies, does the task, and puts the names back into
   `clean_restored/feedback.md`, which it does not open. Open that file yourself.

What keeps Claude away from the originals: `CLAUDE.md` in the folder tells it the rules (Codex reads the same rules
from `AGENTS.md`), and `.claude/settings.json` blocks Claude's file tools from `originals/`, the key and
`clean_restored/` and lets it run the two gate commands without asking. On Windows these rules are not a wall around
every possible command, so keep the default mode, read what Claude asks to run, and answer No to anything that
touches `originals`.

## Way B: run the gate yourself

In a terminal in the folder `privacy_gate_workspace`:

```
python privacy_gate.py clean originals clean
cd clean
claude
cd ..
python privacy_gate.py restore clean/feedback.md
```

Read `clean/_privacy_report.md` and look at the cleaned files before you start the agent.

## Notes

- Needs Python 3 (python.org; on a Mac it is there) and the KTH network or the VPN. Without them, with Ollama on
  your laptop: `python privacy_gate.py clean originals clean --server http://localhost:11434 --model qwen3.5:4b`.
  Cloud models are refused.
- Text files only (`.txt`, `.md`, `.csv`, `.tex`, ...): save Word or PDF as text first. Other files are not copied.
- The local model lists names, e-mail addresses, personal identity numbers, student ids and phone numbers; the
  script replaces them in the text and in the file names, and the same name gets the same placeholder in every file.
  A pattern check catches e-mail addresses, personal identity numbers and phone numbers the model missed. A file
  with health data or similar about a person is not copied at all.
- It is a filter, not a guarantee: a model can miss an unusual name or an indirect description. You own the result.

## Tested on 12 October 2026 (KTH network, qwen3.8:27b on the KTH GPU server, Claude Code 2.1.296)

- Way B: four files cleaned in 70 s; a search of `clean/` for every name, number and address found nothing; the
  request with health data was held back. Claude Code graded the cleaned reports 3 or 4, and 10 out of 10 (the error
  I = b h^3 / 3 found), Codex 4.5 and 10; restore put the names back.
- Way A: one sentence to Claude in the trusted workspace; in 38 s it ran the gate, read only `clean/`, wrote the
  feedback (4 and 10 out of 10) and restored the names. Its tool log shows no access to `originals/`. In a folder that
  was not trusted, Claude asked before running the gate and did not read the originals.
