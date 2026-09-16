## Commit Message Specification (numpy style)

> **⚠️ SUBJECT LINE ONLY — A COMMIT MESSAGE IS EXACTLY ONE LINE. ⚠️**
> **NEVER write a commit body, description, bullet list, or trailer.**
> **NEVER use multiple `-m` flags, heredocs, or newlines in the message.**
> **NEVER add `Co-Authored-By` or any other trailer.**
> The only valid form is: `git commit -m "TYPE: one sentence"`

1. The last commit message before pushing must be written as a single sentence in English: (Because when you squash in MR, only the last commit message is left.)
    1. Message type: content, where, what, why in one sentence.
    2. The example is as follows.
    ```sh
    # ✅ Correct — one -m, one line
    $ git commit -m "ADD: add ontology domain(AR, SR)"
    $ git commit -m "MOD: modify RDCNet parameter"
    $ git commit -m "TST: RDCNet training test on new device(H200)"

    # ❌ WRONG — never do this
    $ git commit -m "ADD: add ontology domain" -m "details..."   # second -m = body
    $ git commit -m "ADD: add ontology domain
    >
    > - added AR domain
    > - added SR domain"                                         # multi-line = body
    ```

### Type priority
When both tables could apply, **prefer the project common type** (ADD/DEL/MOD/TMP).
Fall back to a numpy standard type only when no project type fits
(e.g. `DOC`, `TST`, `BUG`, `STY`). One type per commit — never combine.

### Project common type

| Type | Meaning |
|------|------|
| ADD | add new module |
| DEL | remove old component |
| MOD | change the logic from random to rule-based |
| TMP | temporal commit |

### numpy standard type

| Type | Meaning |
|------|------|
| API | an (incompatible) API change |
| BENCH | changes to the benchmark suite |
| BLD | change related to building numpy |
| BUG | bug fix |
| CI | continuous integration |
| DEP | deprecate something, or remove a deprecated object |
| DEV | development tool or utility |
| DOC | documentation |
| ENH | enhancement |
| MAINT | maintenance commit (refactoring, typos, etc.) |
| MNT | alias for MAINT |
| NEP | NumPy enhancement proposals |
| REL | related to releasing numpy |
| REV | revert an earlier commit |
| STY | style fix (whitespace, PEP8) |
| TST | addition or modification of tests |
| TYP | static typing |
| WIP | work in progress, do not merge |

## Rules:
- Do not use scope brackets (e.g., `(ontoagent)`);
the abbreviation replaces classification.
- Keep the summary concise and in the imperative form. Detailed background belongs in the **MR description** (`/mr`), never in the commit message.
- One line means one line: if the change feels too big for a single sentence, that is a signal to split the commit, not to add a body.
- Examples: `ENH: Add Stage 2 batch-ID gate`, `BUG: Fix node collapse of objects in the same class`, `DOC: README description of two stages`.
