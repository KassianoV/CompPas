from lexer import Lexer, LexerError
from parser import Parser, ParserError
from ast_nodes import *
from ast_exporter import export_ast_to_json, DotExporter
import sys, os

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def carregar_codigo(caminho: str) -> str:
    """Lê o conteúdo de um arquivo .pas e retorna como string."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")
    if not caminho.endswith(".pas"):
        raise ValueError("O arquivo deve ter a extensão .pas")
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

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
    """Impressão hierárquica da AST."""
    pad = '  ' * indent
    if isinstance(node, Program):
        print(f"{pad}Program(name='{node.name}')")
        if node.decls:
            print(f"{pad}  Declarações:")
            for d in node.decls:
                print_ast(d, indent+2)
        print(f"{pad}  Bloco principal:")
        print_ast(node.block, indent+2)

    elif isinstance(node, VarDecl):
        print(f"{pad}VarDecl(names={node.names}, type={node.type_name})")

    elif isinstance(node, ConstDecl):
        print(f"{pad}ConstDecl(name='{node.name}')")
        print_ast(node.value, indent+1)

    elif isinstance(node, TypeDecl):
        print(f"{pad}TypeDecl(name='{node.name}', definition='{node.definition}')")

    elif isinstance(node, FunctionDecl):
        print(f"{pad}FunctionDecl(name='{node.name}', return_type='{node.return_type}')")
        if node.params:
            print(f"{pad}  Params:")
            for p in node.params:
                print_ast(p, indent+2)
        if node.local_vars:
            print(f"{pad}  LocalVars:")
            for v in node.local_vars:
                print_ast(v, indent+2)
        print(f"{pad}  Body:")
        print_ast(node.body, indent+2)

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
        if node.left: print_ast(node.left, indent+1)
        if node.right: print_ast(node.right, indent+1)

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

def testar_parser(codigo: str):
    """Executa o parser e imprime a AST."""
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
    """Exporta a AST para JSON e DOT."""
    if not ast:
        print("Nenhuma AST para exportar!")
        return
    os.makedirs("export", exist_ok=True)
    export_ast_to_json(ast, "export/ast.json")
    dot = DotExporter()
    dot.export(ast, "export/ast.dot")
    print("\n✅ AST exportada com sucesso!")
    print("  → export/ast.json")
    print("  → export/ast.dot (visualize em https://dreampuf.github.io/GraphvizOnline/)")

# ==========================================
# MENU PRINCIPAL
# ==========================================
def menu():
    ultima_ast = None
    while True:
        print("\n========== MENU ==========")
        print("1 - Testar lexer (arquivo .pas)")
        print("2 - Testar parser (arquivo .pas)")
        print("3 - Exportar AST (JSON / DOT)")
        print("4 - Sair")
        print("==========================")
        op = input("Escolha uma opção: ").strip()

        if op in ('1', '2'):
            caminho = input("\nInforme o caminho do arquivo .pas: ").strip()
            try:
                codigo = carregar_codigo(caminho)
            except Exception as e:
                print(f"❌ Erro ao carregar arquivo: {e}")
                continue

            if op == '1':
                testar_lexer(codigo)
            elif op == '2':
                ultima_ast = testar_parser(codigo)

        elif op == '3':
            exportar_ast(ultima_ast)

        elif op == '4':
            print("Saindo...")
            sys.exit(0)

        else:
            print("Opção inválida. Tente novamente.")

# ==========================================
if __name__ == "__main__":
    menu()
