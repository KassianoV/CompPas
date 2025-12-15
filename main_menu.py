"""
Autores: Kassiano Vieira e Claudio Nunes
"""

from lexer import Lexer, LexerError
from parser import Parser, ParserError, SemanticError
from tac_generator import TACGenerator
from optimizer import TACOptimizer, optimize_tac
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
    """Testa apenas o analisador léxico"""
    print("\n===== RESULTADO DA ANÁLISE LÉXICA =====")
    try:
        lexer = Lexer(codigo_fonte)
        tokens = list(lexer.tokenize())
        print(f"\nTotal de tokens: {len(tokens)}\n")
        print(f"{'LINHA':<6} {'COLUNA':<8} {'TIPO':<15} {'LEXEMA':<20}")
        print("-" * 55)
        for token in tokens:
            print(f"{token.line:<6} {token.column:<8} {token.type:<15} {token.lexeme:<20}")
        print("\n Análise léxica concluída com sucesso!")
    except LexerError as e:
        print(f"\n Erro léxico: {e}")
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

    elif isinstance(node, String):
        print(f"{pad}String(value='{node.value}')")

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

def testar_parser_com_semantica(codigo: str, habilitar_semantica=True):
    """Executa o parser com análise semântica integrada."""
    lexer = Lexer(codigo)
    tokens = list(lexer.tokenize())
    parser = Parser(tokens, enable_semantic=habilitar_semantica)
    
    try:
        ast = parser.parse()
        print("\n===== ÁRVORE SINTÁTICA ABSTRATA =====")
        print_ast(ast)
        print("=====================================")
        
        if habilitar_semantica:
            print("\n Análise sintática e semântica concluídas com sucesso!")
        else:
            print("\n Análise sintática concluída com sucesso!")
        
        return ast
    except ParserError as e:
        print(f"\n Erro sintático: {e}")
        return None
    except SemanticError as e:
        print(f"\n {e}")
        return None

def gerar_codigo_intermediario(ast):
    """Gera código intermediário (TAC) a partir da AST"""
    if not ast:
        print(" Nenhuma AST disponível para gerar código intermediário!")
        return None
    
    print("\n Gerando código intermediário...")
    
    try:
        generator = TACGenerator()
        tac_instructions = generator.generate(ast)
        
        # Exibe o código TAC
        generator.print_tac()
        
        return generator
    except Exception as e:
        print(f"\n Erro ao gerar código intermediário: {e}")
        import traceback
        traceback.print_exc()
        return None

def exportar_ast(ast):
    """Exporta a AST para JSON e DOT."""
    if not ast:
        print(" Nenhuma AST para exportar!")
        return
    
    os.makedirs("export", exist_ok=True)
    
    try:
        export_ast_to_json(ast, "export/ast.json")
        dot = DotExporter()
        dot.export(ast, "export/ast.dot")
        print("\n AST exportada com sucesso!")
        print("  → export/ast.json")
        print("  → export/ast.dot (visualize em https://dreampuf.github.io/GraphvizOnline/)")
    except Exception as e:
        print(f"\n Erro ao exportar AST: {e}")

def exportar_tac(generator: TACGenerator, otimizado=False):
    """Exporta o código TAC para arquivo"""
    if not generator:
        print(" Nenhum código TAC para exportar!")
        return

    os.makedirs("export", exist_ok=True)

    try:
        filename = "export/codigo_intermediario_otimizado.tac" if otimizado else "export/codigo_intermediario.tac"
        generator.export_tac(filename)
    except Exception as e:
        print(f"\n Erro ao exportar código TAC: {e}")

def otimizar_codigo_tac(generator: TACGenerator):
    """Otimiza o código TAC usando todas as técnicas disponíveis"""
    if not generator or not generator.instructions:
        print(" Nenhum código TAC disponível para otimizar!")
        return None

    print("\n OTIMIZANDO CÓDIGO INTERMEDIÁRIO...")
    print("="*70)

    # Mostra código original
    print("\n CÓDIGO ORIGINAL:")
    print("-"*70)
    generator.print_tac()

    # Aplica otimizações
    original_instructions = generator.instructions.copy()
    optimized_instructions = optimize_tac(original_instructions, verbose=True)

    # Cria um novo gerador com instruções otimizadas
    optimized_generator = TACGenerator()
    optimized_generator.instructions = optimized_instructions

    # Mostra código otimizado
    print("\n CÓDIGO OTIMIZADO:")
    print("-"*70)
    optimized_generator.print_tac()

    return optimized_generator

def comparar_codigo_tac(generator_original: TACGenerator, generator_otimizado: TACGenerator):
    """Compara código original com otimizado lado a lado"""
    if not generator_original or not generator_otimizado:
        print(" É necessário ter ambos os códigos (original e otimizado) para comparar!")
        return

    print("\n" + "="*70)
    print(" "*20 + "COMPARAÇÃO DE CÓDIGO TAC")
    print("="*70)

    original = generator_original.instructions
    otimizado = generator_otimizado.instructions

    max_len = max(len(original), len(otimizado))

    print(f"\n{'ORIGINAL':<35} | {'OTIMIZADO':<35}")
    print("-"*35 + "+" + "-"*35)

    for i in range(max_len):
        left = ""
        right = ""

        if i < len(original):
            inst = original[i]
            left = f"{inst.op:<8} {inst.addr1 or '':<10} {inst.addr2 or '':<10} {inst.addr3 or '':<10}"

        if i < len(otimizado):
            inst = otimizado[i]
            right = f"{inst.op:<8} {inst.addr1 or '':<10} {inst.addr2 or '':<10} {inst.addr3 or '':<10}"

        print(f"{left:<35} | {right:<35}")

    print("-"*70)
    print(f"Total de instruções: {len(original):<18} | {len(otimizado):<18}")
    reduction = len(original) - len(otimizado)
    if len(original) > 0:
        percentage = (reduction / len(original)) * 100
        print(f"Redução: {reduction} instruções ({percentage:.1f}%)")
    print("="*70)

