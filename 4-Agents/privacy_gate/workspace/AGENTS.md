# Privacy gate workspace

The folder `originals` holds files with personal data. They must not reach a cloud model, and that includes you.

- Never open, read, search, list the contents of or copy anything in `originals/`, the file `clean_KEY.json` or the
  folder `clean_restored/`. Not with Read, not with a shell command, not with a script.
- Step 1, before anything else: run `python privacy_gate.py clean originals clean` as one command, exactly as
  written. It sends the originals to the local model on the KTH GPU server, not to you.
- Step 2: read only `clean/_privacy_report.md`. Tell the user how many files were cleaned and how many held back,
  then stop and ask the user to look at the files in `clean` and confirm that they may be shared with you. Continue
  only after the user says yes.
- Step 3: do the user’s task with the files in `clean/` only (they have neutral names, FILE_0001.md, ...). Keep the
  placeholders (PERSON_1, EMAIL_1, ...) exactly as written. Write the results into `clean/` as .md or .txt files.
- Step 4: run `python privacy_gate.py restore clean/<result file>` for each result. Tell the user the file with the
  real names is in `clean_restored/`. Do not open it.
- If the gate fails (for example no answer from the KTH GPU server off the KTH network), or says `clean` already
  exists, stop and tell the user. Never work around it by reading the originals.
