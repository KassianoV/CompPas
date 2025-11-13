# Não-Terminais, Regras Semânticas e Instruções de Código Intermediário

## Parte 1: Não-Terminais e Regras Semânticas

Esta seção mapeia cada não-terminal da gramática com as regras semânticas que devem ser avaliadas durante o processamento.

### 📋 Tabela de Não-Terminais e Regras Semânticas

| Não-Terminal | Regras Aplicadas | Descrição das Verificações |
|--------------|------------------|----------------------------|
| **`<PROGRAMA>`** | - | Nenhuma verificação específica |
| **`<CORPO>`** | - | Estrutura geral do programa |
| **`<DECLARACOES>`** | - | Organização das seções |
| **`<DEF_CONST_LIST>`** | **R1** | Declaração única de constantes no escopo |
| **`<CONSTANTE>`** | **R1, R3** | Nome único no escopo; Tipo da expressão constante |
| **`<DEF_TIPOS_LIST>`** | **R1** | Tipo não redefinido |
| **`<TIPO>`** | **R1** | Nome de tipo único |
| **`<TIPO_DADO>`** | - | Validação do tipo base |
| **`<DEF_VAR_LIST>`** | **R1, R2** | Declaração única; Registro na tabela de símbolos |
| **`<VARIAVEL>`** | **R1, R2** | Cada ID declarado uma vez; Tipo válido |
| **`<LISTA_ID>`** | **R1** | IDs únicos na mesma declaração |
| **`<LISTA_FUNC>`** | **R1, R2, R4, R5, R6, R7** | Função única; Parâmetros válidos; Tipo de retorno |
| **`<FUNCAO>`** | **R1, R4, R5, R6, R7** | Nome único; Parâmetros corretos; Retorno compatível |
| **`<NOME_FUNCAO>`** | **R1, R4** | Nome não usado; Tipos de parâmetros válidos |
| **`<BLOCO_FUNCAO>`** | - | Novo escopo criado |
| **`<BLOCO>`** | - | Escopo de bloco |
| **`<COMANDO>`** | *Depende* | Varia conforme o tipo de comando |
| **`<ATRIBUICAO>`** | **R2, R3** | Variável declarada; Tipos compatíveis |
| **`<IF>`** | **R3** | Condição deve resultar em tipo booleano |
| **`<WHILE>`** | **R3** | Condição deve resultar em tipo booleano |
| **`<CHAMADA>`** | **R2, R4, R5, R6** | Função declarada; Quantidade e tipos de parâmetros |
| **`<EXP_LOGICA>`** | **R3** | Operandos booleanos para AND/OR |
| **`<EXP_REL>`** | **R3** | Operandos compatíveis; Retorna boolean |
| **`<EXP_AD>`** | **R3** | Operandos numéricos; Promoção de tipos |
| **`<EXP_MUL>`** | **R3** | Operandos numéricos; Promoção de tipos |
| **`<FATOR>`** | **R2, R3** | Identificadores declarados; Tipos válidos |
| **`<NOME>`** | **R2, R8, R9, R10** | Variável declarada; Acesso array/classe válido |

---

## 📝 Detalhamento das Regras Semânticas

### **R1: Não declarar mais de 1 ID com mesmo nome no mesmo escopo**

**Não-terminais afetados:** `<DEF_CONST_LIST>`, `<CONSTANTE>`, `<DEF_TIPOS_LIST>`, `<TIPO>`, `<DEF_VAR_LIST>`, `<VARIAVEL>`, `<LISTA_ID>`, `<LISTA_FUNC>`, `<FUNCAO>`, `<NOME_FUNCAO>`

**Descrição:**
Garante que cada identificador (variável, constante, tipo ou função) seja declarado apenas uma vez dentro do mesmo escopo.

**Pseudocódigo:**
```python
def verificar_declaracao_unica(nome, escopo_atual):
    if nome in tabela_simbolos[escopo_atual]:
        erro_semantico(f"Identificador '{nome}' já declarado neste escopo")
    else:
        tabela_simbolos[escopo_atual][nome] = info_simbolo
```

**Exemplo de erro:**
```pascal
var 
  A : integer;
  A : real;     {# ERRO R1: 'A' já foi declarado #}
```

