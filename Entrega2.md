<div align="center"> <h2> Mapeamento Completo de Regras Semânticas por Não-Terminal </h2> </div> 

Nós observamos que de acordo com a atribuições das regras em alguns Não-terminais o codigo pode ser verificado de forma diferente dependendo do momento, podendo ser na hora de compilação ou na hora de escrita do código.
Nós usamos a verificação no momento da escrita do código. <br><br>

| Não-Terminal                             | Regras              | Verificações Semânticas                               |
| ---------------------------------------- | ------------------- | ----------------------------------------------------- |
| **[PROGRAMA]**                           | -                   | Nenhuma verificação                                   |
| **[CORPO]**                              | -                   | Estrutura do programa                                 |
| **[DECLARACOES]**                        | -                   | Organização das seções                                |
| **[DEF_CONST]**                          | -                   | Seção de constantes                                   |
| **[LISTA_CONST]**                        | -                   | Lista de constantes                                   |
| **[LISTA_CONST']**                       | -                   | Continuação da lista                                  |
| **[CONSTANTE]**                          | **R1, R3**          | • Declaração única<br>• Tipo da expressão             |
| **[CONST_VALOR]**                        | **R3**              | • Inferir tipo do valor                               |
| **[DEF_TIPOS]**                          | -                   | Seção de tipos                                        |
| **[LISTA_TIPOS]**                        | -                   | Lista de tipos                                        |
| **[LISTA_TIPOS']**                       | -                   | Continuação da lista                                  |
| **[TIPO]**                               | **R1**              | • Nome de tipo único                                  |
| **[TIPO_DADO]**                          | **R2**              | • Tipo existe (se customizado)                        |
| **[DEF_VAR]**                            | -                   | Seção de variáveis                                    |
| **[LISTA_VAR]**                          | -                   | Lista de variáveis                                    |
| **[LISTA_VAR']**                         | -                   | Continuação da lista                                  |
| **[VARIAVEL]**                           | **R1, R2**          | • Declaração única<br>• Tipo válido                   |
| **[LISTA_ID]**                           | **R1**              | • IDs únicos na mesma linha                           |
| **[LISTA_ID']**                          | -                   | Continuação da lista de IDs                           |
| **[NUMERO]**                             | -                   | Literal numérico                                      |
| **[LISTA_FUNC]**                         | -                   | Lista de funções                                      |
| **[FUNCAO]**                             | **R1, R7**          | • Nome único<br>• Tipo de retorno                     |
| **[NOME_FUNCAO]**                        | **R1, R4**          | • Nome não usado<br>• Pode ter parâmetros             |
| **[BLOCO_FUNCAO]**                       | -                   | Corpo da função                                       |
| **[BLOCO]**                              | -                   | Bloco de comandos                                     |
| **[LISTA_COM]**                          | -                   | Lista de comandos                                     |
| **[COMANDO]**                            | **R2, R3, R7**      | Depende do tipo de comando                            |
| **[COMANDO] → [ID] [NOME] (:=) [VALOR]** | **R2, R3**          | • Variável declarada<br>• Tipos compatíveis           |
| **[COMANDO] → (while) ...**              | **R3**              | • Condição booleana                                   |
| **[COMANDO] → (if) ...**                 | **R3**              | • Condição booleana                                   |
| **[COMANDO] → (write) ...**              | -                   | Saída                                                 |
| **[COMANDO] → (read) ...**               | **R2**              | • Variável declarada                                  |
| **[ELSE]**                               | -                   | Parte else opcional                                   |
| **[VALOR]**                              | **R2, R3**          | • Identificadores declarados<br>• Tipos válidos       |
| **[VALOR']**                             | **R2, R4, R5, R6**  | • Função declarada<br>• Parâmetros corretos           |
| **[LISTA_NOME]**                         | **R5, R6**          | • Quantidade de parâmetros<br>• Tipos dos parâmetros  |
| **[LISTA_NOME']**                        | -                   | Continuação da lista                                  |
| **[EXP_LOGICA]**                         | **R3**              | • Operandos booleanos                                 |
| **[EXP_LOGICA']**                        | **R3**              | • Operador lógico válido                              |
| **[EXP_MAT]**                            | **R2, R3**          | • Identificadores declarados<br>• Operandos numéricos |
| **[EXP_MAT']**                           | **R3**              | • Operandos numéricos                                 |
| **[OP_LOGICO]**                          | -                   | Operador de comparação                                |
| **[OP_MAT]**                             | -                   | Operador aritmético                                   |
| **[NOME]**                               | **R2, R8, R9, R10** | • Declarado<br>• Array/Record válido                  |
| **[ID]**                                 | **R2**              | • Declarado (quando usado)                            |

---
<br>
            
<div align="center"> <h2> Tabela de Instruções código intermediario </h2> </div>

| # | Instrução | Categoria | End_1 | End_2 | End_3 | Descrição Curta |
|---|-----------|-----------|-------|-------|-------|-----------------|
| 1 | **ATR**  | Atribuição | dest | src | - | dest = src |
| 2 | **ADD**  | Aritmética | res | op1 | op2 | res = op1 + op2 |
| 3 | **SUB**  | Aritmética | res | op1 | op2 | res = op1 - op2 |
| 4 | **MUL**  | Aritmética | res | op1 | op2 | res = op1 * op2 |
| 5 | **DIV**  | Aritmética | res | op1 | op2 | res = op1 / op2 |
| 6 | **EQ**   | Comparação | res | op1 | op2 | res = (op1 == op2) |
| 7 | **NE**   | Comparação | res | op1 | op2 | res = (op1 != op2) |
| 8 | **LT**   | Comparação | res | op1 | op2 | res = (op1 < op2) |
| 9 | **GT**  | Comparação | res | op1 | op2 | res = (op1 > op2) |
| 10 | **NOT** | Lógica | res | op | - | res = NOT op |
| 11 | **JMP** | Controle | label | - | - | goto label |
| 12 | **JZ**  | Controle | label | var | - | if (var == 0) goto |
| 13 | **JNZ** | Controle | label | var | - | if (var != 0) goto |
| 14 | **JEQ** | Controle | label | op1 | op2 | if (op1 == op2) goto |
| 15 | **JNE** | Controle | label | op1 | op2 | if (op1 != op2) goto |
| 16 | **JLT** | Controle | label | op1 | op2 | if (op1 < op2) goto |
| 17 | **JGT** | Controle | label | op1 | op2 | if (op1 > op2) goto |
| 18 | **LABEL** | Controle | nome | - | - | Define rótulo |
| 20 | **CALL** | Função | func | nargs | - | Chama função |
| 21 | **RETURN** | Função | val | - | - | Retorna de função |
| 22 | **READ** | I/O | var | - | - | Lê da entrada |
| 23 | **WRITE** | I/O | val | - | - | Escreve na saída |
| 24 | **HALT** | Sistema | - | - | - | Encerra programa |
| 25 | **NOP** | Sistema | - | - | - | Nenhuma operação |

---
<br>
<div align="center"> <h1> EXPLICAÇÃO DAS INSTRUÇÕES </h1> </div>

<div align="center"> <h2> INSTRUÇÕES DE ATRIBUIÇÃO </h2> </div>

### 1 - ATR (Atribuição)
**Formato:** `ATR  destino  origem`

**Funcionamento:**
- Copia o valor de `origem` para `destino`
- Equivalente a: `destino = origem`
- Pode ser usado com variáveis, constantes ou temporários

<div align="center"> <h2> INSTRUÇÕES ARITMÉTICAS </h2> </div>

### 2 - ADD (adição)
**Formato:** `ADD  resultado  operando1  operando2`

**Funcionamento:**
- Soma `operando1` + `operando2`
- Armazena o resultado em `resultado`
- Equivalente a: `resultado = operando1 + operando2`

### 3 - SUB (Subtração)
**Formato:** `SUB  resultado  operando1  operando2`

**Funcionamento:**
- Subtrai `operando2` de `operando1`
- Armazena em `resultado`
- Equivalente a: `resultado = operando1 - operando2`
- **Ordem importa:** `SUB T1 A B` é `A - B`, não `B - A`

### 4 - MUL (Multiplicação)
**Formato:** `MUL  resultado  operando1  operando2`

**Funcionamento:**
- Multiplica `operando1` × `operando2`
- Armazena em `resultado`
- Equivalente a: `resultado = operando1 * operando2`

### 5 - DIV (Divisão)
**Formato:** `DIV  resultado  operando1  operando2`

**Funcionamento:**
- Divide `operando1` ÷ `operando2`
- Armazena em `resultado`
- Equivalente a: `resultado = operando1 / operando2`
- **Ordem importa:** `DIV T1 A B` é `A / B`, não `B / A`
- **Atenção:** Divisão por zero causa erro em tempo de execução

<div align="center"> <h2> INSTRUÇÕES DE COMPARAÇÃO </h2></div>

Todas retornam 1 (verdadeiro) ou 0 (falso) no resultado.

### 1 - EQ (Igual)
**Formato:** `EQ  resultado  operando1  operando2`

**Funcionamento:**
- Compara se `operando1` == `operando2`
- Resultado = 1 se igual, 0 se diferente
- Equivalente a: `resultado = (operando1 == operando2) ? 1 : 0`

### 2 - NE (Não Igual / Diferente)
**Formato:** `NE  resultado  operando1  operando2`

**Funcionamento:**
- Compara se `operando1` ≠ `operando2`
- Resultado = 1 se diferente, 0 se igual
- Equivalente a: `resultado = (operando1 != operando2) ? 1 : 0`

### 3 LT (Menor Que)
**Formato:** `LT  resultado  operando1  operando2`

**Funcionamento:**
- Compara se `operando1` < `operando2`
- Resultado = 1 se menor, 0 caso contrário
- **Ordem importa:** `LT T1 A B` testa `A < B`, não `B < A`

### 4 - GT (Maior Que)
**Formato:** `GT  resultado  operando1  operando2`

**Funcionamento:**
- Compara se `operando1` > `operando2`
- Resultado = 1 se maior, 0 caso contrário
- **Ordem importa:** `GT T1 A B` testa `A > B`


<div align="center"> <h2> INSTRUÇÕES LÓGICAS </h2> </div>

### 1 - NOT (NÃO Lógico)
**Formato:** `NOT  resultado  operando`

**Funcionamento:**
- Nega o `operando`
- Resultado = 1 se operando é zero, 0 se operando não-zero
- Equivalente a: `resultado = !operando`

<div align="center"> <h2> INSTRUÇÕES DE CONTROLE DE FLUXO </h2> </div>

### 1 - JMP (Jump Incondicional)
**Formato:** `JMP  label`

**Funcionamento:**
- Salta incondicionalmente para `label`
- Equivalente a: `goto label`
- Sempre executa o salto

### 2 - JZ (Jump if Zero / Jump if False)**
**Formato:** `JZ  label  variavel`

**Funcionamento:**
- Salta para `label` SE `variavel` == 0 (falso)
- Se `variavel` ≠ 0, continua na próxima instrução
- Equivalente a: `if (variavel == 0) goto label`

### 3 - JNZ (Jump if Not Zero / Jump if True)**
**Formato:** `JNZ  label  variavel`

**Funcionamento:**
- Salta para `label` SE `variavel` ≠ 0 (verdadeiro)
- Se `variavel` == 0, continua na próxima instrução
- Equivalente a: `if (variavel != 0) goto label`
- **Oposto de JZ**

### 4 - JEQ (Jump if Equal)
**Formato:** `JEQ  label  operando1  operando2`

**Funcionamento:**
- Salta para `label` SE `operando1` == `operando2`
- Equivalente a: `if (op1 == op2) goto label`
- **Otimização:** Evita temporário para a comparação

### 5 - JNE (Jump if Not Equal)
**Formato:** `JNE  label  operando1  operando2`

**Funcionamento:**
- Salta para `label` SE `operando1` ≠ `operando2`

### 6 - JLT (Jump if Less Than)
**Formato:** `JLT  label  operando1  operando2`

**Funcionamento:**
- Salta para `label` SE `operando1` < `operando2`

### 7 - JGT (Jump if Greater Than)
**Formato:** `JGT  label  operando1  operando2`

**Funcionamento:**
- Salta para `label` SE `operando1` > `operando2`


### 10 - LABEL (Definição de Rótulo)**
**Formato:** `LABEL  nome`

**Funcionamento:**
- Define um ponto de destino para saltos
- Marca uma posição no código
- Não executa nenhuma operação
- **Nome único** no escopo

<div align="center"> <h2> INSTRUÇÕES DE FUNÇÃO </h2></div>


### 1 - CALL (Chamar Função)
**Formato:** `CALL  nome_funcao  num_args`

**Funcionamento:**
- Chama a função `nome_funcao`
- `num_args` = número de argumentos passados
- **Validação:** num_args deve corresponder aos PARAMs anteriores
- Após execução, valor de retorno fica em `RETVAL`

### 2 - RETURN (Retornar de Função)
**Formato:** `RETURN  valor`

**Funcionamento:**
- Retorna de função com `valor`
- Armazena `valor` em `RETVAL` (variável especial)
- Restaura contexto do chamador
- Volta para instrução após CALL

<div align="center"> <h2> INSTRUÇÕES DE ENTRADA/SAÍDA </h2> </div>

### 1 - READ (Ler da Entrada)**
**Formato:** `READ  variavel`

**Funcionamento:**
- Lê um valor da entrada padrão (teclado/stdin)
- Armazena o valor lido em `variavel`
- Bloqueia até entrada estar disponível
- Conversão automática para o tipo da variável

### 2 - WRITE (Escrever na Saída)
**Formato:** `WRITE  valor`

**Funcionamento:**
- Escreve `valor` na saída padrão (tela/stdout)
- `valor` pode ser variável, constante ou temporário
- Conversão automática para string para exibição

<div align="center"> <h2> INSTRUÇÕES DE SISTEMA </h2> </div>

### 1 - HALT (Encerrar Programa)
**Formato:** `HALT`

**Funcionamento:**
- Encerra a execução do programa
- Equivalente a: `exit(0)`
- Deve ser a última instrução do programa principal
- Código de saída = 0 (sucesso)

### 2 - NOP (No Operation / Operação Nula)
**Formato:** `NOP`

**Funcionamento:**
- Não faz nada
- Apenas avança para próxima instrução
- Usado como placeholder
- Útil para alinhamento ou futuras otimizações