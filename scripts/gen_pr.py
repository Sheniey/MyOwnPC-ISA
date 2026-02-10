
from typer import Typer, Argument, Option
from rich.console import Console
from pathlib import Path
from pyperclip import copy
from datetime import datetime as dt

app: Typer = Typer()
console: Console = Console()

@app.command(
    'new'
)
def new(
    username: str = Option(..., '--username', '-u', help='Your GitHub username.'),
    version: str = Option(..., '--version', '-v', help='The version of the ISA.'),
    family: str = Option(..., '--family', '-f', help='The family of the instruction.'),
    instruction: str = Option(..., '--instruction', '-i', help='The path to the instruction implementation file.'),
    opcode: str = Option('0000', '--opcode', '-o', help='The opcode of the instruction in hexadecimal. (optional, default: 0x0000)'),
    description: str = Option(
        '> A short description of your institution that you want to add.',
        '--description', '-d',
        help='The description of the instruction.'
    ),
    operation: str = Option(
        '/* no operation provided */',
        '--operation', '-op',
        help='A short description of the operation performed by your instruction. (Optional)'
    ),
    tested: bool = Option(
        False,
        '--tested', '-t',
        help='Whether you have tested your instruction implementation or not. (Optional)'
    ),
    new_family: bool = Option(
        False,
        '--new-family/--no-new-family', '-nf/-nnf',
        help='Whether you create a new family to accommodate your instruction or not. (Optional)'
    ),
    no_additional_resources: bool = Option(
        False,
        '--no-additional-resources/--additional-resources', '-nar/-ar',
        help='Whether your implementation needs any additional resources or a post update or not. (Optional)'
    ),
    ready_for_review: bool = Option(
        False,
        '--ready-for-review/--not-ready-for-review', '-rfr/-nrfr',
        help='Whether your implementation is complete and ready for review or not. (Optional)'
    ),
    aware_of_preferences: bool = Option(
        False,
        '--aware-of-preferences/--not-aware-of-preferences', '-aop/-naop',
        help='Whether you are aware that your questionnaire preferences may vary or not. (Optional)'
    ),
    operands_1: tuple[bool, bool, bool] = Option(
        ...,
        '--operands-1', '-op1',
        help='The types of the first operand in order like <register> <immediate> <memory>. (Required) | Ex: --operands-1 true false true'
    ),
    operands_2: tuple[bool, bool, bool] = Option(
        ...,
        '--operands-2', '-op2',
        help='The types of the second operand in order like <register> <immediate> <memory>. (Required) | Ex: --operands-2 false true false'
    ),
    notes: str = Option(
        '> Some notes about possible problems or preferences regarding how you want your instruction to be handled. (Optional)',
        '--notes', '-n',
        help='Some notes about possible problems or preferences regarding how you want your instruction to be handled. (Optional)'
    )
) -> None:
    
    check = lambda checked: '[X]' if checked else '[ ]'

    mnemonic: str = instruction.replace('.h', '').split('/')[-1]
    formatted_opcode: str = f'0x{int(opcode, 16):>04X}'
    payload: str = \
f"""

# {mnemonic.upper()} - {formatted_opcode}

> **PR Purpose:** *`POST INSTRUCTION`*
>
> **Branch:** [{family.lower()}/{instruction.lower()}](https://github.com/{username}/MyOwnPC-ISA/tree/main/isa/{version}/{family.lower()}/{instruction.lower()}) ~ **ISA {version}**
>  
> **Author:** {username}
>
> **Date:** {dt.now().strftime('%Y-%m-%d')}

---

#### Description:
{description}

#### Operation:
```csharp
{operation}
```

---

#### Questionary:
> [!IMPORTANT]
> All the content in this questionnaire *may be added exactly as it appears*, ***but*** it *may be subject to edits.* **Ex:** Opcode: `0x00AF` but in the end it is added as Opcode: `0x002A` for convenience.

**Mnemonic:** `{mnemonic.upper()}`

**Opcode:** `{formatted_opcode}`

**ISA:** `{version}`

{check(tested)} **I tested my instruction implementation.**

{check(new_family)} **I create a new family to accommodate my instruction.**

{check(no_additional_resources)} **My implementation don't need any additional resources or a post update.**

{check(ready_for_review)} **My implementation is complete and ready for review.**

{check(aware_of_preferences)} **I am aware that my questionnaire preferences may vary.**

---

#### Operands 1:
{check(operands_1[0])} **Register**
{check(operands_1[1])} **Immediate**
{check(operands_1[2])} **Memory**

#### Operands 2:
{check(operands_2[0])} **Register**
{check(operands_2[1])} **Immediate**
{check(operands_2[2])} **Memory**

---

#### Notes:
{notes}

"""
    
    copy(payload)
    console.print(f'[green][✓] Payload copied to clipboard![/green]\n\n{payload}')

@app.command(
    'commit'
)
def commit() -> None: ...

if __name__ == '__main__':
    app()
