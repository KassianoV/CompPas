from lexer import Lexer, LexerError
from parser import Parser, ParserError
from ast_nodes import *
from ast_exporter import export_ast_to_json, DotExporter
import sys, os

def testar_lexer(codigo_fonte: str):
    print("\n===== RESULTADO DA ANÁLISE LÉXICA =====")
    try:
        lexer = Lexer(codigo_fonte)
        for token in lexer.tokenize():
            print(f"{token.line:3}:{token.column:<3}  {token.type:<12}  {token.lexeme}")
    except LexerError as e:
        print(f"Erro léxico: {e}")
    print("======================================\n")

def print_ast(node, indent=0):
    pad = '  ' * indent
    if isinstance(node, Program):
        print(f"{pad}Program(name='{node.name}')")
        if node.var_decls:
            print(f"{pad}  VarDecls:")
            for vd in node.var_decls:
                print(f"{pad}    {vd.names} : {vd.type_name}")
        print(f"{pad}  Block:")
        print_ast(node.block, indent+2)
    elif isinstance(node, Compound):
        print(f"{pad}Compound:")
        for s in node.statements:
            print_ast(s, indent+1)
    elif isinstance(node, Assign):
        print(f"{pad}Assign:")
        print_ast(node.target, indent+1)
        print_ast(node.value, indent+1)
    elif isinstance(node, Var):
        print(f"{pad}Var(name='{node.name}')")
    elif isinstance(node, Num):
        print(f"{pad}Num(value={node.value})")
    elif isinstance(node, BinOp):
        print(f"{pad}BinOp(op='{node.op}')")
        print_ast(node.left, indent+1)
        print_ast(node.right, indent+1)
    elif isinstance(node, If):
        print(f"{pad}If:")
        print(f"{pad}  Condition:")
        print_ast(node.condition, indent+2)
        print(f"{pad}  Then:")
        print_ast(node.then_branch, indent+2)
        if node.else_branch:
            print(f"{pad}  Else:")
            print_ast(node.else_branch, indent+2)
    elif isinstance(node, While):
        print(f"{pad}While:")
        print(f"{pad}  Condition:")
        print_ast(node.condition, indent+2)
        print(f"{pad}  Body:")
        print_ast(node.body, indent+2)
    elif isinstance(node, Call):
        print(f"{pad}Call(name='{node.name}')")
        for a in node.args:
            print_ast(a, indent+1)
    else:
        print(f"{pad}{node!r}")

def testar_parser(codigo):
    lexer = Lexer(codigo)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("\n===== ÁRVORE SINTÁTICA ABSTRATA =====")
        print_ast(ast)
        print("=====================================")
        return ast
    except ParserError as e:
        print(f"Erro sintático: {e}")
        return None

def exportar_ast(ast):
    if not ast:
        print("Nenhuma AST para exportar!")
        return
    os.makedirs("export", exist_ok=True)
    export_ast_to_json(ast, "export/ast.json")
    dot = DotExporter()
    dot.export(ast, "export/ast.dot")
    print("Você pode visualizar o arquivo DOT em: https://dreampuf.github.io/GraphvizOnline/")

def menu():
    exemplos = {
        '1': """program exemplo;
var x: integer;
begin
  x := 5 + 3;
  write(x);
end.""",
        '2': """program teste;
var a, b: real;
begin
  read(a);
  b := a * 2;
  write(b);
end."""
    }

    ultima_ast = None
    while True:
        print("\n===== MENU =====")
        print("1 - Testar lexer")
        print("2 - Testar parser (mostrar AST)")
        print("3 - Exportar AST (JSON / DOT)")
        print("4 - Usar exemplo pronto")
        print("5 - Sair")
        print("================")
        op = input("Escolha uma opção: ").strip()
        if op == '1':
            codigo = input("\nDigite o código: \n")
            testar_lexer(codigo)
        elif op == '2':
            codigo = input("\nDigite o código: \n")
            ultima_ast = testar_parser(codigo)
        elif op == '3':
            exportar_ast(ultima_ast)
        elif op == '4':
            print("\nExemplos disponíveis:")
            for k, v in exemplos.items():
                print(f"{k} - {v.splitlines()[0]}")
            escolha = input("Escolha o exemplo: ").strip()
            codigo = exemplos.get(escolha)
            if codigo:
                ultima_ast = testar_parser(codigo)
            else:
                print("Opção inválida.")
        elif op == '5':
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    menu()
