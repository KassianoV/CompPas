from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class ASTNode:
    pass

# ========== EXPRESSÕES ==========
@dataclass
class Num(ASTNode):
    value: Union[int, float]

@dataclass
class Var(ASTNode):
    name: str

@dataclass
class BinOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode

@dataclass
class Call(ASTNode):
    name: str
    args: List[ASTNode]

# ========== DECLARAÇÕES ==========
@dataclass
class VarDecl(ASTNode):
    names: List[str]
    type_name: str

# ========== COMANDOS ==========
@dataclass
class Assign(ASTNode):
    target: Var
    value: ASTNode

@dataclass
class If(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode]

@dataclass
class While(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass
class Compound(ASTNode):
    statements: List[ASTNode]

# ========== PROGRAMA ==========
@dataclass
class Program(ASTNode):
    name: str
    var_decls: List[VarDecl]
    block: Compound
