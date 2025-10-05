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

        # ordem importa: padrões mais longos / específicos primeiro
        self.token_specs = [
            # Comentários no formato {# ... #} (multi-linha)
            ('COMMENT', r'\{#[\s\S]*?#\}'),

            # Literais
            ('CONST_STR', r'"[^"\\]*"'),
            ('CONST_NUM', r'\d+(?:\.\d+)?'),

            # Operadores relacionais (colocar antes de tokens simples)
            ('OP_REL', r'(<=|>=|<>|<|>|=)'),

            # Atribuição
            ('OP_ASSIGN', r':='),

            # Operadores aritméticos
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

            # Identificador (underscores permitidos)
            ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),

            # Espaços e nova linha
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t\r]+'),

            # Qualquer outro caractere (erro)
            ('MISMATCH', r'.'),
        ]

        parts = [f'(?P<{name}>{pattern})' for name, pattern in self.token_specs]
        # compile without DOTALL because comment pattern already uses [\s\S]
        self.master_re = re.compile('|'.join(parts))

        # palavras reservadas (em lower-case para comparação)
        self.keywords = {
            'program','begin','end','type','var','function','procedure',
            'if','then','else','while','do','array','of','record','read','write','const'
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
                # atualiza linha/coluna mesmo dentro do comentário
                self.line += value.count('\n')
                # após comentário, colocamos coluna no final da última linha do comentário +1
                if '\n' in value:
                    # posição depois do último newline
                    last_line = value.split('\n')[-1]
                    self.col = len(last_line) + 1
                else:
                    self.col += len(value)
                continue
            elif kind == 'ID' and value.lower() in self.keywords:
                kind = value.upper()   # token do tipo PROGRAM, BEGIN, IF etc.
            elif kind == 'MISMATCH':
                raise LexerError(f'Caractere inesperado {value!r} na linha {self.line}, coluna {self.col}')

            token = Token(kind, value, self.line, self.col)
            yield token
            self.col += len(value)
