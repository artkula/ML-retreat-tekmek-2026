# Privacy gate: a skill for Claude Code

A local model on the KTH GPU server removes names, e-mail addresses, personal identity numbers and similar from
your files; Claude works on the cleaned copy after you have looked at it; the real names go back into the result on
your laptop. You only talk to Claude.

For the retreat, use the synthetic example files. The gate replaces detected identifiers with reversible
placeholders. That is not anonymisation, and it does not by itself establish that real student, applicant,
confidential or internal material may be sent to a cloud service: you decide that under the KTH rules
([KTH recommendations for the use of AI](https://intra.kth.se/en/it/natverk/regler-policys/rekommendationer-vid-anvandning-av-ai-1.1446862)).

## 1. Install once

In a terminal (Windows PowerShell or the Mac Terminal), with Claude Code 2.1.292 or newer:

```
claude plugin install privacy-gate --marketplace artkula/ML-retreat-tekmek-2026
```

Inside a Claude session the same works as `/plugin install privacy-gate --marketplace artkula/ML-retreat-tekmek-2026`.
Start a new Claude session afterwards.

## 2. Use it

1. Make a new task folder and, inside it, a folder with copies of your files, for example `Applications`. Word
   (.docx), Excel (.xlsx), PDF with text, and text files work. Name the files without personal names, for example
   `report1.docx`: Claude can see file names in your folder, though not the contents.
2. Open a terminal in the task folder (Windows: right-click the folder in File Explorer, Open in Terminal; Mac:
   right-click, Services, New Terminal at Folder) and type `claude`.
3. Say what you want and mention the gate, for example:

   > Use the privacy gate on the folder Applications: rank the applicants by points and write a three-line summary
   > per applicant into summary.md. Then give me the names back.

4. Claude runs the gate and tells you how many files were cleaned and how many were held back. It then waits: open
   the folder `clean` yourself, look at the files, and answer yes if they may be shared.
5. Claude does the task on the cleaned copies and writes the result with the real names to
   `clean_restored/summary.md`, which it does not open. Open that file yourself.

```
your task folder/
  Applications/     your files (any folder name); only the local model reads them
  clean/            neutral file names (FILE_0001.md), placeholders (PERSON_1, EMAIL_1); Claude works here
  clean_KEY.json    which placeholder is which name and which FILE is which original; stays on your laptop
  clean_restored/   the result with the real names
```

Run the gate once per task folder. To run it again (new files, or after a failure), delete `clean`,
`clean_KEY.json` and `clean_restored`, or start a new task folder.

To try it first: [privacy_gate_workspace.zip](https://github.com/artkula/ML-retreat-tekmek-2026/raw/main/4-Agents/privacy_gate/privacy_gate_workspace.zip)
is a ready task folder with a synthetic example (two lab reports, a rubric, a request with health data, a Word
reference letter and an Excel list of applicants). It also works without the install: it carries the skill and
folder rules (`.claude/settings.json`).

## Good to know

- Needs Python 3.9 or newer and the KTH network or the VPN. If Python is missing, Claude offers to install it
  (Windows). Without the KTH network, Ollama on your laptop can do the cleaning with a local qwen3.5 model; ask
  Claude to add `--server http://localhost:11434 --model qwen3.5:4b`. Only these endpoints are accepted; on your
  own Ollama, switch cloud models off with `OLLAMA_NO_CLOUD=1`.
- What the gate finds: the local model lists names, e-mail addresses, personal identity numbers, student ids, phone
  numbers and similar; a pattern check then catches e-mail addresses, personal identity numbers and some Swedish
  mobile-number formats that the model missed. A file with health data or similar about a person is not copied at
  all. Grades, affiliations and the story in a text remain. A model can miss an unusual name, a lower-case name or
  an indirect description: look at `clean` before you say yes.
- File formats: Word and Excel become plain text; headers, footers and comments of Word files are included, text
  boxes may not be. Legacy .doc and .xls, images and scanned PDFs are not copied (scans need text recognition
  first). Results to be restored must be .md or .txt.
- What keeps Claude out of your files: the skill instructs Claude to work in `clean` only and allows it to run the
  two gate commands and to write into `clean` without asking. It does not lock the other files away; anything else
  Claude wants to run, it asks first, so answer No to anything that touches your original folder. For real
  confidential files, run the gate and the restore yourself, outside the Claude session, and give Claude only
  `clean`.
- By hand, from the task folder: `python privacy_gate.py clean originals clean`, look at `clean`, work there, then
  `python privacy_gate.py restore clean/summary.md` (the script is in this folder).

## Tested on 12 October 2026 (KTH network, qwen3.8:27b on the KTH GPU server, Claude Code 2.1.296)

- Install: the one line above, from GitHub, on a computer where it was not installed.
- Script: eight synthetic files (two lab reports, a rubric, a request with health data, a Word letter, an Excel
  list, a copy of a report named after its author, an empty file) in 26 s; neutral file names; a search of `clean`
  for every name, address and number found nothing; the request with health data was held back. Refused as
  intended: a second run into an existing `clean`, the same folder as input and output, a missing input folder, an
  unapproved server, a restore of a file outside `clean`, and a key from another place.
- Skill, with Claude: see the results of the final check in the retreat notes.
