"""
Otimizador de Código Intermediário (TAC)
Implementa várias técnicas de otimização para o código de três endereços.
"""

from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from tac_generator import TACInstruction


class TACOptimizer:
    """
    Otimizador de código TAC que aplica múltiplas passes de otimização.
    """

    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions
        self.optimizations_applied = []

    def optimize(self, passes: Optional[List[str]] = None) -> List[TACInstruction]:
        """
        Aplica passes de otimização no código TAC.

        Args:
            passes: Lista de passes a aplicar. Se None, aplica todas.
                   Opções: 'constant_folding', 'constant_propagation',
                          'copy_propagation', 'dead_code', 'cse'

        Returns:
            Lista de instruções otimizadas
        """
        if passes is None:
            passes = ['constant_folding', 'constant_propagation',
                     'copy_propagation', 'dead_code', 'cse']

        optimized = self.instructions.copy()

        # Aplicar múltiplas iterações até não haver mais mudanças
        max_iterations = 10
        for iteration in range(max_iterations):
            changed = False
            initial_count = len(optimized)

            for pass_name in passes:
                if pass_name == 'constant_folding':
                    optimized = self._constant_folding(optimized)
                elif pass_name == 'constant_propagation':
                    optimized = self._constant_propagation(optimized)
                elif pass_name == 'copy_propagation':
                    optimized = self._copy_propagation(optimized)
                elif pass_name == 'dead_code':
                    optimized = self._dead_code_elimination(optimized)
                elif pass_name == 'cse':
                    optimized = self._common_subexpression_elimination(optimized)

            # Verifica se houve mudança
            if len(optimized) != initial_count:
                changed = True

            if not changed:
                break

        return optimized

    def _is_constant(self, value: Optional[str]) -> bool:
        """Verifica se um valor é uma constante numérica."""
        if value is None:
            return False
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _is_temp(self, value: Optional[str]) -> bool:
        """Verifica se um valor é uma variável temporária."""
        if value is None:
            return False
        return isinstance(value, str) and value.startswith('T')

    def _is_variable(self, value: Optional[str]) -> bool:
        """Verifica se um valor é uma variável (não constante e não None)."""
        return value is not None and not self._is_constant(value)

    def _eval_binop(self, op: str, left: str, right: str) -> Optional[str]:
        """
        Avalia uma operação binária entre constantes.

        Returns:
            String com o resultado ou None se não puder avaliar
        """
        try:
            left_val = float(left)
            right_val = float(right)

            if op == 'ADD':
                result = left_val + right_val
            elif op == 'SUB':
                result = left_val - right_val
            elif op == 'MUL':
                result = left_val * right_val
            elif op == 'DIV':
                if right_val == 0:
                    return None  # Não otimizar divisão por zero
                result = left_val / right_val
            elif op == 'JEQ':
                return 'true' if left_val == right_val else 'false'
            elif op == 'JNE':
                return 'true' if left_val != right_val else 'false'
            elif op == 'JLT':
                return 'true' if left_val < right_val else 'false'
            elif op == 'JGT':
                return 'true' if left_val > right_val else 'false'
            elif op == 'JLE':
                return 'true' if left_val <= right_val else 'false'
            elif op == 'JGE':
                return 'true' if left_val >= right_val else 'false'
            elif op == 'AND':
                # Trata como booleano: 0 = false, não-zero = true
                return 'true' if (left_val != 0 and right_val != 0) else 'false'
            elif op == 'OR':
                return 'true' if (left_val != 0 or right_val != 0) else 'false'
            else:
                return None

            # Retorna como inteiro se possível, senão como float
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)

        except (ValueError, TypeError, ZeroDivisionError):
            return None

    def _constant_folding(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Dobramento de constantes: Avalia expressões constantes em tempo de compilação.
        Exemplo: T1 := 5 + 3  =>  T1 := 8
        """
        optimized = []

        for inst in instructions:
            if inst.op in ['ADD', 'SUB', 'MUL', 'DIV', 'JEQ', 'JNE', 'JLT', 'JGT', 'JLE', 'JGE', 'AND', 'OR']:
                # Se ambos operandos são constantes, avalia
                if self._is_constant(inst.addr2) and self._is_constant(inst.addr3):
                    result = self._eval_binop(inst.op, inst.addr2, inst.addr3)
                    if result is not None:
                        # Substitui por atribuição direta
                        optimized.append(TACInstruction('ATR', inst.addr1, result, None))
                        self.optimizations_applied.append(f'Constant folding: {inst.op} {inst.addr2} {inst.addr3} => {result}')
                        continue

            optimized.append(inst)

        return optimized

    def _constant_propagation(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Propagação de constantes: Substitui variáveis por seus valores constantes.
        Exemplo:
            A := 5
            B := A + 3  =>  B := 5 + 3
        """
        constants: Dict[str, str] = {}
        optimized = []

        for inst in instructions:
            # Limpa constantes em pontos de controle
            if inst.op in ['LABEL', 'JMP', 'JZ', 'JNZ', 'CALL']:
                constants.clear()

            # Propaga constantes nos operandos
            addr2 = inst.addr2
            addr3 = inst.addr3

            if addr2 and addr2 in constants:
                addr2 = constants[addr2]

            if addr3 and addr3 in constants:
                addr3 = constants[addr3]

            # Cria instrução com operandos propagados
            new_inst = TACInstruction(inst.op, inst.addr1, addr2, addr3)
            optimized.append(new_inst)

            # Registra novas constantes
            if inst.op == 'ATR' and inst.addr1 and inst.addr2:
                if self._is_constant(inst.addr2):
                    constants[inst.addr1] = inst.addr2
                elif inst.addr1 in constants:
                    del constants[inst.addr1]

        return optimized

    def _copy_propagation(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Propagação de cópias: Substitui variáveis que são cópias de outras.
        Exemplo:
            T1 := A
            T2 := T1 + B  =>  T2 := A + B
        """
        copies: Dict[str, str] = {}
        optimized = []

        for inst in instructions:
            # Limpa cópias em pontos de controle
            if inst.op in ['LABEL', 'JMP', 'JZ', 'JNZ', 'CALL']:
                copies.clear()

            # Propaga cópias nos operandos
            addr2 = inst.addr2
            addr3 = inst.addr3

            if addr2 and addr2 in copies:
                addr2 = copies[addr2]

            if addr3 and addr3 in copies:
                addr3 = copies[addr3]

            # Cria instrução com operandos propagados
            new_inst = TACInstruction(inst.op, inst.addr1, addr2, addr3)
            optimized.append(new_inst)

            # Registra novas cópias (A := B)
            if inst.op == 'ATR' and inst.addr1 and inst.addr2:
                if self._is_variable(inst.addr2) and not self._is_constant(inst.addr2):
                    copies[inst.addr1] = inst.addr2
                elif inst.addr1 in copies:
                    del copies[inst.addr1]

            # Invalida cópias se a variável é modificada
            if inst.addr1:
                # Remove todas as cópias que dependem desta variável
                to_remove = [k for k, v in copies.items() if v == inst.addr1]
                for k in to_remove:
                    del copies[k]

        return optimized

    def _dead_code_elimination(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Eliminação de código morto: Remove instruções que nunca são usadas.
        Remove temporárias que são atribuídas mas nunca lidas.
        """
        # Primeira passagem: identifica variáveis usadas
        used_vars: Set[str] = set()

        for inst in instructions:
            # Marcar operandos como usados
            if inst.addr2:
                used_vars.add(inst.addr2)
            if inst.addr3:
                used_vars.add(inst.addr3)

            # Instruções especiais sempre marcam seus operandos como usados
            if inst.op in ['JZ', 'JNZ', 'WRITE', 'RETURN', 'PARAM']:
                if inst.addr1:
                    used_vars.add(inst.addr1)

        # Segunda passagem: remove atribuições a variáveis não usadas
        optimized = []

        for inst in instructions:
            # Mantém instruções que não são atribuições
            if inst.op not in ['ATR', 'ADD', 'SUB', 'MUL', 'DIV', 'JEQ', 'JNE', 'JLT', 'JGT', 'JLE', 'JGE', 'AND', 'OR', 'NOT']:
                optimized.append(inst)
                continue

            # Mantém atribuições a variáveis usadas ou não-temporárias
            if inst.addr1:
                # Sempre mantém variáveis do programa (não temporárias)
                if not self._is_temp(inst.addr1):
                    optimized.append(inst)
                # Mantém temporárias se forem usadas
                elif inst.addr1 in used_vars:
                    optimized.append(inst)
                else:
                    self.optimizations_applied.append(f'Dead code eliminated: {inst.op} {inst.addr1}')
            else:
                optimized.append(inst)

        return optimized

    def _common_subexpression_elimination(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Eliminação de subexpressões comuns (CSE): Reutiliza resultados de cálculos idênticos.
        Exemplo:
            T1 := A + B
            T2 := A + B  =>  T2 := T1
        """
        # Mapeia expressões para suas variáveis resultado
        expressions: Dict[Tuple[str, str, str], str] = {}
        # Mapeia variáveis para suas substituições
        replacements: Dict[str, str] = {}
        optimized = []

        for inst in instructions:
            # Limpa expressões em pontos de controle
            if inst.op in ['LABEL', 'JMP', 'JZ', 'JNZ', 'CALL']:
                expressions.clear()
                replacements.clear()

            # Aplica substituições nos operandos
            addr2 = inst.addr2
            addr3 = inst.addr3

            if addr2 and addr2 in replacements:
                addr2 = replacements[addr2]

            if addr3 and addr3 in replacements:
                addr3 = replacements[addr3]

            # Verifica se é uma operação que pode ser eliminada
            if inst.op in ['ADD', 'SUB', 'MUL', 'DIV', 'JEQ', 'JNE', 'JLT', 'JGT', 'JLE', 'JGE', 'AND', 'OR']:
                expr_key = (inst.op, addr2, addr3)

                if expr_key in expressions:
                    # Subexpressão comum encontrada! Substitui por cópia
                    existing_var = expressions[expr_key]
                    optimized.append(TACInstruction('ATR', inst.addr1, existing_var, None))
                    replacements[inst.addr1] = existing_var
                    self.optimizations_applied.append(f'CSE: {inst.op} {addr2} {addr3} reused as {existing_var}')
                else:
                    # Nova expressão
                    new_inst = TACInstruction(inst.op, inst.addr1, addr2, addr3)
                    optimized.append(new_inst)
                    expressions[expr_key] = inst.addr1
            else:
                # Outras instruções
                new_inst = TACInstruction(inst.op, inst.addr1, addr2, addr3)
                optimized.append(new_inst)

            # Invalida expressões quando variáveis são modificadas
            if inst.addr1:
                # Remove expressões que usam esta variável
                to_remove = [k for k, v in expressions.items() if inst.addr1 in (k[1], k[2])]
                for k in to_remove:
                    del expressions[k]

        return optimized

    def print_optimizations(self):
        """Imprime as otimizações aplicadas."""
        if not self.optimizations_applied:
            print("\nNenhuma otimização aplicada.")
        else:
            print(f"\n{'='*60}")
            print(f"OTIMIZAÇÕES APLICADAS ({len(self.optimizations_applied)} total)")
            print('='*60)
            for i, opt in enumerate(self.optimizations_applied, 1):
                print(f"{i}. {opt}")
            print('='*60)

    @staticmethod
    def compare_code(original: List[TACInstruction], optimized: List[TACInstruction]):
        """Compara código original com otimizado e mostra estatísticas."""
        print(f"\n{'='*60}")
        print("ESTATÍSTICAS DE OTIMIZAÇÃO")
        print('='*60)
        print(f"Instruções originais:  {len(original)}")
        print(f"Instruções otimizadas: {len(optimized)}")
        reduction = len(original) - len(optimized)
        if len(original) > 0:
            percentage = (reduction / len(original)) * 100
            print(f"Redução:               {reduction} instruções ({percentage:.1f}%)")
        print('='*60)


def optimize_tac(instructions: List[TACInstruction],
                 passes: Optional[List[str]] = None,
                 verbose: bool = True) -> List[TACInstruction]:
    """
    Função utilitária para otimizar código TAC.

    Args:
        instructions: Lista de instruções TAC
        passes: Passes de otimização a aplicar (None = todas)
        verbose: Se True, imprime informações sobre otimizações

    Returns:
        Lista de instruções otimizadas
    """
    optimizer = TACOptimizer(instructions)
    optimized = optimizer.optimize(passes)

    if verbose:
        optimizer.print_optimizations()
        TACOptimizer.compare_code(instructions, optimized)

    return optimized
