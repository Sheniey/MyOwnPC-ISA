
from typing import Final as Const
from sys import argv
from tree_sitter import Node
from pathlib import Path
import pytest

from parser import parse_cpp_file, node_text

if len(argv) < 2:
    print(' [!] Usage: python test.py <path_to_cpp_file>')
    exit()

IMPLEMENT_NOT_FOUND: Const[str] = ' [!] Instruction Error: | The Instruction Implementation shall be named "entry" |...'

COMMENT_NOT_FOUND: Const[str] = ' [!] Comment Error: | The Instruction must have a Detailed Comment |...'
EMPTY_COMMENT: Const[str] = ' [!] Comment Error: | The Comment must not be empty |...'
INVALID_COMMENT_FORMAT: Const[str] = ' [!] Comment Error: | The Comment must be in the format /* ... */ or /** ... */ |...'
MISSING_DESCRIPTION: Const[str] = ' [!] Comment Error: | The Comment must include a @brief tag describing the instruction |...'
MISSING_MNEMONIC: Const[str] = ' [!] Comment Error: | The Comment must include a @brief tag with the instruction mnemonic in the description like "@brief\n```csharp\nadd r16, i16\n```" |...'
MISSING_OPERATION: Const[str] = ' [!] Comment Error: | The Comment must include a detailed operation description with a code block like "#### Operation:\n```csharp\n[1] Register dest;\n[2] Number src;\n[3]\ndest = dest + src;\n```" |...'
MISSING_FAMILY_INSTRUCTION: Const[str] = ' [!] Comment Error: | The Comment must include a @class tag specifying the instruction family like "@class add" |...'
MISSING_RETURN: Const[str] = ' [!] Comment Error: | The Comment must include a @return tag stating the return type in the format "@return\n```csharp\ncppTypeToReturn```" |...'
MISSING_NOTE: Const[str] = ' [!] Comment Error: | The Comment should include a @note tag with additional information, a bit more technical, about the instruction implementation |...'
MISSING_DATE: Const[str] = ' [!] Comment Error: | The Comment must include a @date tag with the date of the completed implementation |...'
MISSING_AUTHOR: Const[str] = ' [!] Comment Error: | The Comment must include an @author tag with the name of the implementer |...'
MISSING_DOC_LINKS: Const[str] = ' [!] Comment Error: | The Comment should include @see references to official AMFx architecture manuals or documentation/media to learn more about that instruction |...'

INVALID_PARAM_LENGTH: Const[str] = ' [!] Signature Error: | The Instruction Signature must include exactly 2 parameters |...'
MISSING_CPU_API: Const[str] = ' [!] Signature Error: | The Instruction Signature must include a parameter named "api" of type "CPU_API*" |...'
MISSING_INSTR_PAYLOAD: Const[str] = ' [!] Signature Error: | The Instruction Signature must include a parameter named "payload" of type "InstructionPackage" |...'
NOEXCEPT_NOT_IMPLEMENTED: Const[str] = ' [!] Signature Error: | The Instruction Signature should be marked as noexcept to improve the performance |...'

def _test_comments(node: Node) -> None:
    """
## Example of a well-formatted comment for an instruction implementation:

/**
 ## ADD r16, i16

 @brief Adds a 16-bit immediate value to a 16-bit register.
 @brief
```csharp
add r16, i16
```

 #### Operation:
```csharp
[1] Register dest;
[2] Number src;
[3] 
[4] dest = dest + src;
```

 @class add
 @param api Pointer to the CPU_API safe context instance.
 @param payload The instruction package containing operands.
 @return 
```csharp
void
```

 @note This function handles the addition of a 16-bit immediate value to a specified 16-bit register, updating the register with the result.
 
 @todo Implement flag updates (Zero, Sign, Overflow, Carry, etc.) after the addition operation.
 @todo Add @see references to x86 architecture manuals.

 @date 02/01/2025
 @author Sheñey
 */
    """

    comment: Node = node.prev_named_sibling

    assert comment.type == 'comment', COMMENT_NOT_FOUND
    assert len(comment.text) > 4, EMPTY_COMMENT
    
    assert (comment.text.startswith(b'/*') or comment.text.startswith(b'/**')) and comment.text.endswith(b'*/'), INVALID_COMMENT_FORMAT
    assert comment.text.count(b'@brief') == 2, MISSING_DESCRIPTION
    assert b'```csharp\n' in comment.text and b'\n```' in comment.text, MISSING_MNEMONIC
    assert b'#### Operation:\n```csharp\n' in comment.text and b'\n```' in comment.text, MISSING_OPERATION
    assert b'@class ' in comment.text, MISSING_FAMILY_INSTRUCTION
    assert b'@return\n```csharp\n' in comment.text and b'\n```' in comment.text, MISSING_RETURN
    assert b'@note ' in comment.text, MISSING_NOTE
    assert b'@date ' in comment.text, MISSING_DATE
    assert b'@author ' in comment.text, MISSING_AUTHOR
    assert b'@see ' in comment.text, MISSING_DOC_LINKS

def _test_signatures(node: Node | None) -> None:
    assert node is not None, IMPLEMENT_NOT_FOUND
    assert node.type == 'function_definition', IMPLEMENT_NOT_FOUND

    raw_parameters: Node | None = node.child_by_field_name('parameters')
    parameters: list[Node] = [
        c for c in raw_parameters.children
        if c.type == 'parameter_declaration'
    ]

    assert parameters is not None, INVALID_PARAM_LENGTH
    assert len(parameters) == 2, INVALID_PARAM_LENGTH
    assert b'CPU_API* api' in parameters[0].text, MISSING_CPU_API
    assert b'InstructionPackage payload' in parameters[1].text, MISSING_INSTR_PAYLOAD
    assert b'noexcept' in node.text, NOEXCEPT_NOT_IMPLEMENTED

def walk(node: Node):
    yield node
    for c in node.children:
        yield from walk(c)

def test() -> None:
    path: Path = Path(argv[1])
    if not path.is_file():
        print(f'Error: {path} is not a valid file.')
        exit()
    
    root_node: Node = parse_cpp_file(path)
    instruction: Node | None = None
    for node in walk(root_node):
        print(node.type, node_text(node, root_node.text))
        if node.type == 'function_definition':
            name = node.child_by_field_name('identifier')
            if name and  b'entry' in name.text:
                instruction = node
                break
    # else:
    #     assert False, IMPLEMENT_NOT_FOUND

    _test_signatures(instruction)
    _test_comments(instruction)
    
if __name__ == '__main__':
    test()
