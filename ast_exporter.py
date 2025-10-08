import json
from ast_nodes import ASTNode, Program, Compound, Assign, Var, Num, BinOp, If, While, Call, VarDecl, ConstDecl, TypeDecl, FunctionDecl
from typing import Any, Dict, List


# ---------- EXPORTAÇÃO PARA JSON ----------
def ast_to_dict(node: ASTNode) -> Any:
    if isinstance(node, list):
        return [ast_to_dict(x) for x in node]
    if not isinstance(node, ASTNode):
        return node
    result = {"type": node.__class__.__name__}
    for field, value in node.__dict__.items():
        result[field] = ast_to_dict(value)
    return result

def export_ast_to_json(node: ASTNode, file_path: str):
    data = ast_to_dict(node)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ AST exportada para JSON com sucesso: {file_path}")

# ---------- EXPORTAÇÃO PARA GRAPHVIZ ----------
class DotExporter:
    def __init__(self):
        self.lines: List[str] = []
        self.counter = 0

    def new_id(self) -> str:
        self.counter += 1
        return f"n{self.counter}"

    def node_label(self, node: ASTNode) -> str:
        if isinstance(node, Var):
            return f"Var({node.name})"
        elif isinstance(node, Num):
            return f"Num({node.value})"
        elif isinstance(node, BinOp):
            return f"BinOp({node.op})"
        elif isinstance(node, Call):
            return f"Call({node.name})"
        else:
            return node.__class__.__name__

    def export(self, node: ASTNode, file_path: str):
        self.lines.append("digraph AST {")
        self._visit(node)
        self.lines.append("}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
        print(f"✅ AST exportada para DOT com sucesso: {file_path}")

    def _visit(self, node: ASTNode, parent_id: str = None):
        node_id = self.new_id()
        label = self.node_label(node).replace('"', "'")
        self.lines.append(f'  {node_id} [label="{label}", shape=box, style=rounded];')
        if parent_id:
            self.lines.append(f"  {parent_id} -> {node_id};")

        # percorrer filhos
        for field, value in getattr(node, "__dict__", {}).items():
            if isinstance(value, ASTNode):
                self._visit(value, node_id)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self._visit(item, node_id)