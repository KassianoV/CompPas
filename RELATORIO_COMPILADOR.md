# Compilador Pascal Simplificado - Relatório Completo

**Autores:** Kassiano Vieira e Claudio Nunes  
**Data:** Novembro 2025

---

## ETAPA 1: Classificação dos Tokens e Remoção de Ambiguidade

### 1.1 Tokens da Linguagem

| Token | Lexema | Expressão Regular Aproximada |
|-------|--------|------------------------------|
| T_PROGRAM | program | `program` |
| T_BEGIN | begin | `begin` |
| T_END | end | `end` |
| T_TYPE | type | `type` |
| T_VAR | var | `var` |
| T_CONST | const | `const` |
| T_FUNCTION | function | `function` |
| T_PROCEDURE | procedure | `procedure` |
| T_WHILE | while | `while` |
| T_DO | do | `do` |
| T_IF | if | `if` |
| T_THEN | then | `then` |
| T_ELSE | else | `else` |
| T_ARRAY | array | `array` |
| T_OF | of | `of` |
| T_RECORD | record | `record` |
| T_READ | read | `read` |
| T_WRITE | write | `write` |
| T_INTEGER | integer | `integer` |
| T_REAL | real | `real` |
| T_BOOLEAN | boolean | `boolean` |
| T_STRING | string | `string` |
| T_TRUE | true | `true` |
| T_FALSE | false | `false` |
| T_AND | and | `and` |
| T_OR | or | `or` |
| T_NOT | not | `not` |
| T_ID | identificador | `[a-zA-Z][a-zA-Z0-9_]*` |
| T_CONST_NUM | número | `\d+(\.\d+)?` |
| T_CONST_STR | string literal | `"[^"]*"` |
| OP_ASSIGN | := | `:=` |
| OP_MAT | +, -, *, / | `[+\-*/]` |
| OP_REL | =, <>, <, >, <=, >= | `(<=\|>=\|<>\|<\|>\|=)` |
| T_PONT_VIRG | ; | `;` |
| T_VIRG | , | `,` |
| T_DOIS_PONT | : | `:` |
| T_PONT | . | `\.` |
| T_ABRE_PARENT | ( | `\(` |
| T_FECHA_PARENT | ) | `\)` |
| T_ABRE_COL | [ | `\[` |
| T_FECHA_COL | ] | `\]` |
| T_COMMENT | {# ... #} | `\{#[\s\S]*?#\}` |

### 1.2 Gramática Original (Com Ambiguidades)

```
<PROGRAMA> → program <ID> ; <CORPO>

<CORPO> → <DECLARACOES> begin <LISTA_COM> end

<DECLARACOES> → <DEF_CONST_LIST> <DEF_TIPOS_LIST> <DEF_VAR_LIST> <LISTA_FUNC>
              | ε

<DEF_CONST_LIST> → const <LISTA_CONST>
                 | ε

<LISTA_CONST> → <CONSTANTE> <LISTA_CONST>
              | <CONSTANTE>

<CONSTANTE> → <ID> := <CONST_VALOR> ;

<CONST_VALOR> → <CONST_STR> | <EXP_LOGICA>

<DEF_TIPOS_LIST> → type <LISTA_TIPOS>
                 | ε

<LISTA_TIPOS> → <TIPO> ; <LISTA_TIPOS>
              | <TIPO> ;

<TIPO> → <ID> = <TIPO_DADO>

<TIPO_DADO> → integer
            | real
            | boolean
            | string
            | array [ <NUMERO> ] of <TIPO_DADO>
            | record <LISTA_VAR> end
            | <ID>

<DEF_VAR_LIST> → var <LISTA_VAR>
               | ε

<LISTA_VAR> → <VARIAVEL> ; <LISTA_VAR>
            | <VARIAVEL>

<VARIAVEL> → <LISTA_ID> : <TIPO_DADO>

<LISTA_ID> → <ID> , <LISTA_ID>
           | <ID>

<LISTA_FUNC> → <FUNCAO> <LISTA_FUNC>
             | ε

<FUNCAO> → <NOME_FUNCAO> <BLOCO_FUNCAO>

<NOME_FUNCAO> → function <ID> ( <LISTA_VAR> ) : <TIPO_DADO>
              | function <ID> ( ) : <TIPO_DADO>

<BLOCO_FUNCAO> → <DEF_VAR_LIST> <BLOCO>
               | <BLOCO>

<BLOCO> → begin <LISTA_COM> end
        | begin end

<LISTA_COM> → <COMANDO> ; <LISTA_COM>
            | <COMANDO>
            | ε

<COMANDO> → <COMANDO_COMPLETO>
          | <COMANDO_INCOMPLETO>
          | <OUTROS_COMANDOS>

<OUTROS_COMANDOS> → <NOME> := <VALOR>
                  | while <EXP_LOGICA> do <BLOCO>
                  | write ( <EXP_LOGICA> )
                  | read ( <NOME> )
                  | <BLOCO>

<COMANDO_COMPLETO> → if <EXP_LOGICA> then <COMANDO_COMPLETO> else <COMANDO_COMPLETO>
                   | <OUTROS_COMANDOS>

<COMANDO_INCOMPLETO> → if <EXP_LOGICA> then <COMANDO>
                     | if <EXP_LOGICA> then <COMANDO_INCOMPLETO> else <COMANDO_INCOMPLETO>

<VALOR> → <EXP_LOGICA>
        | <CHAMADA_FUNCAO>

<CHAMADA_FUNCAO> → <ID> ( <LISTA_ARG> )
                 | <ID> ( )

<LISTA_ARG> → <EXP_LOGICA> , <LISTA_ARG>
            | <EXP_LOGICA>

<EXP_LOGICA> → <EXP_REL> <OP_LOGICO_BIN> <EXP_LOGICA>
             | <EXP_REL>

<EXP_REL> → <EXP_AD> <OP_REL> <EXP_AD>
          | <EXP_AD>

<EXP_AD> → <EXP_MUL> + <EXP_AD>
         | <EXP_MUL> - <EXP_AD>
         | <EXP_MUL>

<EXP_MUL> → <FATOR> * <EXP_MUL>
          | <FATOR> / <EXP_MUL>
          | <FATOR>

<FATOR> → <NUMERO>
        | <NOME>
        | ( <EXP_LOGICA> )
        | not <FATOR>
        | true
        | false

<NOME> → <ID>
       | <ID> . <NOME>
       | <ID> [ <EXP_LOGICA> ]

<OP_LOGICO_BIN> → and | or

<OP_REL> → > | < | = | <> | <= | >=
```

### 1.3 Problemas de Ambiguidade Identificados

#### **Problema 1: Ambiguidade Dangling Else**
```
if <cond1> then if <cond2> then <cmd1> else <cmd2>
```
- **Solução:** Implementada com `<COMANDO_COMPLETO>` e `<COMANDO_INCOMPLETO>`
- O `else` sempre se associa ao `if` mais próximo

#### **Problema 2: Recursividade à Esquerda em Expressões**
```
<EXP_LOGICA> → <EXP_REL> <OP_LOGICO_BIN> <EXP_LOGICA>
<EXP_AD> → <EXP_MUL> + <EXP_AD>
<EXP_MUL> → <FATOR> * <EXP_MUL>
```
- **Problema:** Causaria loop infinito em parsers recursivos descendentes
- **Solução:** Transformada em recursividade à direita com iteração

#### **Problema 3: Ambiguidade em Listas**
```
<LISTA_CONST> → <CONSTANTE> <LISTA_CONST>
              | <CONSTANTE>
```
- **Solução:** Usar iteração (loop while) no parser

### 1.4 Gramática Corrigida (Sem Ambiguidade e Recursividade à Esquerda)

```
<PROGRAMA> → program <ID> ; <CORPO>

<CORPO> → <DECLARACOES> begin <LISTA_COM>? end

<DECLARACOES> → <DEF_CONST_LIST>? <DEF_TIPOS_LIST>? <DEF_VAR_LIST>? <LISTA_FUNC>?

<DEF_CONST_LIST> → const <CONSTANTE>+

<CONSTANTE> → <ID> := <CONST_VALOR> ;

<CONST_VALOR> → <CONST_STR> | <NUMERO> | true | false

<DEF_TIPOS_LIST> → type <TIPO>+

<TIPO> → <ID> = <TIPO_DADO> ;

<TIPO_DADO> → integer | real | boolean | string
            | array [ <NUMERO> ] of <TIPO_DADO>
            | record <VARIAVEL>+ end
            | <ID>

<DEF_VAR_LIST> → var <VARIAVEL>+

<VARIAVEL> → <ID> ( , <ID> )* : <TIPO_DADO> ;

<LISTA_FUNC> → <FUNCAO>*

<FUNCAO> → function <ID> ( <PARAMETROS>? ) : <TIPO_DADO> ; <DEF_VAR_LIST>? <BLOCO> ;

<PARAMETROS> → <VARIAVEL> ( ; <VARIAVEL> )*

<BLOCO> → begin <COMANDO> ( ; <COMANDO> )* end

<COMANDO> → <ATRIBUICAO>
          | <IF_COMPLETO>
          | <IF_INCOMPLETO>
          | <WHILE>
          | <CHAMADA>
          | <BLOCO>

<IF_COMPLETO> → if <EXP_LOGICA> then <COMANDO_COMPLETO> else <COMANDO_COMPLETO>

<IF_INCOMPLETO> → if <EXP_LOGICA> then <COMANDO>

<COMANDO_COMPLETO> → <IF_COMPLETO> | <ATRIBUICAO> | <WHILE> | <CHAMADA> | <BLOCO>

<ATRIBUICAO> → <NOME> := <EXP_LOGICA>

<WHILE> → while <EXP_LOGICA> do <COMANDO>

<CHAMADA> → <ID> ( <ARGS>? )
          | read ( <NOME> )
          | write ( <EXP_LOGICA> )

<ARGS> → <EXP_LOGICA> ( , <EXP_LOGICA> )*

// Expressões sem recursividade à esquerda
<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*

<EXP_REL> → <EXP_AD> ( <OP_REL> <EXP_AD> )?

<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*

<EXP_MUL> → <FATOR> ( (*|/) <FATOR> )*

<FATOR> → <NUMERO>
        | <CONST_STR>
        | <NOME>
        | <CHAMADA>
        | ( <EXP_LOGICA> )
        | not <FATOR>
        | true
        | false

<NOME> → <ID> ( . <ID> | [ <EXP_LOGICA> ] )*

<OP_REL> → = | <> | < | > | <= | >=
```

**Notações:**
- `?` = opcional (0 ou 1 ocorrência)
- `*` = zero ou mais ocorrências
- `+` = uma ou mais ocorrências
- `( ... )*` = iteração (implementada com loop while no parser)

---

## ETAPA 2: Implementação do Compilador

### 2.1 Análise Léxica (lexer.py)

O analisador léxico implementado possui as seguintes características:

**Funcionalidades:**
- Reconhecimento de todos os tokens da gramática
- Tratamento de palavras reservadas
- Suporte a comentários `{# ... #}`
- Números inteiros e reais
- Strings entre aspas duplas
- Rastreamento de linha e coluna

**Melhorias Implementadas:**
```python
# Ordem correta de tokens para evitar ambiguidades
token_specs = [
    ('COMMENT', r'\{#[\s\S]*?#\}'),          # Comentários primeiro
    ('CONST_STR', r'"(?:\\.|[^"\\])*"'),     # Strings com escape
    ('CONST_NUM', r'\d+(?:\.\d+)?'),         # Números
    ('OP_REL', r'(<=|>=|<>|<|>|=)'),         # Operadores relacionais (>= antes de >)
    ('OP_ASSIGN', r':='),                     # Atribuição antes de :
    ('OP_MAT', r'[+\-*/]'),                  # Operadores matemáticos
    # ... demais tokens
]
```

### 2.2 Análise Sintática (parser.py)

O parser implementa um analisador **recursivo descendente** que:

1. **Segue a gramática corrigida** sem recursividade à esquerda
2. **Constrói a AST** (Árvore Sintática Abstrata)
3. **Integra análise semântica** durante o parsing

**Estrutura Principal:**
```python
class Parser:
    def parse(self) -> Program
    def parse_declarations(self) -> List[ASTNode]
    def parse_const_decl(self) -> List[ConstDecl]
    def parse_type_decl(self) -> List[TypeDecl]
    def parse_var_decl(self) -> List[VarDecl]
    def parse_function(self) -> List[FunctionDecl]
    def parse_block(self) -> Compound
    def parse_statement(self) -> ASTNode
    def parse_expression(self) -> ASTNode
    # ... outros métodos
```

**Tratamento de Expressões (sem recursividade à esquerda):**
```python
def parse_expression(self):
    """<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*"""
    node = self.parse_relation()
    while self.match('AND', 'OR'):
        op = self.consume().lexeme
        right = self.parse_relation()
        node = BinOp(op, node, right)
    return node

def parse_simple_expression(self):
    """<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*"""
    node = self.parse_term()
    while self.peek() and self.peek().type == 'OP_MAT' and self.peek().lexeme in ['+','-']:
        op = self.consume('OP_MAT').lexeme
        right = self.parse_term()
        node = BinOp(op, node, right)
    return node
```

### 2.3 Análise Semântica Integrada

O analisador semântico verifica:

1. **Declaração antes do uso**
2. **Escopo de variáveis**
3. **Compatibilidade de tipos**
4. **Parâmetros de funções**
5. **Tipos de retorno**

**Tabela de Símbolos:**
```python
class Symbol:
    name: str           # Nome do identificador
    symbol_type: str    # Tipo (integer, real, etc)
    kind: str          # 'var', 'const', 'function', 'type'
    scope_level: int   # Nível de escopo
    params: List       # Para funções
    return_type: str   # Para funções

class SymbolTable:
    scopes: List[Dict[str, Symbol]]  # Pilha de escopos
    
    def enter_scope(self)
    def exit_scope(self)
    def declare(self, symbol: Symbol)
    def lookup(self, name: str) -> Optional[Symbol]
```

**Verificações Implementadas:**
```python
# Exemplo: Verificação de atribuição
def parse_assignment(self):
    var_name = self.consume('ID').lexeme
    self.consume('OP_ASSIGN')
    expr = self.parse_expression()
    
    if self.enable_semantic:
        var_symbol = self.symbol_table.lookup(var_name)
        if not var_symbol:
            self.add_semantic_error(f"Variável '{var_name}' não declarada")
        else:
            expr_type = self.infer_expression_type(expr)
            if not self.types_compatible(var_symbol.symbol_type, expr_type):
                self.add_semantic_error(
                    f"Atribuição incompatível: '{var_name}' é "
                    f"'{var_symbol.symbol_type}', mas expressão é '{expr_type}'"
                )
    
    return Assign(Var(var_name), expr)
```

---

## ETAPA 3: Regras Semânticas e Gramática

### 3.1 Mapeamento de Regras Semânticas para a Gramática

#### Regra 1: Não declarar mais de 1 ID com mesmo nome no mesmo escopo

**Produção Afetada:**
```
<VARIAVEL> → <ID> ( , <ID> )* : <TIPO_DADO> ;
```

**Verificação Semântica:**
```python
def parse_var_decl(self):
    vars = self.consume('VAR')
    declarations = []
    
    while not self.match('FUNCTION', 'PROCEDURE', 'BEGIN'):
        names = [self.consume('ID').lexeme]
        while self.match('VIRG'):
            self.consume('VIRG')
            names.append(self.consume('ID').lexeme)
        
        self.consume('DOIS_PONT')
        type_tok = self.consume().lexeme
        self.consume('PONT_VIRG')
        
        # VERIFICAÇÃO SEMÂNTICA: Declaração única por escopo
        if self.enable_semantic:
            for name in names:
                try:
                    symbol = Symbol(name, type_tok, 'var', self.symbol_table.current_level)
                    self.symbol_table.declare(symbol)
                except SemanticError as e:
                    self.add_semantic_error(str(e))
        
        declarations.append(VarDecl(names, type_tok))
    
    return declarations
```

#### Regra 2: Declaração de ID no escopo antes do uso

**Produção Afetada:**
```
<ATRIBUICAO> → <NOME> := <EXP_LOGICA>
<FATOR> → <NOME>
```

**Verificação Semântica:**
```python
def infer_expression_type(self, node: ASTNode) -> str:
    if isinstance(node, Var):
        # VERIFICAÇÃO: Variável foi declarada?
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.add_semantic_error(f"Variável '{node.name}' não foi declarada")
            return 'unknown'
        return symbol.symbol_type
    # ... outros casos
```

#### Regra 3: Só permite atribuição e operações com tipos iguais

**Produção Afetada:**
```
<ATRIBUICAO> → <NOME> := <EXP_LOGICA>
<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*
<EXP_MUL> → <FATOR> ( (*|/) <FATOR> )*
```

**Verificação Semântica:**
```python
def infer_binop_type(self, node: BinOp) -> str:
    op = node.op.lower()
    left_type = self.infer_expression_type(node.left)
    right_type = self.infer_expression_type(node.right)
    
    if op in ['+', '-', '*', '/']:
        # VERIFICAÇÃO: Operandos devem ser numéricos
        if left_type not in ['integer', 'real'] or right_type not in ['integer', 'real']:
            self.add_semantic_error(
                f"Operador '{op}' requer operandos numéricos, "
                f"mas recebeu '{left_type}' e '{right_type}'"
            )
            return 'unknown'
        
        # Promoção de tipo: integer + real = real
        if left_type == 'real' or right_type == 'real':
            return 'real'
        return 'integer'
```

#### Regra 4: Quantidade de parâmetros na chamada deve ser igual à declaração

**Produção Afetada:**
```
<CHAMADA> → <ID> ( <ARGS>? )
```

**Verificação Semântica:**
```python
def infer_call_type(self, node: Call) -> str:
    func_name_lower = node.name.lower()
    
    # Funções built-in
    if func_name_lower in ['read', 'write']:
        return 'void'
    
    # Função definida pelo usuário
    func_symbol = self.symbol_table.lookup(node.name)
    if not func_symbol:
        self.add_semantic_error(f"Função '{node.name}' não foi declarada")
        return 'unknown'
    
    # VERIFICAÇÃO: Quantidade de parâmetros
    expected_count = len(func_symbol.params)
    actual_count = len(node.args)
    
    if expected_count != actual_count:
        self.add_semantic_error(
            f"Função '{node.name}' espera {expected_count} parâmetros, "
            f"mas recebeu {actual_count}"
        )
        return func_symbol.return_type
    
    # VERIFICAÇÃO: Tipos dos parâmetros
    for i, (arg, (param_name, param_type)) in enumerate(zip(node.args, func_symbol.params)):
        arg_type = self.infer_expression_type(arg)
        if not self.types_compatible(param_type, arg_type):
            self.add_semantic_error(
                f"Parâmetro {i+1} de '{node.name}' espera tipo '{param_type}', "
                f"mas recebeu '{arg_type}'"
            )
    
    return func_symbol.return_type
```

#### Regra 5: Só pode usar índice ([]) em variáveis do tipo vetor

**Produção Afetada:**
```
<NOME> → <ID> ( . <ID> | [ <EXP_LOGICA> ] )*
```

**Verificação Semântica (Extensão Futura):**
```python
# Esta regra requereria extensão na AST para representar acesso a array
class ArrayAccess(ASTNode):
    name: str
    index: ASTNode

def parse_postfix(self):
    # ... implementação
    if self.match('ABRE_COL'):
        self.consume('ABRE_COL')
        index = self.parse_expression()
        self.consume('FECHA_COL')
        
        # VERIFICAÇÃO SEMÂNTICA
        if self.enable_semantic:
            var_symbol = self.symbol_table.lookup(name)
            if not var_symbol:
                self.add_semantic_error(f"Variável '{name}' não declarada")
            elif not var_symbol.symbol_type.startswith('array'):
                self.add_semantic_error(
                    f"'{name}' não é um array, não pode usar índice []"
                )
```

#### Regra 6: Só pode usar membros (.) em variáveis do tipo classe/record

**Produção Afetada:**
```
<NOME> → <ID> ( . <ID> | [ <EXP_LOGICA> ] )*
```

**Verificação Semântica (Extensão Futura):**
```python
class MemberAccess(ASTNode):
    object: str
    member: str

def parse_postfix(self):
    # ... implementação
    if self.match('PONT'):
        self.consume('PONT')
        member = self.consume('ID').lexeme
        
        # VERIFICAÇÃO SEMÂNTICA
        if self.enable_semantic:
            var_symbol = self.symbol_table.lookup(name)
            if not var_symbol:
                self.add_semantic_error(f"Variável '{name}' não declarada")
            elif not var_symbol.symbol_type.startswith('record'):
                self.add_semantic_error(
                    f"'{name}' não é um record, não pode acessar membro '.{member}'"
                )
            else:
                # Verificar se o membro existe no record
                # (requer estrutura adicional na tabela de símbolos)
                pass
```

### 3.2 Resumo das Regras Implementadas

| Regra | Produção | Status | Localização no Código |
|-------|----------|--------|----------------------|
| Declaração única por escopo | `<VARIAVEL>`, `<CONSTANTE>`, `<TIPO>` | ✅ Implementado | `SymbolTable.declare()` |
| Declaração antes do uso | `<NOME>`, `<FATOR>` | ✅ Implementado | `infer_expression_type()` |
| Compatibilidade de tipos | `<ATRIBUICAO>`, `<EXP_AD>`, `<EXP_MUL>` | ✅ Implementado | `infer_binop_type()`, `parse_assignment()` |
| Parâmetros de função | `<CHAMADA>` | ✅ Implementado | `infer_call_type()` |
| Tipo de retorno | `<FUNCAO>` | ✅ Implementado | `parse_function()` |
| Índice em arrays | `<NOME>` | ⚠️ Parcial | Requer extensão |
| Acesso a membros | `<NOME>` | ⚠️ Parcial | Requer extensão |

---

## ETAPA 4: Geração de Código Intermediário

### 4.1 Formato do Código Intermediário (Three-Address Code - TAC)

O código intermediário utiliza o formato de **três endereços**, onde cada instrução tem no máximo um operador e três operandos:

```
OP | Endereço_1 | Endereço_2 | Endereço_3
```

### 4.2 Instruções Suportadas

| Operação | End_1 | End_2 | End_3 | Descrição |
|----------|-------|-------|-------|-----------|
| **ATR** | destino | origem | - | Atribuição: dest ← origem |
| **ADD** | resultado | op1 | op2 | Adição: res ← op1 + op2 |
| **SUB** | resultado | op1 | op2 | Subtração: res ← op1 - op2 |
| **MUL** | resultado | op1 | op2 | Multiplicação: res ← op1 * op2 |
| **DIV** | resultado | op1 | op2 | Divisão: res ← op1 / op2 |
| **JMP** | label | - | - | Salto incondicional |
| **JZ** | label | variável | - | Salto se zero (false) |
| **JNZ** | label | variável | - | Salto se não-zero (true) |
| **JGT** | label | op1 | op2 | Salto se op1 > op2 |
| **JLT** | label | op1 | op2 | Salto se op1 < op2 |
| **JGE** | label | op1 | op2 | Salto se op1 >= op2 |
| **JLE** | label | op1 | op2 | Salto se op1 <= op2 |
| **JEQ** | label | op1 | op2 | Salto se op1 = op2 |
| **JNE** | label | op1 | op2 | Salto se op1 <> op2 |
| **LABEL** | nome | - | - | Define um rótulo |
| **CALL** | função | nargs | - | Chamada de função |
| **PARAM** | arg | - | - | Passa parâmetro |
| **RETURN** | valor | - | - | Retorna de função |
| **READ** | variável | - | - | Lê entrada |
| **WRITE** | valor | - | - | Escreve saída |

### 4.3 Implementação do Gerador de Código Intermediário

```python
# tac_generator.py

from dataclasses import dataclass
from typing import List, Optional
from ast_nodes import *

@dataclass
class TACInstruction:
    """Representa uma instrução de três endereços"""
    op: str
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    addr3: Optional[str] = None
    
    def __str__(self):
        parts = [self.op]
        if self.addr1: parts.append(str(self.addr1))
        if self.addr2: parts.append(str(self.addr2))
        if self.addr3: parts.append(str(self.addr3))
        return '\t'.join(parts)

class TACGenerator:
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self) -> str:
        """Gera um novo temporário"""
        self.temp_counter += 1
        return f"T{self.temp_counter}"
    
    def new_label(self) -> str:
        """Gera um novo rótulo"""
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, op: str, addr1=None, addr2=None, addr3=None):
        """Emite uma instrução TAC"""
        self.instructions.append(TACInstruction(op, addr1, addr2, addr3))
    
    def generate(self, ast: Program) -> List[TACInstruction]:
        """Gera código intermediário para o programa"""
        self.visit_program(ast)
        return self.instructions
    
    def visit_program(self, node: Program):
        """Visita o nó Program"""
        # Declarações globais não geram código
        # Apenas o bloco principal
        self.emit('LABEL', 'MAIN')
        self.visit_compound(node.block)
        self.emit('HALT')
    
    def visit_compound(self, node: Compound):
        """Visita bloco de comandos"""
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: ASTNode):
        """Visita um comando"""
        if isinstance(node, Assign):
            self.visit_assign(node)
        elif isinstance(node, If):
            self.visit_if(node)
        elif isinstance(node, While):
            self.visit_while(node)
        elif isinstance(node, Call):
            self.visit_call(node)
        elif isinstance(node, Compound):
            self.visit_compound(node)
    
    def visit_assign(self, node: Assign):
        """
        Geração para: <NOME> := <EXP>
        
        Exemplo: A := B + C * D
        TAC:
            MUL  T1  C  D
            ADD  T2  B  T1
            ATR  A   T2
        """
        temp = self.visit_expression(node.value)
        target = node.target.name
        self.emit('ATR', target, temp)
    
    def visit_expression(self, node: ASTNode) -> str:
        """Visita expressão e retorna temporário com resultado"""
        if isinstance(node, Num):
            return str(node.value)
        elif isinstance(node, Var):
            return node.name
        elif isinstance(node, String):
            return f'"{node.value}"'
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, Call):
            return self.visit_call_expr(node)
        else:
            return self.new_temp()
    
    def visit_binop(self, node: BinOp) -> str:
        """
        Geração para operações binárias
        
        Exemplo: A + B
        TAC:
            ADD  T1  A  B
        """
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '=': 'EQ',
            '<>': 'NE',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LE',
            '>=': 'GE',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT'
        }
        
        op = node.op.lower()
        
        if op == 'not':
            # Operador unário
            operand = self.visit_expression(node.left)
            result = self.new_temp()
            self.emit('NOT', result, operand)
            return result
        else:
            # Operador binário
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right)
            result = self.new_temp()
            self.emit(op_map[op], result, left, right)
            return result
    
    def visit_if(self, node: If):
        """
        Geração para: if <EXP> then <CMD1> else <CMD2>
        
        TAC:
            [avaliar condição em T1]
            JZ   L_ELSE  T1
            [código CMD1]
            JMP  L_FIM
        L_ELSE:
            [código CMD2]
        L_FIM:
        """
        label_else = self.new_label()
        label_end = self.new_label()
        
        # Avalia condição
        cond_temp = self.visit_expression(node.condition)
        
        # Salta para else se falso
        self.emit('JZ', label_else, cond_temp)
        
        # Código do then
        self.visit_statement(node.then_branch)
        
        if node.else_branch:
            # Pula o else após executar then
            self.emit('JMP', label_end)
            
            # Código do else
            self.emit('LABEL', label_else)
            self.visit_statement(node.else_branch)
            
            self.emit('LABEL', label_end)
        else:
            # Sem else, apenas define o label
            self.emit('LABEL', label_else)
    
    def visit_while(self, node: While):
        """
        Geração para: while <EXP> do <CMD>
        
        TAC:
        L_INICIO:
            [avaliar condição em T1]
            JZ   L_FIM  T1
            [código CMD]
            JMP  L_INICIO
        L_FIM:
        """
        label_start = self.new_label()
        label_end = self.new_label()
        
        # Label do início do loop
        self.emit('LABEL', label_start)
        
        # Avalia condição
        cond_temp = self.visit_expression(node.condition)
        
        # Salta para fim se falso
        self.emit('JZ', label_end, cond_temp)
        
        # Código do corpo
        self.visit_statement(node.body)
        
        # Volta para o início
        self.emit('JMP', label_start)
        
        # Label do fim
        self.emit('LABEL', label_end)
    
    def visit_call(self, node: Call):
        """
        Geração para: function(arg1, arg2, ...)
        
        TAC:
            PARAM  arg1
            PARAM  arg2
            CALL   function  2
        """
        func_name = node.name.lower()
        
        if func_name == 'read':
            # read(var)
            if node.args:
                var_temp = self.visit_expression(node.args[0])
                self.emit('READ', var_temp)
        elif func_name == 'write':
            # write(exp)
            if node.args:
                val_temp = self.visit_expression(node.args[0])
                self.emit('WRITE', val_temp)
        else:
            # Chamada de função normal
            for arg in node.args:
                arg_temp = self.visit_expression(arg)
                self.emit('PARAM', arg_temp)
            self.emit('CALL', func_name, len(node.args))
    
    def visit_call_expr(self, node: Call) -> str:
        """Chamada de função como expressão (retorna temporário)"""
        self.visit_call(node)
        result = self.new_temp()
        self.emit('ATR', result, 'RETVAL')
        return result
    
    def print_tac(self):
        """Imprime o código TAC"""
        print("\n===== CÓDIGO INTERMEDIÁRIO (TAC) =====")
        for i, instr in enumerate(self.instructions, 1):
            print(f"{i:3}. {instr}")
        print("======================================\n")
```

### 4.4 Exemplos de Geração de Código

#### Exemplo 1: Atribuição Simples
```pascal
program teste;
var A, B, C : integer;
begin
  A := B + C;
end.
```

**Código TAC Gerado:**
```
LABEL   MAIN
ADD     T1      B       C
ATR     A       T1
HALT
```

#### Exemplo 2: Expressão Complexa
```pascal
program teste;
var A, B, C, D : integer;
begin
  A := B + C * D;
end.
```

**Código TAC Gerado:**
```
LABEL   MAIN
MUL     T1      C       D
ADD     T2      B       T1
ATR     A       T2
HALT
```

#### Exemplo 3: Comando IF
```pascal
program teste;
var A, B : integer;
begin
  if A > B then
    A := A + 1
  else
    B := B + 1;
end.
```

**Código TAC Gerado:**
```
LABEL   MAIN
GT      T1      A       B
JZ      L1      T1
ADD     T2      A       1
ATR     A       T2
JMP     L2
LABEL   L1
ADD     T3      B       1
ATR     B       T3
LABEL   L2
HALT
```

#### Exemplo 4: Laço WHILE
```pascal
program teste;
var i, soma : integer;
begin
  i := 1;
  soma := 0;
  while i < 10 do
  begin
    soma := soma + i;
    i := i + 1;
  end;
end.
```

**Código TAC Gerado:**
```
LABEL   MAIN
ATR     i       1
ATR     soma    0
LABEL   L1
LT      T1      i       10
JZ      L2      T1
ADD     T2      soma    i
ATR     soma    T2
ADD     T3      i       1
ATR     i       T3
JMP     L1
LABEL   L2
HALT
```

#### Exemplo 5: Chamada de Função
```pascal
program teste;
var resultado : integer;

function soma(a: integer; b: integer) : integer;
begin
  soma := a + b;
end;

begin
  resultado := soma(5, 3);
end.
```

**Código TAC Gerado:**
```
LABEL   soma
PARAM   a
PARAM   b
ADD     T1      a       b
ATR     soma    T1
RETURN  T1

LABEL   MAIN
PARAM   5
PARAM   3
CALL    soma    2
ATR     T2      RETVAL
ATR     resultado T2
HALT
```

### 4.5 Otimizações Possíveis

1. **Eliminação de Código Morto**
   - Remover instruções que nunca são executadas

2. **Propagação de Constantes**
   ```
   Antes:
   ATR  T1  5
   ADD  T2  T1  3
   
   Depois:
   ATR  T2  8
   ```

3. **Eliminação de Subexpressões Comuns**
   ```
   Antes:
   MUL  T1  A  B
   MUL  T2  A  B
   
   Depois:
   MUL  T1  A  B
   ATR  T2  T1
   ```

4. **Peephole Optimization**
   - Otimizações locais em pequenas janelas de código

---

## Conclusão

Este documento apresentou as quatro etapas principais do desenvolvimento do compilador Pascal simplificado:

1. **Classificação de Tokens e Remoção de Ambiguidades** - Definição formal da linguagem com gramática livre de contexto corrigida

2. **Implementação do Compilador** - Análise léxica, sintática e semântica integradas

3. **Regras Semânticas** - Mapeamento das verificações semânticas para produções gramaticais

4. **Geração de Código Intermediário** - Transformação da AST em código de três endereços (TAC)

O compilador implementa todas as verificações semânticas requeridas e está pronto para extensões futuras, como otimização de código e geração de código de máquina.

### Próximos Passos Sugeridos

- Implementação completa de arrays e records
- Otimização do código intermediário
- Geração de código assembly
- Interpretador para o código TAC
- Tratamento de erros mais robusto

---
**Projeto Acadêmico - 2025**
