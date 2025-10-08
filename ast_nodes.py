from dataclasses import dataclass
from typing import List, Optional, Union

# ============ NÓ BASE ============
@dataclass
class ASTNode:
    pass

# ============ PROGRAMA PRINCIPAL ============
@dataclass
class Program(ASTNode):
    name: str
    decls: List[ASTNode]
    block: 'Compound'

# ============ DECLARAÇÕES ============
@dataclass
class VarDecl(ASTNode):
    names: List[str]
    type_name: str

@dataclass
class ConstDecl(ASTNode):
    name: str
    value: ASTNode

@dataclass
class TypeDecl(ASTNode):
    name: str
    definition: str  # Pode ser expandido futuramente (array, record etc.)

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List['VarDecl']
    return_type: str
    local_vars: List['VarDecl']
    body: 'Compound'

# ============ COMANDOS ============
@dataclass
class Compound(ASTNode):
    statements: List[ASTNode]

@dataclass
class Assign(ASTNode):
    target: 'Var'
    value: ASTNode

@dataclass
class If(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None

@dataclass
class While(ASTNode):
    condition: ASTNode
    body: ASTNode

@dataclass
class Call(ASTNode):
    name: str
    args: List[ASTNode]

# ============ EXPRESSÕES ============
@dataclass
class BinOp(ASTNode):
    op: str
    left: ASTNode
    right: Optional[ASTNode]  # pode ser None (para operador 'not')

@dataclass
class Num(ASTNode):
    value: Union[int, float]

@dataclass
class Var(ASTNode):
    name: str
    
@dataclass
class String(ASTNode):
    value: str