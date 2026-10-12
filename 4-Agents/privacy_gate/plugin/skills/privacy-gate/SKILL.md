---
name: privacy-gate
description: Use when the user wants Claude to work on files that may hold personal data (student work, names, personal identity numbers, grades, e-mail addresses, health information) or mentions the privacy gate. A local model on the KTH GPU server removes the personal data first; Claude works only on the cleaned copy, after the user has looked at it, and the real names go back at the end into a file Claude does not open. Skip public files, and synthetic files unless the user asks for the privacy gate.
allowed-tools: Bash(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean * clean) Bash(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/*) PowerShell(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean * clean) PowerShell(python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/*) Edit(clean/**)
---

# Privacy gate

The user’s files with personal data must not reach a cloud model. You are a cloud model. A local model reads them
instead, through the script `${CLAUDE_SKILL_DIR}/privacy_gate.py`.

The user’s task, if given with the command: $ARGUMENTS

## The rules (they hold for the whole session)

- Never open, read, search, list the contents of, or copy the user’s original files: not with Read, not with Grep
  or Glob, not with cat, type, Get-Content or a script. The same holds for `clean_KEY.json` and `clean_restored/`.
- Work only with the files in `clean/`. Keep the placeholders (PERSON_1, EMAIL_1, PERSONNUMMER_1, ...) exactly as
  written in everything you produce.
- If the gate fails, stop and tell the user. Never work around it by reading the originals.

## Steps

1. Find the folder with the user’s files. Default: a folder `originals` in the current folder. If there is none,
   ask the user which folder holds the files and use its name; do not look inside it. Word (.docx), Excel (.xlsx),
   PDF with text, and text files are supported. If the files lie loose in the current folder, ask the user to move
   them into a folder of their own first.
2. Clean. Run the command exactly as written, as one command in the current folder: no `cd` before it, no `&&`,
   `;` or `||` around it, otherwise the user is asked to approve it. Replace `originals` with the folder name if it
   is another one; the output folder is always `clean`:

   ```
   python "${CLAUDE_SKILL_DIR}/privacy_gate.py" clean originals clean
   ```

   It takes 5 to 20 seconds per file on the KTH GPU server, which answers only on the KTH network or the VPN.
   - It says `clean` already exists: tell the user to delete `clean`, `clean_KEY.json` and `clean_restored`, or to
     use a new task folder. Then stop.
   - Gate failed (no answer from the server): tell the user to connect to the KTH network or VPN, and stop.
   - `python` not found: offer to install it. On Windows, with the user’s yes, run
     `winget install --id Python.Python.3.12 -e`, then ask the user to close and reopen the terminal and start
     Claude again. On a Mac, tell the user to install Python 3 from python.org. Then stop.
   - A PDF reported as needing pypdf: with the user’s yes, run `python -m pip install pypdf`; then the user deletes
     `clean` and `clean_KEY.json` and you clean again.
3. Read `clean/_privacy_report.md` (nothing else yet). Tell the user in two or three lines how many files were
   cleaned and how many were held back (those stay at KTH). The cleaned files have neutral names (FILE_0001.md, ...).
   Then stop and ask the user to look at the files in `clean` on their own computer and confirm that they may be
   shared with you. Continue only after the user says yes.
4. Do the user’s task with the files in `clean/` only. Write every result into `clean/` as a .md or .txt file.
5. Restore each result file, again as one command exactly as written:

   ```
   python "${CLAUDE_SKILL_DIR}/privacy_gate.py" restore clean/<result file>
   ```

   Tell the user the file with the real names is in `clean_restored/` and that you have not opened it.

## What to say if asked

The local model lists names, e-mail addresses, personal identity numbers, student ids, phone numbers and similar,
and says whether a file must stay at KTH (for example health data about a named person). The script replaces each
item with a placeholder, gives the cleaned files neutral names, runs a pattern check for e-mail addresses, personal
identity numbers and some Swedish mobile-number formats, and keeps the key in `clean_KEY.json` next to `clean`.
Only the KTH GPU server or Ollama on the laptop with a local qwen3.5 model is accepted. Placeholders are reversible,
and grades, affiliations and the story in a text remain, so this is a filter, not anonymisation and not a
guarantee: the user decides what may be shared, under the KTH rules, and owns the result. The skill instructs
Claude; it does not lock other files away.
