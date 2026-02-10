
# Commit Message Guidelines

## Format

All commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short description>
```

Context:
This repository it's about an Instruction Set Architecture (ISA) container, here you will found the code of each instruction... just its code, because that's can not are in the DB.

Where:

- **`<type>`** — obligatory; describes the purpose of the change (see list below).
- **`<scope>`** — obligatory; identifies the ISA version (like x.x.x) to which the change applies.
- **`<scope`** - optional; in case about no instruction commit then this will be optional to indentifies the helper function.
- **`<short description>`** — obligatory; concise summary of the change, written in **imperative mood** (e.g., _add_, _fix_, _update_, _remove_) in case about no instruction commit, if no that's right then only type "new AMFx({ISA Version like <scope>... x.x.x})::{microfamily like add, mov}.{operands type in case of that would necesary like reg_imm, mem_reg, imm}", **max 50 characters**.

## Examples

feat(1.0.0): new AMFx(1.0.0)::add.reg_reg
fix(uploader): fix any bugs in the helper function uploader 
refactor(test): refactor some tests to improve readability
test: add more unit tests for the instruction implementation
chore(pydantic): update pydantic to v2.0.0
docs(readme): clarify setup instructions

## Allowed Commit Types

| Type         | Purpose                                                 |
| ------------ | ------------------------------------------------------- |
| **feat**     | Introduce a new feature                                 |
| **fix**      | Fix a bug or regression                                 |
| **refactor** | Code change that neither fixes a bug nor adds a feature |
| **perf**     | Improve performance                                     |
| **docs**     | Documentation changes only                              |
| **style**    | Code style changes (formatting, semicolons, etc.)       |
| **test**     | Add or modify tests                                     |
| **build**    | Changes to build system or dependencies                 |
| **ci**       | CI/CD configuration changes                             |
| **chore**    | Routine maintenance tasks                               |
| **revert**   | Revert a previous commit                                |

## Additional Rules

- Keep the **first line under 50 characters**.
- Use **present tense** and **imperative mood** (“add” not “added” or “adds”).
- Do **not** end the short description with a period.
- Optionally, include a blank line and a detailed description if necessary.

---

**Example with details:**
feat(1.0.0): new AMFx(1.0.0)::hlt

This commit introduces a new instruction to the ISA version 1.0.0, the HLT (halt) instruction, which halts the CPU until the next external interrupt is received. This is a crucial addition for power management and efficient CPU usage.

---

**In short:**  
Write clear, consistent, and meaningful commit messages — they are part of your project’s documentation.