---

### **R2: Declaração de ID no escopo antes do uso**

**Não-terminais afetados:** `<DEF_VAR_LIST>`, `<VARIAVEL>`, `<ATRIBUICAO>`, `<FATOR>`, `<NOME>`, `<CHAMADA>`

**Descrição:**
Todo identificador deve ser declarado antes de ser usado. A busca é feita do escopo atual para os escopos externos.

**Pseudocódigo:**
```python
def verificar_declaracao_antes_uso(nome):
    simbolo = buscar_na_tabela(nome, escopo_atual_e_externos)
    if simbolo is None:
        erro_semantico(f"Identificador '{nome}' não foi declarado")
    return simbolo
```

**Exemplo de erro:**
```pascal
begin
  A := 5;      {# ERRO R2: 'A' não foi declarado #}
  B := A + 1;  {# ERRO R2: 'B' não foi declarado #}
end.
```

---

### **R3: Só permite atribuição e operações com tipos iguais**

**Não-terminais afetados:** `<CONSTANTE>`, `<ATRIBUICAO>`, `<IF>`, `<WHILE>`, `<EXP_LOGICA>`, `<EXP_REL>`, `<EXP_AD>`, `<EXP_MUL>`, `<FATOR>`

**Descrição:**
Verifica compatibilidade de tipos em:
- Atribuições
- Operações aritméticas (+, -, *, /)
- Operações relacionais (=, <>, <, >, <=, >=)
- Operações lógicas (and, or, not)
- Condições (if, while)

**Pseudocódigo:**
```python
# Atribuição
def verificar_atribuicao(variavel, expressao):
    tipo_var = obter_tipo(variavel)
    tipo_exp = inferir_tipo(expressao)
    if not tipos_compativeis(tipo_var, tipo_exp):
        erro_semantico(f"Tipos incompatíveis: {tipo_var} e {tipo_exp}")

# Operação aritmética
def verificar_operacao_aritmetica(op, esq, dir):
    tipo_esq = inferir_tipo(esq)
    tipo_dir = inferir_tipo(dir)
    if tipo_esq not in ['integer', 'real'] or tipo_dir not in ['integer', 'real']:
        erro_semantico(f"Operador '{op}' requer operandos numéricos")
    # Retorna 'real' se algum operando for real, senão 'integer'
    return 'real' if 'real' in [tipo_esq, tipo_dir] else 'integer'

# Operação lógica
def verificar_operacao_logica(op, esq, dir):
    tipo_esq = inferir_tipo(esq)
    tipo_dir = inferir_tipo(dir)
    if tipo_esq != 'boolean' or tipo_dir != 'boolean':
        erro_semantico(f"Operador '{op}' requer operandos booleanos")
    return 'boolean'

# Condição
def verificar_condicao(expressao):
    tipo_cond = inferir_tipo(expressao)
    if tipo_cond != 'boolean':
        erro_semantico("Condição deve ser booleana")
```

**Exemplos de erro:**
```pascal
var 
  A : integer;
  B : string;
begin
  A := B;           {# ERRO R3: integer e string incompatíveis #}
  A := A + B;       {# ERRO R3: operação aritmética com string #}
  if A then         {# ERRO R3: condição deve ser boolean #}
    write(A);
end.
```

---

### **R4: Só posso passar parâmetros para funções**

**Não-terminais afetados:** `<LISTA_FUNC>`, `<FUNCAO>`, `<NOME_FUNCAO>`, `<CHAMADA>`

**Descrição:**
Garante que apenas funções/procedimentos possam receber parâmetros. Variáveis e constantes não podem ser "chamadas" com parênteses.

**Pseudocódigo:**
```python
def verificar_chamada(nome, argumentos):
    simbolo = buscar_na_tabela(nome)
    if simbolo is None:
        erro_semantico(f"'{nome}' não foi declarado")
    if simbolo.kind != 'function' and len(argumentos) > 0:
        erro_semantico(f"'{nome}' não é uma função, não pode receber parâmetros")
```

**Exemplo de erro:**
```pascal
var A : integer;
begin
  A(5, 10);    {# ERRO R4: 'A' não é função, não pode ter parâmetros #}
end.
```

