# Privacy gate: a skill for Claude Code

For material that may not go to a cloud service as it is (student work, names, personal identity numbers): a local
model on the KTH GPU server removes the personal data, Claude works on the cleaned copy, and the real names are put
back on your laptop at the end. You only talk to Claude.

## 1. Install once

In a terminal (Windows PowerShell or the Mac Terminal):

```
claude plugin install privacy-gate --marketplace artkula/ML-retreat-tekmek-2026
```

Inside a Claude session the same works as `/plugin install privacy-gate --marketplace artkula/ML-retreat-tekmek-2026`.
Start a new Claude session afterwards.

## 2. Use it

1. Make a folder for the task and, inside it, a folder with copies of your files (Word, Excel, PDF or text), for
   example `Applications`. Name the files without personal names, for example `report1.docx`: Claude can see file
   names, though not the contents.
2. Open a terminal in the task folder (Windows: right-click the folder in File Explorer, Open in Terminal; Mac:
   right-click, Services, New Terminal at Folder) and type `claude`.
3. Say what you want and mention the gate, for example:

   > Use the privacy gate on the folder Applications: rank the applicants by points and write a three-line summary
   > per applicant into summary.md. Then give me the names back.

   or, for teaching:

   > Use the privacy gate: grade the lab reports against the rubric into feedback.md, then give me the names back.

Claude runs the gate (the originals go only to the KTH GPU server), tells you what was cleaned and what was held back,
does the task on the cleaned copies in `clean/`, and writes the result with the real names to
`clean_restored/feedback.md`, which it does not open. Open that file yourself.

```
your task folder/
  Applications/     your files (any folder name); only the local model reads them
  clean/            the copy with placeholders (PERSON_1, EMAIL_1); Claude works here
  clean_restored/   the result with the real names
  clean_KEY.json    which placeholder is which name; stays on your laptop
```

To try it first: [privacy_gate_workspace.zip](https://github.com/artkula/ML-retreat-tekmek-2026/raw/main/4-Agents/privacy_gate/privacy_gate_workspace.zip)
is a ready task folder with a synthetic example (two lab reports, a rubric, a request with health data, a Word
reference letter and an Excel list of applicants). It also
works without the install: it carries the skill and stricter folder rules (`.claude/settings.json`).

## Good to know

- Needs Python 3 and the KTH network or the VPN. If Python is missing, Claude offers to install it (Windows). Without them, Ollama on your
  laptop can do the cleaning: ask Claude to use `--server http://localhost:11434 --model qwen3.5:4b`.
- The skill tells Claude never to open the originals, the key or `clean_restored`, and it may run only the two gate
  commands and write into `clean/` without asking. Anything else it wants to run, it asks first: answer No to
  anything that touches `originals`. On Windows the rules are instructions and permission checks, not a wall.
- The local model lists names, e-mail addresses, personal identity numbers, student ids and phone numbers; the
  script replaces them in the text and in the file names, and a pattern check catches e-mail addresses, personal
  identity numbers and phone numbers the model missed. A file with health data or similar about a person is not
  copied at all. It is a filter, not a guarantee: look at `clean/` if in doubt. You own the result.
- Without Claude: `python privacy_gate.py clean originals clean`, work in `clean`, then
  `python privacy_gate.py restore clean/feedback.md` (the script is in this folder).

## Tested on 12 October 2026 (KTH network, qwen3.8:27b on the KTH GPU server, Claude Code 2.1.296)

- Install: the one line above, from GitHub, on a computer where it was not installed.
- Skill, in a folder with only `originals`: one sentence; Claude ran the gate, read only `clean/`, graded the reports
  4 and 10 out of 10 (the error I = b h^3 / 3 found), restored the names, and asked nothing. No name, address or
  number from the originals appears anywhere in its transcript. The request with health data was held back.
- Admin example, folder `Applications` with an Excel list of three applicants and a Word reference letter: one
  sentence; 34 s; Claude ranked the applicants, used the letter, restored the names; no question asked, and no name,
  address or number in its transcript.
- In the ready folder from the zip, asked directly to show an original, Claude refused.
- The script alone: four files in 70 s; Codex graded the cleaned copies too (4.5 and 10).
