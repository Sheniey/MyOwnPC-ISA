
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Tree, Node
from pathlib import Path

CPP_LANGUAGE: Language = Language(tscpp.language())
parser: Parser = Parser(CPP_LANGUAGE)

def parse_cpp_code(code: str, *, encoding='utf8') -> Node:
    tree: Tree = parser.parse(bytes(code, encoding=encoding))
    return tree.root_node

def parse_cpp_file(path: Path, *, encoding='utf8') -> Node:
    with open(path, 'r', encoding=encoding) as file:
        code: str = file.read()
        print(code)
    return parse_cpp_code(code, encoding=encoding)

def node_text(node: Node, source: bytes) -> bytes:
    return source[node.start_byte:node.end_byte]
