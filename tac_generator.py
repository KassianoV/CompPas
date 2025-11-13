"""
Gerador de Código Intermediário (Three-Address Code - TAC)
para o Compilador Pascal Simplificado

Autores: Kassiano Vieira e Claudio Nunes
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from ast_nodes import *

@dataclass
class TACInstruction:
    """Representa uma instrução de três endereços"""
    op: str
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    addr3: Optional[str] = None
    
    def __str__(self):
        """Formata a instrução para exibição"""
        parts = [f"{self.op:<8}"]
        if self.addr1 is not None:
            parts.append(f"{str(self.addr1):<12}")
        if self.addr2 is not None:
            parts.append(f"{str(self.addr2):<12}")
        if self.addr3 is not None:
            parts.append(f"{str(self.addr3):<12}")
        return '\t'.join(parts)

class TACGenerator:
    """Gerador de Código Intermediário"""
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.function_labels = {}  # Mapeia nomes de funções para labels
    
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
        instr = TACInstruction(op, addr1, addr2, addr3)
        self.instructions.append(instr)
        return instr
    
    def generate(self, ast: Program) -> List[TACInstruction]:
        """
        Gera código intermediário para o programa completo.
        
        Args:
            ast: Árvore sintática do programa
            
        Returns:
            Lista de instruções TAC geradas
        """
        # Reseta os contadores
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        self.function_labels = {}
        
        # Visita o programa
        self.visit_program(ast)
        
        return self.instructions
    
    def visit_program(self, node: Program):
        """
        Visita o nó Program e gera código para declarações e bloco principal.
        
        Estrutura:
            - Funções primeiro (se houver)
            - Label MAIN
            - Código do bloco principal
            - HALT
        """
        # Primeiro, gera código para todas as funções
        if node.decls:
            for decl in node.decls:
                if isinstance(decl, FunctionDecl):
                    self.visit_function(decl)
        
        # Depois, gera o bloco principal
        self.emit('LABEL', 'MAIN')
        self.visit_compound(node.block)
        self.emit('HALT')
    
    def visit_function(self, node: FunctionDecl):
        """
        Gera código para declaração de função.
        
        Estrutura:
            LABEL  nome_funcao
            [código do corpo]
            RETURN result_temp
        """
        func_label = f"FUNC_{node.name}"
        self.function_labels[node.name.lower()] = func_label
        
        self.emit('LABEL', func_label)
        
        # Corpo da função
        self.visit_compound(node.body)
        
        # Se a função não tiver um return explícito, adiciona um
        # (em Pascal, o retorno é feito atribuindo ao nome da função)
        self.emit('RETURN', node.name)
    
    def visit_compound(self, node: Compound):
        """Visita bloco de comandos"""
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: ASTNode):
        """Despacha para o visitante apropriado de acordo com o tipo do comando"""
        if isinstance(node, Assign):
            self.visit_assign(node)
        elif isinstance(node, If):
            self.visit_if(node)
        elif isinstance(node, While):
            self.visit_while(node)
        elif isinstance(node, Call):
            self.visit_call_statement(node)
        elif isinstance(node, Compound):
            self.visit_compound(node)
        # Outros tipos de nós podem ser ignorados ou gerar erro
    
    def visit_assign(self, node: Assign):
        """
        Gera código para atribuição: <NOME> := <EXP>
        
        Exemplo: A := B + C * D
        Gera:
            MUL     T1      C       D
            ADD     T2      B       T1
            ATR     A       T2
        """
        # Avalia a expressão do lado direito
        value_temp = self.visit_expression(node.value)
        
        # Atribui ao destino
        target = node.target.name
        self.emit('ATR', target, value_temp)
    
    def visit_expression(self, node: ASTNode) -> str:
        """
        Visita uma expressão e retorna o temporário/variável com o resultado.
        
        Returns:
            Nome do temporário ou variável que contém o resultado
        """
        if isinstance(node, Num):
            # Constante numérica - retorna diretamente o valor
            return str(int(node.value) if isinstance(node.value, int) else node.value)
        
        elif isinstance(node, String):
            # String literal
            return f'"{node.value}"'
        
        elif isinstance(node, Var):
            # Variável - retorna o nome
            return node.name
        
        elif isinstance(node, BinOp):
            # Operação binária
            return self.visit_binop(node)
        
        elif isinstance(node, Call):
            # Chamada de função como expressão
            return self.visit_call_expression(node)
        
        else:
            # Caso não tratado - gera temporário vazio
            return self.new_temp()
    
    def visit_binop(self, node: BinOp) -> str:
        """
        Gera código para operações binárias.
        
        Exemplo: A + B
        Gera:
            ADD     T1      A       B
        
        Returns:
            Nome do temporário com o resultado
        """
        # Mapeamento de operadores para instruções TAC
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
            # Operador unário NOT
            operand = self.visit_expression(node.left)
            result = self.new_temp()
            self.emit('NOT', result, operand)
            return result
        
        else:
            # Operadores binários
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right) if node.right else None
            result = self.new_temp()
            
            tac_op = op_map.get(op, 'UNKNOWN')
            self.emit(tac_op, result, left, right)
            
            return result
    
    def visit_if(self, node: If):
        """
        Gera código para comando IF-THEN-ELSE.
        
        Estrutura com else:
            [avaliar condição em T1]
            JZ      L_ELSE  T1
            [código THEN]
            JMP     L_FIM
        L_ELSE:
            [código ELSE]
        L_FIM:
        
        Estrutura sem else:
            [avaliar condição em T1]
            JZ      L_FIM   T1
            [código THEN]
        L_FIM:
        """
        label_else = self.new_label()
        label_end = self.new_label()
        
        # Avalia a condição
        cond_temp = self.visit_expression(node.condition)
        
        # Salta para ELSE (ou FIM) se condição falsa
        if node.else_branch:
            self.emit('JZ', label_else, cond_temp)
        else:
            self.emit('JZ', label_end, cond_temp)
        
        # Código do THEN
        self.visit_statement(node.then_branch)
        
        if node.else_branch:
            # Pula o ELSE após executar THEN
            self.emit('JMP', label_end)
            
            # Código do ELSE
            self.emit('LABEL', label_else)
            self.visit_statement(node.else_branch)
        
        # Label de fim
        self.emit('LABEL', label_end)
    
    def visit_while(self, node: While):
        """
        Gera código para laço WHILE.
        
        Estrutura:
        L_INICIO:
            [avaliar condição em T1]
            JZ      L_FIM   T1
            [código do corpo]
            JMP     L_INICIO
        L_FIM:
        """
        label_start = self.new_label()
        label_end = self.new_label()
        
        # Label do início do loop
        self.emit('LABEL', label_start)
        
        # Avalia a condição
        cond_temp = self.visit_expression(node.condition)
        
        # Salta para fim se condição falsa
        self.emit('JZ', label_end, cond_temp)
        
        # Código do corpo
        self.visit_statement(node.body)
        
        # Volta para o início
        self.emit('JMP', label_start)
        
        # Label do fim
        self.emit('LABEL', label_end)
    
    def visit_call_statement(self, node: Call):
        """
        Gera código para chamada de procedimento (sem retorno usado).
        
        Estrutura:
            PARAM   arg1
            PARAM   arg2
            CALL    funcao  nargs
        """
        func_name = node.name.lower()
        
        if func_name == 'read':
            # READ é uma instrução especial
            if node.args:
                var_temp = self.visit_expression(node.args[0])
                self.emit('READ', var_temp)
        
        elif func_name == 'write':
            # WRITE é uma instrução especial
            if node.args:
                val_temp = self.visit_expression(node.args[0])
                self.emit('WRITE', val_temp)
        
        else:
            # Chamada de função/procedimento normal
            # Empilha parâmetros
            for arg in node.args:
                arg_temp = self.visit_expression(arg)
                self.emit('PARAM', arg_temp)
            
            # Chama a função
            func_label = self.function_labels.get(func_name, func_name)
            self.emit('CALL', func_label, str(len(node.args)))
    
    def visit_call_expression(self, node: Call) -> str:
        """
        Gera código para chamada de função como expressão (usa o retorno).
        
        Estrutura:
            PARAM   arg1
            PARAM   arg2
            CALL    funcao  nargs
            ATR     T_result RETVAL
        
        Returns:
            Nome do temporário com o valor de retorno
        """
        # Gera a chamada
        self.visit_call_statement(node)
        
        # Captura o valor de retorno em um temporário
        result = self.new_temp()
        self.emit('ATR', result, 'RETVAL')
        
        return result
    
    def print_tac(self):
        """Imprime o código TAC gerado de forma formatada"""
        print("\n" + "="*70)
        print(" "*20 + "CÓDIGO INTERMEDIÁRIO (TAC)")
        print("="*70)
        print(f"{'Nº':<5} {'OPERAÇÃO':<10} {'ENDEREÇO 1':<14} {'ENDEREÇO 2':<14} {'ENDEREÇO 3':<14}")
        print("-"*70)
        
        for i, instr in enumerate(self.instructions, 1):
            addr1 = str(instr.addr1) if instr.addr1 is not None else '-'
            addr2 = str(instr.addr2) if instr.addr2 is not None else '-'
            addr3 = str(instr.addr3) if instr.addr3 is not None else '-'
            print(f"{i:<5} {instr.op:<10} {addr1:<14} {addr2:<14} {addr3:<14}")
        
        print("="*70 + "\n")
    
    def export_tac(self, filepath: str):
        """Exporta o código TAC para um arquivo"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# CÓDIGO INTERMEDIÁRIO (TAC)\n")
            f.write("# Gerado pelo Compilador Pascal Simplificado\n")
            f.write("# Formato: OPERAÇÃO ADDR1 ADDR2 ADDR3\n\n")
            
            for i, instr in enumerate(self.instructions, 1):
                f.write(f"{i:4}. {instr}\n")
        
        print(f"✅ Código TAC exportado para: {filepath}")
