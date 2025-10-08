from lexer import Token
from ast_nodes import *
from typing import List

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = list(tokens)
        self.pos = 0

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

    # ======== Ponto de entrada ========
    def parse(self):
        self.consume('PROGRAM')
        name_tok = self.consume('ID')
        self.consume('PONT_VIRG')

        decls = self.parse_declarations()
        block = self.parse_block()
        self.consume('PONT')

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
            consts.append(ConstDecl(name, value))
        return consts

    def parse_type_section(self):
        types = []
        self.consume('TYPE')
        while not self.match('VAR', 'FUNCTION', 'BEGIN'):
            name = self.consume('ID').lexeme
            self.consume('OP_REL', '=')

            # CORREÇÃO: Aceita um ID ou um tipo primitivo
            if self.match('ID', 'INTEGER', 'REAL', 'BOOLEAN', 'STRING'):
                definition = self.consume().lexeme
            else:
                raise ParserError(f'Definição de tipo inválida: {self.peek().lexeme}')

            self.consume('PONT_VIRG')
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

        local_vars = []
        if self.match('VAR'):
            local_vars = self.parse_var_section()

        block = self.parse_block()
        self.consume('PONT_VIRG')
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
        return Assign(Var(var_name), expr)

    def parse_if(self):
        self.consume('IF')
        cond = self.parse_expression()
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
        return Call(name, args)

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
            return String(tok.lexeme[1:-1])  # Remove as aspas
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
        return Call(name, args)
