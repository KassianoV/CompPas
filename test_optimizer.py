"""
Script de teste para demonstrar as otimizações do código intermediário
"""

from lexer import Lexer
from parser import Parser
from tac_generator import TACGenerator
from optimizer import optimize_tac, TACOptimizer

def testar_otimizacao(arquivo_pas: str):
    """Testa otimizações em um arquivo Pascal"""
    print("\n" + "="*80)
    print(f"TESTANDO OTIMIZAÇÕES: {arquivo_pas}")
    print("="*80)

    # Lê o código fonte
    with open(arquivo_pas, 'r', encoding='utf-8') as f:
        codigo = f.read()

    print("\nCODIGO FONTE:")
    print("-"*80)
    for i, linha in enumerate(codigo.split('\n'), 1):
        print(f"{i:3}: {linha}")
    print("-"*80)

    # Análise léxica
    lexer = Lexer(codigo)
    tokens = list(lexer.tokenize())

    # Análise sintática e semântica
    parser = Parser(tokens, enable_semantic=True)
    ast = parser.parse()

    # Geração de código intermediário
    generator = TACGenerator()
    tac_instructions = generator.generate(ast)

    # Mostra código original
    print("\nCODIGO TAC ORIGINAL:")
    print("-"*80)
    generator.print_tac()
    print(f"\nTotal: {len(tac_instructions)} instrucoes")

    # Otimiza o código
    print("\nAPLICANDO OTIMIZACOES...")
    print("-"*80)

    optimized_instructions = optimize_tac(tac_instructions, verbose=True)

    # Mostra código otimizado
    optimized_generator = TACGenerator()
    optimized_generator.instructions = optimized_instructions

    print("\nCODIGO TAC OTIMIZADO:")
    print("-"*80)
    optimized_generator.print_tac()
    print(f"\nTotal: {len(optimized_instructions)} instrucoes")

    # Comparação lado a lado
    print("\nCOMPARACAO LADO A LADO:")
    print("="*80)
    print(f"{'ORIGINAL':<40} | {'OTIMIZADO':<40}")
    print("-"*40 + "+" + "-"*40)

    max_len = max(len(tac_instructions), len(optimized_instructions))
    for i in range(max_len):
        left = ""
        right = ""

        if i < len(tac_instructions):
            inst = tac_instructions[i]
            left = f"{inst.op:<8} {inst.addr1 or '':<10} {inst.addr2 or '':<10} {inst.addr3 or ''}"

        if i < len(optimized_instructions):
            inst = optimized_instructions[i]
            right = f"{inst.op:<8} {inst.addr1 or '':<10} {inst.addr2 or '':<10} {inst.addr3 or ''}"

        print(f"{left:<40} | {right:<40}")

    print("="*80)
    print()


if __name__ == "__main__":
    import sys
    import os

    # Lista de arquivos de exemplo
    exemplos = ['exemplo1.pas', 'exemplo2.pas', 'exemplo3.pas']

    # Verifica se um arquivo específico foi passado
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        if os.path.exists(arquivo):
            testar_otimizacao(arquivo)
        else:
            print(f" Arquivo não encontrado: {arquivo}")
    else:
        # Testa todos os exemplos disponíveis
        for exemplo in exemplos:
            if os.path.exists(exemplo):
                testar_otimizacao(exemplo)
                print("\n\n")
            else:
                print(f"  Arquivo {exemplo} não encontrado, pulando...")