---

### **R5: Quantidade de parâmetros na chamada deve ser igual à da declaração**

**Não-terminais afetados:** `<LISTA_FUNC>`, `<FUNCAO>`, `<CHAMADA>`

**Descrição:**
O número de argumentos passados na chamada deve ser igual ao número de parâmetros na declaração da função.

**Pseudocódigo:**
```python
def verificar_quantidade_parametros(nome_funcao, argumentos):
    funcao = buscar_funcao(nome_funcao)
    qtd_esperada = len(funcao.parametros)
    qtd_recebida = len(argumentos)
    if qtd_esperada != qtd_recebida:
        erro_semantico(f"Função '{nome_funcao}' espera {qtd_esperada} "
                      f"parâmetros, mas recebeu {qtd_recebida}")
```

**Exemplo de erro:**
```pascal
function soma(a: integer; b: integer) : integer;
begin
  soma := a + b;
end;

begin
  write(soma(5));        {# ERRO R5: espera 2 parâmetros, recebeu 1 #}
  write(soma(1, 2, 3));  {# ERRO R5: espera 2 parâmetros, recebeu 3 #}
end.
```

---

### **R6: O tipo dos argumentos passados deve ser igual ao tipo dos parâmetros**

**Não-terminais afetados:** `<LISTA_FUNC>`, `<FUNCAO>`, `<CHAMADA>`

**Descrição:**
Cada argumento passado na chamada deve ter tipo compatível com o parâmetro correspondente.

**Pseudocódigo:**
```python
def verificar_tipos_parametros(nome_funcao, argumentos):
    funcao = buscar_funcao(nome_funcao)
    for i, (arg, param) in enumerate(zip(argumentos, funcao.parametros)):
        tipo_arg = inferir_tipo(arg)
        tipo_param = param.tipo
        if not tipos_compativeis(tipo_param, tipo_arg):
            erro_semantico(f"Parâmetro {i+1} de '{nome_funcao}': "
                          f"esperado {tipo_param}, recebido {tipo_arg}")
```

**Exemplo de erro:**
```pascal
function potencia(base: real; expoente: integer) : real;
begin
  {# ... #}
end;

var x : string;
begin
  potencia(x, 2);      {# ERRO R6: param 1 espera real, recebeu string #}
  potencia(2.5, 3.5);  {# ERRO R6: param 2 espera integer, recebeu real #}
end.
```

---

### **R7: O tipo retornado deve ser igual ao tipo de retorno da função**

**Não-terminais afetados:** `<LISTA_FUNC>`, `<FUNCAO>`

**Descrição:**
A expressão atribuída ao nome da função (que representa o retorno) deve ter tipo compatível com o tipo de retorno declarado.

**Pseudocódigo:**
```python
def verificar_tipo_retorno(nome_funcao, expressao_retorno):
    funcao = buscar_funcao(nome_funcao)
    tipo_declarado = funcao.tipo_retorno
    tipo_retornado = inferir_tipo(expressao_retorno)
    if not tipos_compativeis(tipo_declarado, tipo_retornado):
        erro_semantico(f"Função '{nome_funcao}' deve retornar {tipo_declarado}, "
                      f"mas está retornando {tipo_retornado}")
```

**Exemplo de erro:**
```pascal
function dobro(x: integer) : integer;
var resultado : real;
begin
  resultado := x * 2.5;
  dobro := resultado;    {# ERRO R7: deve retornar integer, mas retorna real #}
end;
```

---

### **R8: Só pode usar índice ([]) em variáveis do tipo vetor**

**Não-terminais afetados:** `<NOME>`

**Descrição:**
O operador de indexação `[]` só pode ser aplicado a variáveis declaradas como arrays.

**Pseudocódigo:**
```python
def verificar_acesso_array(nome, indice):
    simbolo = buscar_na_tabela(nome)
    if not simbolo.tipo.startswith('array'):
        erro_semantico(f"'{nome}' não é um array, não pode usar índice []")
    tipo_indice = inferir_tipo(indice)
    if tipo_indice != 'integer':
        erro_semantico("Índice de array deve ser do tipo integer")
```

