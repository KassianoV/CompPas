import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

        # Regras de tokens — ordem importa
        self.token_specs = [
            ('COMMENT', r'\{#[\s\S]*?#\}'),

            # Literais
            ('CONST_STR', r'"(?:\\.|[^"\\])*"'),
            ('CONST_NUM', r'\d+(?:\.\d+)?'),

            # Operadores relacionais e lógicos
            ('OP_REL', r'(<=|>=|<>|<|>|=)'),
            ('OP_ASSIGN', r':='),
            ('OP_MAT', r'[+\-*/]'),

            # Pontuação
            ('PONT_VIRG', r';'),
            ('VIRG', r','),
            ('DOIS_PONT', r':'),
            ('PONT', r'\.'),
            ('ABRE_PARENT', r'\('),
            ('FECHA_PARENT', r'\)'),
            ('ABRE_COL', r'\['),
            ('FECHA_COL', r'\]'),

            # Identificadores
            ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),

            # Espaços e nova linha
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t\r]+'),

            # Qualquer outro caractere
            ('MISMATCH', r'.'),
        ]

        parts = [f'(?P<{name}>{pattern})' for name, pattern in self.token_specs]
        self.master_re = re.compile('|'.join(parts))

        # Palavras reservadas da gramática Pascal simplificada
        self.keywords = {
            # Estrutura
            'program','begin','end','type','var','const','function','procedure',
            # Controle de fluxo
            'if','then','else','while','do',
            # Estruturas de dados
            'array','of','record',
            # Entrada e saída
            'read','write',
            # Booleanos
            'true','false',
            # Operadores lógicos
            'and','or','not',
            # Tipos básicos
            'integer','real','boolean','string'
        }

    def tokenize(self):
        for mo in self.master_re.finditer(self.source):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'NEWLINE':
                self.line += 1
                self.col = 1
                continue
            elif kind == 'SKIP':
                self.col += len(value)
                continue
            elif kind == 'COMMENT':
                self.line += value.count('\n')
                if '\n' in value:
                    last_line = value.split('\n')[-1]
                    self.col = len(last_line) + 1
                else:
                    self.col += len(value)
                continue
            elif kind == 'ID' and value.lower() in self.keywords:
                kind = value.upper()
            elif kind == 'MISMATCH':
                raise LexerError(f'Caractere inesperado {value!r} na linha {self.line}, coluna {self.col}')

            token = Token(kind, value, self.line, self.col)
            yield token
            self.col += len(value)
