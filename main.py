from ast_path import find_node_and_path
from argparse import ArgumentParser
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

argparser=ArgumentParser()
argparser.add_argument('--file', default='example/e1.py')
argparser.add_argument('--line', type=int, default=7)

args=argparser.parse_args()

PY_LANGUAGE = Language(tspython.language())
parser=Parser(PY_LANGUAGE)

if __name__ == '__main__':
    example_code=open(args.file).read()
    tree=parser.parse(bytes(example_code,'utf-8'))
    target_line=args.line-1 # 0-indexed
    minimal_target_path=find_node_and_path(tree, target_line)
    print(minimal_target_path)