**Exemplo de erro:**
```pascal
var 
  A : integer;
  B : array[10] of integer;
begin
  A[5] := 10;    {# ERRO R8: 'A' não é array, não pode usar [] #}
  B[5] := 10;    {# OK: 'B' é array #}
end.
```

---

### **R9: Só pode usar membros (.) em variáveis do tipo classe/record**

**Não-terminais afetados:** `<NOME>`

**Descrição:**
O operador de acesso a membro `.` só pode ser aplicado a variáveis declaradas como records.

**Pseudocódigo:**
```python
def verificar_acesso_membro(nome_objeto, nome_membro):
    simbolo = buscar_na_tabela(nome_objeto)
    if not simbolo.tipo.startswith('record'):
        erro_semantico(f"'{nome_objeto}' não é um record, não pode usar '.'")
    # Verifica se o membro existe no record (R10)
```

**Exemplo de erro:**
```pascal
var 
  A : integer;
  aluno : record
    nome : string;
    nota : real;
  end;
begin
  A.nome := "teste";      {# ERRO R9: 'A' não é record, não pode usar '.' #}
  aluno.nome := "João";   {# OK: 'aluno' é record #}
end.
```

---

### **R10: Só posso acessar membros de classe declarados**

**Não-terminais afetados:** `<NOME>`

**Descrição:**
Ao acessar um membro de um record, o membro deve existir na definição do record.

**Pseudocódigo:**
```python
def verificar_membro_existe(nome_objeto, nome_membro):
    simbolo = buscar_na_tabela(nome_objeto)
    definicao_record = obter_definicao_record(simbolo.tipo)
    if nome_membro not in definicao_record.membros:
        erro_semantico(f"Record '{nome_objeto}' não possui membro '{nome_membro}'")
```

**Exemplo de erro:**
```pascal
type
  aluno = record
    nome : string;
    nota : real;
  end;

var estudante : aluno;
begin
  estudante.nome := "Maria";      {# OK: 'nome' existe #}
  estudante.idade := 20;          {# ERRO R10: 'idade' não foi declarado #}
end.
```

---

## 📋 Resumo: Regras por Não-Terminal

### Declarações

| Não-Terminal | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|--------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| `<DEF_CONST_LIST>` | ✅ | | | | | | | | | |
| `<CONSTANTE>` | ✅ | | ✅ | | | | | | | |
| `<DEF_TIPOS_LIST>` | ✅ | | | | | | | | | |
| `<TIPO>` | ✅ | | | | | | | | | |
| `<DEF_VAR_LIST>` | ✅ | ✅ | | | | | | | | |
| `<VARIAVEL>` | ✅ | ✅ | | | | | | | | |
| `<LISTA_ID>` | ✅ | | | | | | | | | |
| `<LISTA_FUNC>` | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | | | |
| `<FUNCAO>` | ✅ | | | ✅ | ✅ | ✅ | ✅ | | | |
| `<NOME_FUNCAO>` | ✅ | | | ✅ | | | | | | |

### Comandos e Expressões

| Não-Terminal | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|--------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| `<ATRIBUICAO>` | | ✅ | ✅ | | | | | | | |
| `<IF>` | | | ✅ | | | | | | | |
| `<WHILE>` | | | ✅ | | | | | | | |
| `<CHAMADA>` | | ✅ | | ✅ | ✅ | ✅ | | | | |
| `<EXP_LOGICA>` | | | ✅ | | | | | | | |
| `<EXP_REL>` | | | ✅ | | | | | | | |
| `<EXP_AD>` | | | ✅ | | | | | | | |
| `<EXP_MUL>` | | | ✅ | | | | | | | |
| `<FATOR>` | | ✅ | ✅ | | | | | | | |
| `<NOME>` | | ✅ | | | | | | ✅ | ✅ | ✅ |

---

---

## Parte 2: Conjunto de Instruções de Código Intermediário (TAC)

Esta seção descreve todas as instruções do código intermediário de três endereços (Three-Address Code - TAC) geradas pelo compilador.

### 📊 Formato Geral

Cada instrução TAC segue o formato:
```
OPERAÇÃO  ENDEREÇO_1  ENDEREÇO_2  ENDEREÇO_3
```

