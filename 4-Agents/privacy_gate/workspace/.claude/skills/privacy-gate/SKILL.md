---
name: privacy-gate
description: Use when the user wants Claude to work on files that may hold personal data (student work, names, personal identity numbers, grades, e-mail addresses, health information) or says "privacy gate", "/privacy-gate", "clean the originals", "anonymise first". A local model on the KTH GPU server removes the personal data first; Claude works only on the cleaned copy and puts the real names back at the end, into a file it does not open. Skip for files the user says are public or synthetic.
allowed-tools: Bash(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean originals clean) Bash(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/*) PowerShell(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean originals clean) PowerShell(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/*) Write(clean/**) Edit(clean/**)
---

# Privacy gate

The user's files with personal data must not reach a cloud model. You are a cloud model. A local model reads them
instead, through the script `${CLAUDE_SKILL_DIR}/privacy_gate.py`.

The user's task, if given with the command: $ARGUMENTS

## The rules (they hold for the whole session)

- Never open, read, search, list the contents of, or copy the original files: not with Read, not with Grep or Glob
  on their contents, not with cat, type, Get-Content or a script. The same holds for the key file `*_KEY.json` and
  for the folder `*_restored`.
- Work only with the files in the cleaned folder.
- Keep the placeholders (PERSON_1, EMAIL_1, PERSONNUMMER_1, ...) exactly as written in everything you produce.
- If the gate fails, stop and tell the user. Never work around it by reading the originals.

## Steps

1. Find the originals. Default: the folder `originals` in the current folder. If the user names another folder, use
   that. If the files lie loose in the current folder, ask the user to put copies in a folder `originals`; do not
   look at them yourself.
2. Clean. Run the command exactly as written, as one command in the current folder: no `cd` before it, no `&&`,
   `;` or `||` around it, otherwise the user is asked to approve it:

   ```
   python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean originals clean
   ```

   It takes about 20 seconds per file on the KTH GPU server, which answers only on the KTH network or the VPN.
   If it says there is no answer from the server, tell the user to connect to the KTH network or VPN, and stop.
   If `python` is not found, tell the user to install Python 3 from python.org, and stop.
3. Read `clean/_privacy_report.md`. Tell the user in two or three lines which files were cleaned, which were held
   back (they stay at KTH and are not part of the task), and that they can look at the cleaned files in `clean`.
4. Do the user's task with the files in `clean/` only. Write every result into `clean/`.
5. Restore each result file, again as one command exactly as written:

   ```
   python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/<result file>
   ```

   Tell the user the file with the real names is in `clean_restored/` and that you have not opened it.

## What the script does (to explain if asked)

The local model lists names, e-mail addresses, personal identity numbers, student ids, phone numbers and similar,
and says whether a file must stay at KTH (for example health data about a named person). The script replaces each
item with a placeholder in the text and in the file names, runs a pattern check for e-mail addresses, personal
identity numbers and phone numbers, and keeps the key in `clean_KEY.json` next to `clean`, never inside it. Cloud
models are refused. Without the KTH network, Ollama on the laptop works:
`--server http://localhost:11434 --model qwen3.5:4b` after `clean originals clean`. It is a filter, not a guarantee;
the user owns the result.
