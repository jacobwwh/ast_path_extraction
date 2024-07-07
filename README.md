An implementation of the path extraction algorithm in the paper "Code-Aware Prompting: A study of Coverage guided Test Generation in Regression Setting using LLM".

Different from the original paper, our implementation does not extract the complete path from program entrance to the target branch. We only return the path of all the necessary conditions to reach the target branch.

## Usage

```bash
python main.py --file {path_to_python_file} --line {target_line_number}
```

## Return 

A list of nodes along the execution path, each node is of the following format 

```Python
{'content': branch condition, 'line': line number of condition, 'satisfy': whether this condition is satisfied}
```

## Requirements

tree-sitter: see [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)
