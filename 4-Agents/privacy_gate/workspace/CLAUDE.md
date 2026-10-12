# Privacy gate workspace

The folder `originals` holds files with personal data. They must not reach a cloud model, and that includes you.

- Never open, read, search, list the contents of or copy anything in `originals/`, the file `clean_KEY.json` or the
  folder `clean_restored/`. Not with Read, not with a shell command, not with a script.
- Step 1, before anything else: run `python privacy_gate.py clean originals clean`. It sends the originals to the
  local model on the KTH GPU server, not to you. Then read `clean/_privacy_report.md` and tell the user which files
  were cleaned and which were held back.
- Step 2: do the user's task with the files in `clean/` only. Keep the placeholders (PERSON_1, EMAIL_1, ...) exactly
  as written. Write the results into `clean/`.
- Step 3: run `python privacy_gate.py restore clean/<result file>` for each result. Tell the user the file with the
  real names is in `clean_restored/`. Do not open it.
- If the gate fails (for example no answer from the KTH GPU server off the KTH network), stop and say so. Never
  work around it by reading the originals.
