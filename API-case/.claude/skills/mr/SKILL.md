---
name: mr
description: Generate a merge request description following the team template. Use when asked to write an MR/PR description or prepare a merge request.
---

# MR Description Generator

Follow this procedure to write a merge request description:

1. **Understand the change**: Run `git log` and `git diff` against the target
   branch (usually `main`) to see every commit and changed file in this MR.
2. **Fill the template**: Use `template.md` in this skill directory as the
   base. Write in Korean.
3. **Template rules**:
   - Required sections must always be filled; conditional sections only when
     applicable — delete unused conditional sections including their headers.
   - Describe *what changed* and *why*, not *how* (the code explains how).
   - In the checklist, keep only applicable blocks: the ML block must be
     deleted entirely for non-ML repositories.
   - If verification was not performed, state it explicitly with the reason
     (e.g. "검증 안 함: <사유>") — never leave the section blank.
4. **Output**: Print the completed MR description as a markdown code block so
   it can be copy-pasted into the MR form. Do not push or create the MR unless
   explicitly asked.