Onde:
- **OPERAÇÃO**: Mnemônico da instrução
- **ENDEREÇO_1**: Primeiro operando (geralmente destino)
- **ENDEREÇO_2**: Segundo operando (opcional)
- **ENDEREÇO_3**: Terceiro operando (opcional)

---

## 📋 Tabela Completa de Instruções TAC

### 1. Instruções de Atribuição

| Instrução | Endereço 1 | Endereço 2 | Endereço 3 | Descrição | Exemplo |
|-----------|------------|------------|------------|-----------|---------|
| **ATR** | destino | origem | - | Atribuição simples: dest ← origem | `ATR A 5` → A := 5 |

**Semântica:**
```
ATR dest src
→ dest = src
```

**Exemplo Pascal → TAC:**
```pascal
A := 10;
```
```
ATR  A  10
```

---

### 2. Instruções Aritméticas

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **ADD** | resultado | op1 | op2 | Adição: res ← op1 + op2 | `ADD T1 A B` |
| **SUB** | resultado | op1 | op2 | Subtração: res ← op1 - op2 | `SUB T1 A B` |
| **MUL** | resultado | op1 | op2 | Multiplicação: res ← op1 * op2 | `MUL T1 A B` |
| **DIV** | resultado | op1 | op2 | Divisão: res ← op1 / op2 | `DIV T1 A B` |

**Semântica:**
```
ADD dest op1 op2
→ dest = op1 + op2
```

**Exemplo Pascal → TAC:**
```pascal
C := A + B * 2;
```
```
MUL  T1  B    2
ADD  T2  A    T1
ATR  C   T2
```

---

### 3. Instruções de Comparação e Lógica

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **EQ** | resultado | op1 | op2 | Igualdade: res ← (op1 = op2) | `EQ T1 A B` |
| **NE** | resultado | op1 | op2 | Diferença: res ← (op1 <> op2) | `NE T1 A B` |
| **LT** | resultado | op1 | op2 | Menor que: res ← (op1 < op2) | `LT T1 A B` |
| **LE** | resultado | op1 | op2 | Menor igual: res ← (op1 <= op2) | `LE T1 A B` |
| **GT** | resultado | op1 | op2 | Maior que: res ← (op1 > op2) | `GT T1 A B` |
| **GE** | resultado | op1 | op2 | Maior igual: res ← (op1 >= op2) | `GE T1 A B` |
| **AND** | resultado | op1 | op2 | E lógico: res ← op1 AND op2 | `AND T1 A B` |
| **OR** | resultado | op1 | op2 | OU lógico: res ← op1 OR op2 | `OR T1 A B` |
| **NOT** | resultado | op | - | NÃO lógico: res ← NOT op | `NOT T1 A` |

**Semântica:**
```
EQ dest op1 op2
→ dest = (op1 == op2) ? 1 : 0
```

**Exemplo Pascal → TAC:**
```pascal
resultado := (A > B) and (C < D);
```
```
GT   T1  A  B
LT   T2  C  D
AND  T3  T1 T2
ATR  resultado T3
```

---

### 4. Instruções de Controle de Fluxo

#### 4.1 Saltos Incondicionais

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **JMP** | label | - | - | Salto incondicional para label | `JMP L1` |
| **LABEL** | nome | - | - | Define um rótulo | `LABEL L1` |

**Semântica:**
```
JMP label
→ goto label

LABEL nome
→ nome:
```

---

#### 4.2 Saltos Condicionais

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **JZ** | label | var | - | Salta se var = 0 (falso) | `JZ L1 T1` |
| **JNZ** | label | var | - | Salta se var ≠ 0 (verdadeiro) | `JNZ L1 T1` |
| **JEQ** | label | op1 | op2 | Salta se op1 = op2 | `JEQ L1 A B` |
| **JNE** | label | op1 | op2 | Salta se op1 ≠ op2 | `JNE L1 A B` |
| **JLT** | label | op1 | op2 | Salta se op1 < op2 | `JLT L1 A B` |
| **JLE** | label | op1 | op2 | Salta se op1 <= op2 | `JLE L1 A B` |
| **JGT** | label | op1 | op2 | Salta se op1 > op2 | `JGT L1 A B` |
| **JGE** | label | op1 | op2 | Salta se op1 >= op2 | `JGE L1 A B` |

