
from subprocess import run
from typer import Argument, Option, run as run_typer
from pathlib import Path
from rich.console import Console
from pydantic import BaseModel

console: Console = Console()

class ISAPath(BaseModel):
    version: str
    family: str
    instruction: str

    def __str__(self) -> str:
        return f'isa/{self.version}/{self.family}/{self.instruction}'

    def beauty_instr(self, toprint: bool = False) -> str:
        return (
            f'[yellow][bold]AMFx([purple]{self.version}[/purple])[/bold]::{self.instruction.replace("/", ".").replace(".h", "")}[/yellow]'
            if toprint
            else
            f'AMFx({self.version})::{self.instruction.replace("/", ".").replace(".h", "")}'
        )
    
    def validate_instr(self) -> bool:
        _: Path = self.to_pathlib()
        if not (self.instruction.endswith('.h') and _.is_file()):
            console.print(f'[red]Error:[/red] The instruction implementation file "{_}" does not exist.')
            return False
        return True

    def to_pathlib(self) -> Path:
        return Path(f'isa/{self.version}/{self.family}/{self.instruction}')

def lunch_tests(path: Path) -> bool:
    try:
        run(f'python -m test {path}', check=True)
        return True
    except Exception as e:
        console.print(f'[red][!] Test Error:[/red] | Any test failed |...')
        return False

def commit(path: ISAPath) -> None:
    """
    Commits the changes to the repository.

    Args:
        version (str): The version of the ISA.
        family (str): The family of the instruction.
        instruction (str): The path to the instruction implementation file.
        
    Use:
        python upload.py commit --version <version>
    """

    path_instance: Path = path.to_pathlib()

    try:
        run(f'git add {path_instance}', check=True)
        run(f'git commit -m "feat({path.version}): new {path.beauty_instr()}"', check=True)
        run(f'git push', check=True)
    except Exception as e:
        console.clear()
        console.print(f'[red][!] Commit Error:[/red] | {e} |...')
        return
    
    console.clear()
    console.clear()
    console.log(f'[green][+] Success:[/green] New Instruction Implementation has been uploaded to the ISA {path.beauty_instr(toprint=True)}')

def upload(
    version: str = Option(..., '--version', '-v', help='The version of the ISA.'),
    family: str = Option(..., '--family', '-f', help='The family of the instruction.'),
    instruction: str = Option(..., '--instruction', '-i', help='The path to the instruction implementation file.')
) -> None:
    """
    Adds a new instruction implementation to the repository.

    Args:
        version (str): The version of the ISA.
        family (str): The family of the instruction.
        instruction (str): The path to the instruction implementation file.

    Use:
        python upload.py add --version <version> --family <family> --instruction <instruction>
    """
    
    path: ISAPath = ISAPath(version=version, family=family, instruction=instruction)
    path_instance: Path = path.to_pathlib()

    if not path.validate_instr(): return

    lunch_tests(path_instance)
    
    commit(path=path)

    

if __name__ == '__main__':
    run_typer(upload)
