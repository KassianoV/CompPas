from lexer import Lexer, Token
from ast_nodes import *
from typing import List

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = list(tokens)
        self.pos = 0

    # utilitários
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

    # parser principal
    def parse(self):
        # program ID ; [declarations] begin ... end .
        self.consume('PROGRAM')
        name_tok = self.consume('ID')
        self.consume('PONT_VIRG')
        var_decls = self.parse_declarations()  # optional
        block = self.parse_block()
        self.consume('PONT')  # ponto final
        return Program(name_tok.lexeme, var_decls, block)

    def parse_declarations(self):
        decls = []
        if self.match('VAR'):
            self.consume('VAR')
            # múltiplas declarações até encontrar BEGIN
            while not self.match('BEGIN'):
                # id (, id)* : type ;
                names = []
                names.append(self.consume('ID').lexeme)
                while self.match('VIRG'):
                    self.consume('VIRG')
                    names.append(self.consume('ID').lexeme)
                self.consume('DOIS_PONT')
                type_name = self.consume('ID').lexeme
                self.consume('PONT_VIRG')
                decls.append(VarDecl(names, type_name))
        return decls

    def parse_block(self):
        self.consume('BEGIN')
        stmts = []
        # aceitar zero ou mais statements até END
        while not self.match('END'):
            stmt = self.parse_statement()
            stmts.append(stmt)
            # ponto e vírgula opcional entre statements
            if self.match('PONT_VIRG'):
                self.consume('PONT_VIRG')
            else:
                # se próximo token começar um statement sem ; (p.ex. END), ok; caso contrário, continue
                pass
        self.consume('END')
        return Compound(stmts)

    def parse_statement(self):
        tok = self.peek()
        if not tok:
            raise ParserError('Esperava comando, mas encontrou EOF')

        if tok.type == 'ID':
            # pode ser atribuição ou chamada de função (se seguido por '(')
            # olhe adiante
            nxt = self.tokens[self.pos + 1] if (self.pos + 1) < len(self.tokens) else None
            if nxt and nxt.type == 'OP_ASSIGN':
                return self.parse_assignment()
            elif nxt and nxt.type == 'ABRE_PARENT':
                return self.parse_call_statement()
            else:
                # se não for nenhum dos dois, assume erro
                return self.parse_assignment()  # tentamos interpretar como atribuição (vai falhar se não)
        elif tok.type == 'IF':
            return self.parse_if()
        elif tok.type == 'WHILE':
            return self.parse_while()
        elif tok.type == 'BEGIN':
            return self.parse_block()
        elif tok.type in ('READ', 'WRITE'):
            return self.parse_call_statement()
        else:
            raise ParserError(f'Comando inesperado: {tok.lexeme}')

    # comandos
    def parse_assignment(self):
        var_name = self.consume('ID').lexeme
        self.consume('OP_ASSIGN')
        expr = self.parse_expression()
        return Assign(Var(var_name), expr)

    def parse_if(self):
        self.consume('IF')
        self.consume('ABRE_PARENT')
        cond = self.parse_expression()
        self.consume('FECHA_PARENT')
        self.consume('THEN')
        then_stmt = self.parse_statement()
        else_stmt = None
        if self.match('ELSE'):
            self.consume('ELSE')
            else_stmt = self.parse_statement()
        return If(cond, then_stmt, else_stmt)

    def parse_while(self):
        self.consume('WHILE')
        self.consume('ABRE_PARENT')
        cond = self.parse_expression()
        self.consume('FECHA_PARENT')
        self.consume('DO')
        body = self.parse_statement()
        return While(cond, body)

    def parse_call_statement(self):
        # chamadas como: read(x), write(a+b), foo(a, b)
        # aceitar READ/WRITE como keywords também
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

    # expressões (removendo recursão à esquerda)
    def parse_expression(self):
        node = self.parse_simple_expression()
        tok = self.peek()
        if tok and tok.type == 'OP_REL':
            op = self.consume('OP_REL').lexeme
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
        if not tok:
            raise ParserError('Fator inesperado: EOF')
        if tok.type == 'CONST_NUM':
            self.consume('CONST_NUM')
            # se inteiro sem '.', converte para int
            if '.' in tok.lexeme:
                return Num(float(tok.lexeme))
            else:
                return Num(int(tok.lexeme))
        elif tok.type == 'CONST_STR':
            self.consume('CONST_STR')
            # manter com aspas
            return Num(tok.lexeme)
        elif tok.type == 'ID':
            # pode ser var ou chamada de função
            nxt = self.tokens[self.pos + 1] if (self.pos + 1) < len(self.tokens) else None
            if nxt and nxt.type == 'ABRE_PARENT':
                # chamada de função dentro de expressão
                return self.parse_call_expression()
            else:
                self.consume('ID')
                return Var(tok.lexeme)
        elif tok.type == 'ABRE_PARENT':
            self.consume('ABRE_PARENT')
            expr = self.parse_expression()
            self.consume('FECHA_PARENT')
            return expr
        else:
            raise ParserError(f'Fator inesperado: {tok.lexeme}')

    def parse_call_expression(self):
        # semântica de função usada em expressão: foo(a, b)
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