**Semântica:**
```
JZ label var
→ if (var == 0) goto label

JGT label op1 op2
→ if (op1 > op2) goto label
```

**Exemplo Pascal → TAC:**
```pascal
if A > B then
  C := 1
else
  C := 0;
```
```
GT      T1   A    B
JZ      L1   T1        {# se falso, vai para else #}
ATR     C    1
JMP     L2
LABEL   L1             {# else #}
ATR     C    0
LABEL   L2             {# fim if #}
```

---

### 5. Instruções de Função

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **PARAM** | arg | - | - | Passa parâmetro para função | `PARAM A` |
| **CALL** | função | nargs | - | Chama função com nargs parâmetros | `CALL soma 2` |
| **RETURN** | valor | - | - | Retorna valor de função | `RETURN T1` |

**Semântica:**
```
PARAM arg
→ push arg to stack

CALL func nargs
→ call func with nargs parameters

RETURN value
→ return value from function
```

**Exemplo Pascal → TAC:**
```pascal
function soma(a: integer; b: integer) : integer;
begin
  soma := a + b;
end;

begin
  resultado := soma(5, 3);
end.
```
```
{# Definição da função #}
LABEL   FUNC_soma
ADD     T1       a       b
ATR     soma     T1
RETURN  soma

{# Chamada da função #}
LABEL   MAIN
PARAM   5
PARAM   3
CALL    FUNC_soma  2
ATR     T2       RETVAL
ATR     resultado T2
```

---

### 6. Instruções de Entrada/Saída

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **READ** | var | - | - | Lê valor da entrada para var | `READ A` |
| **WRITE** | valor | - | - | Escreve valor na saída | `WRITE A` |

**Semântica:**
```
READ var
→ var = input()

WRITE value
→ output(value)
```

**Exemplo Pascal → TAC:**
```pascal
begin
  read(A);
  write(A);
end.
```
```
READ   A
WRITE  A
```

---

### 7. Instruções de Controle de Programa

| Instrução | End_1 | End_2 | End_3 | Descrição | Exemplo |
|-----------|-------|-------|-------|-----------|---------|
| **HALT** | - | - | - | Encerra o programa | `HALT` |
| **NOP** | - | - | - | Nenhuma operação (placeholder) | `NOP` |

**Semântica:**
```
HALT
→ exit program

NOP
→ do nothing
```

---

## 📋 Resumo das Instruções por Categoria

### Categorias

| Categoria | Instruções | Quantidade |
|-----------|-----------|------------|
| **Atribuição** | ATR | 1 |
| **Aritméticas** | ADD, SUB, MUL, DIV | 4 |
| **Comparação** | EQ, NE, LT, LE, GT, GE | 6 |
| **Lógicas** | AND, OR, NOT | 3 |
| **Controle** | JMP, LABEL, JZ, JNZ, JEQ, JNE, JLT, JLE, JGT, JGE | 10 |
| **Funções** | PARAM, CALL, RETURN | 3 |
| **I/O** | READ, WRITE | 2 |
| **Sistema** | HALT, NOP | 2 |
| **TOTAL** | | **31 instruções** |

---

## 🎯 Exemplos Completos de Tradução

### Exemplo 1: Expressão Aritmética

**Pascal:**
```pascal
program exemplo1;
var A, B, C : integer;
begin
  A := 5;
  B := 10;
  C := A + B * 2;
end.
```

**TAC Gerado:**
```
1.  LABEL    MAIN
2.  ATR      A         5
3.  ATR      B         10
4.  MUL      T1        B         2
5.  ADD      T2        A         T1
6.  ATR      C         T2
7.  HALT
```

---

### Exemplo 2: Estrutura IF-THEN-ELSE

**Pascal:**
```pascal
program exemplo2;
var A, B, maior : integer;
begin
  read(A);
  read(B);
  if A > B then
    maior := A
  else
    maior := B;
  write(maior);
end.
```

**TAC Gerado:**
```
1.  LABEL    MAIN
2.  READ     A
3.  READ     B
4.  GT       T1        A         B
5.  JZ       L1        T1
6.  ATR      maior     A
7.  JMP      L2
8.  LABEL    L1
9.  ATR      maior     B
10. LABEL    L2
11. WRITE    maior
12. HALT
```

