from typing import TypedDict
from pathlib import Path
from enum import StrEnum
import re

class Operand(StrEnum):
    REG = 'register'
    IMM = 'immediate'
    MEM = 'memory'
    NONE = 'none'

class Instruction(TypedDict):
    mnemonic: str
    operands: list[Operand]
    path: Path
    code: str

header_parser = re.compile(r'^[a-zA-Z0-9\.\:\_\-\s\\]+\.h$')
operand_parser = re.compile(r'(reg|imm|mem|none)', re.IGNORECASE)

def parse_operands(filename: str) -> list[Operand]:
    return [Operand[op.upper()] for op in operand_parser.findall(filename)]

def parse(path: Path) -> list[Instruction]:
    isa: list[Instruction] = []

    for file in path.rglob('*.h'):
        if not header_parser.match(file.name):
            continue

        operands: list[Operand] = parse_operands(file.name)
        isa.append({
            'mnemonic': (
                file.parent.name
                if operands or file.stem in ('_', 'entry', 'impl', 'instr', 'main')
                else file.stem
            ),
            'operands': operands,
            'path': file,
            'code': file.read_text()
        })

    return isa

if __name__ == '__main__':
    from sys import argv
    ISA: list[Instruction] = parse(Path(argv[1] or '.'))
    print(ISA)
