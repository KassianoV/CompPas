from lexer import Token
from ast_nodes import *
from typing import List, Dict, Optional

class ParserError(Exception):
    pass

class SemanticError(Exception):
    pass

class Symbol:
    """Representa um símbolo na tabela de símbolos"""
    def __init__(self, name: str, symbol_type: str, kind: str, scope_level: int):
        self.name = name
        self.symbol_type = symbol_type  # tipo do símbolo (integer, real, etc)
        self.kind = kind  # 'var', 'const', 'function', 'type', 'param'
        self.scope_level = scope_level
        self.params = []  # para funções: lista de (nome, tipo)
        self.return_type = None  # para funções

class SymbolTable:
    """Tabela de símbolos com suporte a escopos aninhados"""
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]
        self.current_level = 0
        self._add_builtin_types()
    
    def _add_builtin_types(self):
        """Adiciona tipos primitivos à tabela"""
        for type_name in ['integer', 'real', 'boolean', 'string']:
            self.scopes[0][type_name] = Symbol(
                name=type_name,
                symbol_type=type_name,
                kind='type',
                scope_level=0
            )
    
    def enter_scope(self):
        """Entra em um novo escopo"""
        self.current_level += 1
        self.scopes.append({})
    
    def exit_scope(self):
        """Sai do escopo atual"""
        if self.current_level > 0:
            self.scopes.pop()
            self.current_level -= 1
    
    def declare(self, symbol: Symbol):
        """Declara um símbolo no escopo atual"""
        name_lower = symbol.name.lower()
        
        if name_lower in self.scopes[self.current_level]:
            raise SemanticError(
                f"Erro Semântico: Identificador '{symbol.name}' já foi declarado neste escopo"
            )
        
        symbol.scope_level = self.current_level
        self.scopes[self.current_level][name_lower] = symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Busca um símbolo em todos os escopos"""
        name_lower = name.lower()
        for i in range(self.current_level, -1, -1):
            if name_lower in self.scopes[i]:
                return self.scopes[i][name_lower]
        return None
    
    def resolve_type(self, type_name: str) -> str:
        """Resolve um tipo customizado para seu tipo base"""
        symbol = self.lookup(type_name)
        if not symbol or symbol.kind != 'type':
            return type_name
        if symbol.symbol_type == type_name:
            return type_name
        return self.resolve_type(symbol.symbol_type)


class Parser:
    def __init__(self, tokens: List[Token], enable_semantic=True):
        self.tokens = list(tokens)
        self.pos = 0
        self.enable_semantic = enable_semantic
        
        # Análise Semântica
        self.symbol_table = SymbolTable()
        self.semantic_errors = []
        self.current_function = None

    # ======== Funções utilitárias ========
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        tok = self.peek()
        if not tok:
            raise ParserError('Fim inesperado da entrada.')
        if expected_type and tok.type != expected_type:
            raise ParserError(f'Esperado token {expected_type}, mas encontrado {tok.type} ({tok.lexeme})')
        if expected_value and tok.lexeme.lower() != expected_value.lower():
            raise ParserError(f'Esperado {expected_value}, mas encontrado {tok.lexeme}')
        self.pos += 1
        return tok

    def match(self, *token_types):
        tok = self.peek()
        if tok and tok.type in token_types:
            return True
        return False
    
    def add_semantic_error(self, message: str):
        """Adiciona erro semântico à lista"""
        if self.enable_semantic:
            self.semantic_errors.append(message)
    
    def check_semantic_errors(self):
        """Verifica se há erros semânticos e lança exceção"""
        if self.enable_semantic and self.semantic_errors:
            error_msg = "\n".join(self.semantic_errors)
            raise SemanticError(f"Erros semânticos encontrados:\n{error_msg}")

    # ======== Verificações Semânticas ========
    
    def types_compatible(self, type1: str, type2: str) -> bool:
        """Verifica se dois tipos são compatíveis"""
        if type1 == 'unknown' or type2 == 'unknown':
            return True
        
        type1_lower = type1.lower()
        type2_lower = type2.lower()
        
        if type1_lower == type2_lower:
            return True
        
        # Integer pode ser promovido para real
        if (type1_lower == 'real' and type2_lower == 'integer') or \
           (type1_lower == 'integer' and type2_lower == 'real'):
            return True
        
        # Resolve tipos customizados
        base1 = self.symbol_table.resolve_type(type1)
        base2 = self.symbol_table.resolve_type(type2)
        return base1.lower() == base2.lower()

    def infer_expression_type(self, node: ASTNode) -> str:
        """Infere o tipo de uma expressão"""
        if isinstance(node, Num):
            return 'integer' if isinstance(node.value, int) else 'real'
        elif isinstance(node, String):
            return 'string'
        elif isinstance(node, Var):
            symbol = self.symbol_table.lookup(node.name)
            if not symbol:
                self.add_semantic_error(f"Erro: Variável '{node.name}' não foi declarada")
                return 'unknown'
            return symbol.symbol_type
        elif isinstance(node, BinOp):
            return self.infer_binop_type(node)
        elif isinstance(node, Call):
            return self.infer_call_type(node)
        return 'unknown'
    
    def infer_binop_type(self, node: BinOp) -> str:
        """Infere o tipo de uma operação binária"""
        op = node.op.lower()
        
        if op == 'not':
            operand_type = self.infer_expression_type(node.left)
            if operand_type != 'boolean':
                self.add_semantic_error(
                    f"Erro: Operador 'not' requer operando booleano, mas recebeu '{operand_type}'"
                )
            return 'boolean'
        
        left_type = self.infer_expression_type(node.left)
        right_type = self.infer_expression_type(node.right)
        
        if op in ['+', '-', '*', '/']:
            if left_type not in ['integer', 'real'] or right_type not in ['integer', 'real']:
                self.add_semantic_error(
                    f"Erro: Operador '{op}' requer operandos numéricos, mas recebeu '{left_type}' e '{right_type}'"
                )
                return 'unknown'
            if left_type == 'real' or right_type == 'real':
                return 'real'
            return 'integer'
        
        elif op in ['=', '<>', '<', '>', '<=', '>=']:
            if not self.types_compatible(left_type, right_type):
                self.add_semantic_error(
                    f"Erro: Operador '{op}' requer operandos do mesmo tipo, mas recebeu '{left_type}' e '{right_type}'"
                )
            return 'boolean'
        
        elif op in ['and', 'or']:
            if left_type != 'boolean' or right_type != 'boolean':
                self.add_semantic_error(
                    f"Erro: Operador '{op}' requer operandos booleanos, mas recebeu '{left_type}' e '{right_type}'"
                )
            return 'boolean'
        
        return 'unknown'
    
    def infer_call_type(self, node: Call) -> str:
        """Infere o tipo de uma chamada de função"""
        func_name_lower = node.name.lower()
        
        if func_name_lower in ['read', 'write']:
            for arg in node.args:
                self.infer_expression_type(arg)
            return 'void'
        
        func_symbol = self.symbol_table.lookup(node.name)
        if not func_symbol:
            self.add_semantic_error(f"Erro: Função '{node.name}' não foi declarada")
            return 'unknown'
        
        if func_symbol.kind != 'function':
            self.add_semantic_error(f"Erro: '{node.name}' não é uma função")
            return 'unknown'
        
        expected_params = len(func_symbol.params)
        actual_params = len(node.args)
        
        if expected_params != actual_params:
            self.add_semantic_error(
                f"Erro: Função '{node.name}' espera {expected_params} parâmetro(s), mas recebeu {actual_params}"
            )
            return func_symbol.return_type
        
        for i, arg in enumerate(node.args):
            arg_type = self.infer_expression_type(arg)
            expected_type = func_symbol.params[i][1]
            
            if not self.types_compatible(expected_type, arg_type):
                self.add_semantic_error(
                    f"Erro: Parâmetro {i+1} da função '{node.name}' espera tipo '{expected_type}', mas recebeu '{arg_type}'"
                )
        
        return func_symbol.return_type

    # ======== Ponto de entrada ========
    def parse(self):
        self.consume('PROGRAM')
        name_tok = self.consume('ID')
        self.consume('PONT_VIRG')

        decls = self.parse_declarations()
        block = self.parse_block()
        self.consume('PONT')
        
        # Verifica erros semânticos ao final
        self.check_semantic_errors()

        return Program(name_tok.lexeme, decls, block)

    # ======== Declarações ========
    def parse_declarations(self):
        decls = []
        while self.match('CONST', 'TYPE', 'VAR', 'FUNCTION'):
            if self.match('CONST'):
                decls += self.parse_const_section()
            elif self.match('TYPE'):
                decls += self.parse_type_section()
            elif self.match('VAR'):
                decls += self.parse_var_section()
            elif self.match('FUNCTION'):
                decls += self.parse_function_section()
        return decls

    def parse_const_section(self):
        consts = []
        self.consume('CONST')
        while not self.match('TYPE', 'VAR', 'FUNCTION', 'BEGIN'):
            name = self.consume('ID').lexeme
            self.consume('OP_ASSIGN')
            value = self.parse_expression()
            self.consume('PONT_VIRG')
            
            # Semântica: declara constante
            if self.enable_semantic:
                expr_type = self.infer_expression_type(value)
                symbol = Symbol(name, expr_type, 'const', self.symbol_table.current_level)
                try:
                    self.symbol_table.declare(symbol)
                except SemanticError as e:
                    self.add_semantic_error(str(e))
            
            consts.append(ConstDecl(name, value))
        return consts

    def parse_type_section(self):
        types = []
        self.consume('TYPE')
        while not self.match('VAR', 'FUNCTION', 'BEGIN'):
            name = self.consume('ID').lexeme
            self.consume('OP_REL', '=')

            if self.match('ID', 'INTEGER', 'REAL', 'BOOLEAN', 'STRING'):
                definition = self.consume().lexeme
            else:
                raise ParserError(f'Definição de tipo inválida: {self.peek().lexeme}')

            self.consume('PONT_VIRG')
            
            # Semântica: verifica tipo base e declara novo tipo
            if self.enable_semantic:
                base_type = self.symbol_table.lookup(definition)
                if not base_type or base_type.kind != 'type':
                    self.add_semantic_error(f"Erro: Tipo '{definition}' não foi declarado")
                else:
                    symbol = Symbol(name, definition, 'type', self.symbol_table.current_level)
                    try:
                        self.symbol_table.declare(symbol)
                    except SemanticError as e:
                        self.add_semantic_error(str(e))
            
            types.append(TypeDecl(name, definition))
        return types

    def parse_var_section(self):
        vars = []
        self.consume('VAR')
        while not self.match('BEGIN', 'FUNCTION'):
            names = [self.consume('ID').lexeme]
            while self.match('VIRG'):
                self.consume('VIRG')
                names.append(self.consume('ID').lexeme)
            self.consume('DOIS_PONT')

            if self.match('ID', 'INTEGER', 'REAL', 'BOOLEAN', 'STRING'):
                type_tok = self.consume().lexeme
            else:
                raise ParserError(f'Tipo inválido: {self.peek().lexeme}')
            self.consume('PONT_VIRG')
            
            # Semântica: verifica tipo e declara variáveis
            if self.enable_semantic:
                type_symbol = self.symbol_table.lookup(type_tok)
                if not type_symbol or type_symbol.kind != 'type':
                    self.add_semantic_error(f"Erro: Tipo '{type_tok}' não foi declarado")
                else:
                    for var_name in names:
                        symbol = Symbol(var_name, type_tok, 'var', self.symbol_table.current_level)
                        try:
                            self.symbol_table.declare(symbol)
                        except SemanticError as e:
                            self.add_semantic_error(str(e))
            
            vars.append(VarDecl(names, type_tok))
        return vars

    def parse_function_section(self):
        self.consume('FUNCTION')
        name = self.consume('ID').lexeme
        self.consume('ABRE_PARENT')
        params = []
        if not self.match('FECHA_PARENT'):
            params.append(self.parse_param())
            while self.match('PONT_VIRG'):
                self.consume('PONT_VIRG')
                params.append(self.parse_param())
        self.consume('FECHA_PARENT')
        self.consume('DOIS_PONT')
        return_type = self.consume().lexeme
        self.consume('PONT_VIRG')
        
        # Semântica: declara função no escopo atual
        if self.enable_semantic:
            return_type_symbol = self.symbol_table.lookup(return_type)
            if not return_type_symbol or return_type_symbol.kind != 'type':
                self.add_semantic_error(f"Erro: Tipo de retorno '{return_type}' não foi declarado")
            
            func_symbol = Symbol(name, return_type, 'function', self.symbol_table.current_level)
            func_symbol.return_type = return_type
            
            for param in params:
                for param_name in param.names:
                    func_symbol.params.append((param_name, param.type_name))
            
            try:
                self.symbol_table.declare(func_symbol)
            except SemanticError as e:
                self.add_semantic_error(str(e))

        local_vars = []
        
        # Entra no escopo da função
        if self.enable_semantic:
            self.symbol_table.enter_scope()
            self.current_function = name
            
            # Declara parâmetros no escopo da função
            for param in params:
                param_type_symbol = self.symbol_table.lookup(param.type_name)
                if not param_type_symbol or param_type_symbol.kind != 'type':
                    self.add_semantic_error(f"Erro: Tipo '{param.type_name}' não foi declarado")
                else:
                    for param_name in param.names:
                        param_symbol = Symbol(param_name, param.type_name, 'param', 
                                            self.symbol_table.current_level)
                        try:
                            self.symbol_table.declare(param_symbol)
                        except SemanticError as e:
                            self.add_semantic_error(str(e))
        
        if self.match('VAR'):
            local_vars = self.parse_var_section()

        block = self.parse_block()
        self.consume('PONT_VIRG')
        
        # Sai do escopo da função
        if self.enable_semantic:
            self.symbol_table.exit_scope()
            self.current_function = None
        
        return [FunctionDecl(name, params, return_type, local_vars, block)]

    def parse_param(self):
        names = [self.consume('ID').lexeme]
        while self.match('VIRG'):
            self.consume('VIRG')
            names.append(self.consume('ID').lexeme)
        self.consume('DOIS_PONT')
        if self.match('ID', 'INTEGER', 'REAL', 'BOOLEAN', 'STRING'):
            type_tok = self.consume().lexeme
        else:
            raise ParserError(f'Tipo inválido em parâmetro: {self.peek().lexeme}')
        return VarDecl(names, type_tok)

    # ======== Blocos e comandos ========
    def parse_block(self):
        self.consume('BEGIN')
        stmts = []
        while not self.match('END'):
            stmts.append(self.parse_statement())
            if self.match('PONT_VIRG'):
                self.consume('PONT_VIRG')
        self.consume('END')
        return Compound(stmts)

    def parse_statement(self):
        tok = self.peek()
        if not tok:
            raise ParserError('Esperava comando, mas encontrou EOF')

        if tok.type == 'ID':
            nxt = self.tokens[self.pos + 1] if (self.pos + 1) < len(self.tokens) else None
            if nxt and nxt.type == 'OP_ASSIGN':
                return self.parse_assignment()
            elif nxt and nxt.type == 'ABRE_PARENT':
                return self.parse_call_statement()
        elif tok.type == 'IF':
            return self.parse_if()
        elif tok.type == 'WHILE':
            return self.parse_while()
        elif tok.type == 'BEGIN':
            return self.parse_block()
        elif tok.type in ('READ', 'WRITE'):
            return self.parse_call_statement()
        raise ParserError(f'Comando inesperado: {tok.lexeme}')

    def parse_assignment(self):
        var_name = self.consume('ID').lexeme
        self.consume('OP_ASSIGN')
        expr = self.parse_expression()
        
        # Semântica: verifica atribuição
        if self.enable_semantic:
            var_symbol = self.symbol_table.lookup(var_name)
            if not var_symbol:
                self.add_semantic_error(f"Erro: Variável '{var_name}' não foi declarada")
            elif var_symbol.kind == 'const':
                self.add_semantic_error(
                    f"Erro: Não é possível atribuir valor a constante '{var_name}'"
                )
            else:
                expr_type = self.infer_expression_type(expr)
                if not self.types_compatible(var_symbol.symbol_type, expr_type):
                    self.add_semantic_error(
                        f"Erro: Atribuição incompatível. '{var_name}' é do tipo "
                        f"'{var_symbol.symbol_type}', mas expressão é do tipo '{expr_type}'"
                    )
        
        return Assign(Var(var_name), expr)

    def parse_if(self):
        self.consume('IF')
        cond = self.parse_expression()
        
        # Semântica: verifica condição
        if self.enable_semantic:
            cond_type = self.infer_expression_type(cond)
            if cond_type != 'boolean':
                self.add_semantic_error(
                    f"Erro: Condição do 'if' deve ser booleana, mas é '{cond_type}'"
                )
        
        self.consume('THEN')
        then_stmt = self.parse_statement()
        else_stmt = None
        if self.match('ELSE'):
            self.consume('ELSE')
            else_stmt = self.parse_statement()
        return If(cond, then_stmt, else_stmt)

    def parse_while(self):
        self.consume('WHILE')
        cond = self.parse_expression()
        
        # Semântica: verifica condição
        if self.enable_semantic:
            cond_type = self.infer_expression_type(cond)
            if cond_type != 'boolean':
                self.add_semantic_error(
                    f"Erro: Condição do 'while' deve ser booleana, mas é '{cond_type}'"
                )
        
        self.consume('DO')
        body = self.parse_statement()
        return While(cond, body)

    def parse_call_statement(self):
        if self.match('READ') or self.match('WRITE'):
            name = self.consume().lexeme
        else:
            name = self.consume('ID').lexeme
        self.consume('ABRE_PARENT')
        args = []
        if not self.match('FECHA_PARENT'):
            args.append(self.parse_expression())
            while self.match('VIRG'):
                self.consume('VIRG')
                args.append(self.parse_expression())
        self.consume('FECHA_PARENT')
        
        call_node = Call(name, args)
        
        # Semântica: verifica chamada
        if self.enable_semantic:
            self.infer_call_type(call_node)
        
        return call_node

    # ======== Expressões ========
    def parse_expression(self):
        node = self.parse_relation()
        while self.match('AND', 'OR'):
            op = self.consume().lexeme
            right = self.parse_relation()
            node = BinOp(op, node, right)
        return node

    def parse_relation(self):
        node = self.parse_simple_expression()
        if self.match('OP_REL'):
            op = self.consume().lexeme
            right = self.parse_simple_expression()
            node = BinOp(op, node, right)
        return node

    def parse_simple_expression(self):
        node = self.parse_term()
        while True:
            tok = self.peek()
            if tok and tok.type == 'OP_MAT' and tok.lexeme in ['+','-']:
                op = self.consume('OP_MAT').lexeme
                right = self.parse_term()
                node = BinOp(op, node, right)
            else:
                break
        return node

    def parse_term(self):
        node = self.parse_factor()
        while True:
            tok = self.peek()
            if tok and tok.type == 'OP_MAT' and tok.lexeme in ['*','/']:
                op = self.consume('OP_MAT').lexeme
                right = self.parse_factor()
                node = BinOp(op, node, right)
            else:
                break
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok.type == 'CONST_STR':
            self.consume('CONST_STR')
            return String(tok.lexeme[1:-1]) 
        if tok.type == 'CONST_NUM':
            self.consume('CONST_NUM')
            return Num(float(tok.lexeme) if '.' in tok.lexeme else int(tok.lexeme))
        elif tok.type == 'ID':
            nxt = self.tokens[self.pos + 1] if (self.pos + 1) < len(self.tokens) else None
            if nxt and nxt.type == 'ABRE_PARENT':
                return self.parse_call_expression()
            self.consume('ID')
            return Var(tok.lexeme)
        elif tok.type == 'ABRE_PARENT':
            self.consume('ABRE_PARENT')
            expr = self.parse_expression()
            self.consume('FECHA_PARENT')
            return expr
        elif tok.type == 'NOT':
            self.consume('NOT')
            expr = self.parse_factor()
            return BinOp('not', expr, None)
        raise ParserError(f'Fator inesperado: {tok.lexeme}')

    def parse_call_expression(self):
        name = self.consume('ID').lexeme
        self.consume('ABRE_PARENT')
        args = []
        if not self.match('FECHA_PARENT'):
            args.append(self.parse_expression())
            while self.match('VIRG'):
                self.consume('VIRG')
                args.append(self.parse_expression())
        self.consume('FECHA_PARENT')
        
        call_node = Call(name, args)
        
        # Semântica: verifica chamada
        if self.enable_semantic:
            self.infer_call_type(call_node)
        
        return call_node