---

### Exemplo 3: Laço WHILE

**Pascal:**
```pascal
program exemplo3;
var i, soma : integer;
begin
  i := 1;
  soma := 0;
  while i < 10 do
  begin
    soma := soma + i;
    i := i + 1;
  end;
  write(soma);
end.
```

**TAC Gerado:**
```
1.  LABEL    MAIN
2.  ATR      i         1
3.  ATR      soma      0
4.  LABEL    L1
5.  LT       T1        i         10
6.  JZ       L2        T1
7.  ADD      T2        soma      i
8.  ATR      soma      T2
9.  ADD      T3        i         1
10. ATR      i         T3
11. JMP      L1
12. LABEL    L2
13. WRITE    soma
14. HALT
```

---

### Exemplo 4: Função com Parâmetros

**Pascal:**
```pascal
program exemplo4;
var resultado : integer;

function multiplicar(a: integer; b: integer) : integer;
begin
  multiplicar := a * b;
end;

begin
  resultado := multiplicar(6, 7);
  write(resultado);
end.
```

**TAC Gerado:**
```
1.  LABEL    FUNC_multiplicar
2.  MUL      T1        a         b
3.  ATR      multiplicar T1
4.  RETURN   multiplicar

5.  LABEL    MAIN
6.  PARAM    6
7.  PARAM    7
8.  CALL     FUNC_multiplicar  2
9.  ATR      T2        RETVAL
10. ATR      resultado T2
11. WRITE    resultado
12. HALT
```

---

### Exemplo 5: Expressões Lógicas Complexas

**Pascal:**
```pascal
program exemplo5;
var A, B, C : integer;
var resultado : boolean;
begin
  A := 5;
  B := 10;
  C := 3;
  resultado := (A > C) and (B > A);
  if resultado then
    write(1)
  else
    write(0);
end.
```

**TAC Gerado:**
```
1.  LABEL    MAIN
2.  ATR      A         5
3.  ATR      B         10
4.  ATR      C         3
5.  GT       T1        A         C
6.  GT       T2        B         A
7.  AND      T3        T1        T2
8.  ATR      resultado T3
9.  JZ       L1        resultado
10. WRITE    1
11. JMP      L2
12. LABEL    L1
13. WRITE    0
14. LABEL    L2
15. HALT
```

---

## 📌 Convenções e Observações

### Temporários
- Formato: `T1`, `T2`, `T3`, ..., `Tn`
- Gerados automaticamente pelo compilador
- Usados para armazenar resultados intermediários

### Labels
- Formato: `L1`, `L2`, `L3`, ..., `Ln`
- Gerados automaticamente para estruturas de controle
- Formato especial: `FUNC_nome` para funções

### Valores Especiais
- **RETVAL**: Variável especial que armazena o valor de retorno de uma função
- **MAIN**: Label obrigatório para o início do programa principal

### Tipos de Operandos
Os endereços podem ser:
- **Variáveis**: `A`, `B`, `soma`, `resultado`
- **Constantes**: `5`, `10`, `3.14`, `"texto"`
- **Temporários**: `T1`, `T2`, `T3`
- **Labels**: `L1`, `L2`, `MAIN`, `FUNC_soma`

---

## ✅ Checklist de Instruções Implementadas

- [x] **Atribuição**: ATR
- [x] **Aritméticas**: ADD, SUB, MUL, DIV
- [x] **Comparação**: EQ, NE, LT, LE, GT, GE
- [x] **Lógicas**: AND, OR, NOT
- [x] **Saltos**: JMP, JZ, JNZ, JEQ, JNE, JLT, JLE, JGT, JGE
- [x] **Labels**: LABEL
- [x] **Funções**: PARAM, CALL, RETURN
- [x] **I/O**: READ, WRITE
- [x] **Sistema**: HALT, NOP

**Total: 31 instruções implementadas** ✅

---

**📚 Referências:**
- Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"
- Código implementado em `tac_generator.py`
- Exemplos práticos em `exemplo1_simples.pas`, `exemplo2_controle.pas`, `exemplo3_funcao.pas`