def processar_arquivo_completo(caminho: str):
    """Processa um arquivo completamente: léxico, sintático, semântico e TAC"""
    try:
        print(f"\n Carregando arquivo: {caminho}")
        codigo = carregar_codigo(caminho)
        
        print(f"\n Código fonte ({len(codigo)} caracteres):")
        print("-" * 70)
        for i, linha in enumerate(codigo.split('\n'), 1):
            print(f"{i:3}: {linha}")
        print("-" * 70)
        
        # 1. Análise Léxica
        print("\n ETAPA 1: Análise Léxica")
        try:
            lexer = Lexer(codigo)
            tokens = list(lexer.tokenize())
            print(f" {len(tokens)} tokens identificados")
        except LexerError as e:
            print(f"❌ Erro léxico: {e}")
            return None, None
        
        # 2. Análise Sintática + Semântica
        print("\n ETAPA 2: Análise Sintática e Semântica")
        parser = Parser(tokens, enable_semantic=True)
        try:
            ast = parser.parse()
            print(" AST construída com sucesso")
            print(" Verificações semânticas concluídas")
        except (ParserError, SemanticError) as e:
            print(f"❌ Erro: {e}")
            return None, None
        
        # 3. Geração de Código Intermediário
        print("\n ETAPA 3: Geração de Código Intermediário")
        generator = gerar_codigo_intermediario(ast)
        
        if generator:
            print(f" {len(generator.instructions)} instruções TAC geradas")
        
        return ast, generator
        
    except Exception as e:
        print(f"\n Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# ==========================================
# MENU PRINCIPAL
# ==========================================
def menu():
    """Menu interativo do compilador"""
    ultima_ast = None
    ultimo_tac = None
    ultimo_tac_otimizado = None

    while True:
        print("\n" + "="*70)
        print(" "*15 + "COMPILADOR PASCAL SIMPLIFICADO")
        print("="*70)
        print("ANÁLISE:")
        print("  1 - Testar apenas Léxico (tokens)")
        print("  2 - Testar apenas Sintático (AST)")
        print("  3 - Testar Sintático + Semântico")
        print("  4 - Processar completo (Léxico + Sintático + Semântico + TAC)")
        print("\nGERAÇÃO DE CÓDIGO:")
        print("  5 - Gerar código intermediário (TAC) da última AST")
        print("  6 - Otimizar código TAC (aplica todas as otimizações)")
        print("  7 - Comparar código original vs otimizado")
        print("\nEXPORTAÇÃO:")
        print("  8 - Exportar AST (JSON / DOT)")
        print("  9 - Exportar código TAC original")
        print(" 10 - Exportar código TAC otimizado")
        print("\n 0 - Sair")
        print("="*70)
        op = input("Escolha uma opção: ").strip()

        if op in ('1', '2', '3', '4'):
            caminho = input("\nInforme o caminho do arquivo .pas: ").strip()
            try:
                codigo = carregar_codigo(caminho)
            except Exception as e:
                print(f" Erro ao carregar arquivo: {e}")
                continue

            if op == '1':
                testar_lexer(codigo)

            elif op == '2':
                ultima_ast = testar_parser_com_semantica(codigo, habilitar_semantica=False)

            elif op == '3':
                ultima_ast = testar_parser_com_semantica(codigo, habilitar_semantica=True)

            elif op == '4':
                ultima_ast, ultimo_tac = processar_arquivo_completo(caminho)
                ultimo_tac_otimizado = None  # Reset otimização

        elif op == '5':
            if ultima_ast:
                ultimo_tac = gerar_codigo_intermediario(ultima_ast)
                ultimo_tac_otimizado = None  # Reset otimização
            else:
                print(" Nenhuma AST disponível! Execute a análise sintática primeiro.")

        elif op == '6':
            if ultimo_tac:
                ultimo_tac_otimizado = otimizar_codigo_tac(ultimo_tac)
            else:
                print(" Nenhum código TAC disponível! Gere o código intermediário primeiro.")

        elif op == '7':
            if ultimo_tac and ultimo_tac_otimizado:
                comparar_codigo_tac(ultimo_tac, ultimo_tac_otimizado)
            else:
                print(" É necessário ter código TAC original e otimizado!")
                if not ultimo_tac:
                    print("   Dica: Use a opção 5 para gerar código TAC")
                if not ultimo_tac_otimizado:
                    print("   Dica: Use a opção 6 para otimizar o código")

        elif op == '8':
            exportar_ast(ultima_ast)

        elif op == '9':
            exportar_tac(ultimo_tac, otimizado=False)

        elif op == '10':
            if ultimo_tac_otimizado:
                exportar_tac(ultimo_tac_otimizado, otimizado=True)
            else:
                print(" Nenhum código TAC otimizado disponível! Use a opção 6 primeiro.")

        elif op == '0':
            print("\n👋 Encerrando o compilador. Até logo!")
            sys.exit(0)

        else:
            print(" Opção inválida. Tente novamente.")

# ==========================================
if __name__ == "__main__":
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*15 + "COMPILADOR PASCAL SIMPLIFICADO" + " "*23 + "║")
    print("║" + " "*10 + "Análise Léxica + Sintática + Semântica + TAC" + " "*14 + "║")
    print("║" + " "*20 + "Autores: Kassiano Vieira & Claudio Nunes" + " "*8 + "║")
    print("╚" + "═"*68 + "╝")
    menu()
