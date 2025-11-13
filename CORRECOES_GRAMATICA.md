# Correções da Gramática - Análise Detalhada

## 🔴 PROBLEMA 1: Ambiguidade Dangling Else

### Gramática Original (AMBÍGUA)
```
<COMANDO> → if <EXP> then <COMANDO>
          | if <EXP> then <COMANDO> else <COMANDO>
```

### Exemplo Ambíguo
```pascal
if A > 0 then 
  if B > 0 then 
    write(1) 
  else 
    write(2)
```

**Interpretação 1:**
```
if A > 0 then 
  [if B > 0 then write(1) else write(2)]
```

**Interpretação 2:**
```
if A > 0 then 
  [if B > 0 then write(1)]
else 
  write(2)
```

### ✅ Solução Implementada

```
<COMANDO> → <COMANDO_COMPLETO>
          | <COMANDO_INCOMPLETO>
          | <OUTROS_COMANDOS>

<COMANDO_COMPLETO> → if <EXP> then <COMANDO_COMPLETO> else <COMANDO_COMPLETO>
                   | <OUTROS_COMANDOS>

<COMANDO_INCOMPLETO> → if <EXP> then <COMANDO>
                     | if <EXP> then <COMANDO_INCOMPLETO> else <COMANDO_INCOMPLETO>
```

**Regra:** O `else` sempre se associa ao `if` mais próximo que ainda não tem `else`.

---

## 🔴 PROBLEMA 2: Recursividade à Esquerda

### Gramática Original (RECURSIVA À ESQUERDA)

```
<EXP_LOGICA> → <EXP_LOGICA> and <EXP_REL>
             | <EXP_LOGICA> or <EXP_REL>
             | <EXP_REL>

<EXP_AD> → <EXP_AD> + <EXP_MUL>
         | <EXP_AD> - <EXP_MUL>
         | <EXP_MUL>

<EXP_MUL> → <EXP_MUL> * <FATOR>
          | <EXP_MUL> / <FATOR>
          | <FATOR>
```

### ❌ Por que é um problema?

Em um parser recursivo descendente:

```
parse_exp_logica():
    parse_exp_logica()  # ← LOOP INFINITO!
    # ...
```

### ✅ Solução 1: Recursividade à Direita (Teórica)

```
<EXP_LOGICA> → <EXP_REL> <EXP_LOGICA_RESTO>
<EXP_LOGICA_RESTO> → and <EXP_REL> <EXP_LOGICA_RESTO>
                   | or <EXP_REL> <EXP_LOGICA_RESTO>
                   | ε
```

### ✅ Solução 2: Iteração (Implementada)

```
<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*

<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*

<EXP_MUL> → <FATOR> ( (*|/) <FATOR> )*
```

**Notação:**
- `( ... )*` = zero ou mais repetições
- `( ... )+` = uma ou mais repetições
- `( ... )?` = opcional (zero ou uma)

### Implementação no Parser

```python
def parse_expression(self):
    """<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*"""
    node = self.parse_relation()
    
    # Iteração ao invés de recursão à esquerda
    while self.match('AND', 'OR'):
        op = self.consume().lexeme
        right = self.parse_relation()
        node = BinOp(op, node, right)
    
    return node

def parse_simple_expression(self):
    """<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*"""
    node = self.parse_term()
    
    while self.peek() and self.peek().type == 'OP_MAT' and \
          self.peek().lexeme in ['+', '-']:
        op = self.consume('OP_MAT').lexeme
        right = self.parse_term()
        node = BinOp(op, node, right)
    
    return node
```

---

## 🔴 PROBLEMA 3: Fatoração de Listas

### Gramática Original (NÃO FATORADA)

```
<LISTA_CONST> → <CONSTANTE> <LISTA_CONST>
              | <CONSTANTE>

<LISTA_VAR> → <VARIAVEL> ; <LISTA_VAR>
            | <VARIAVEL>

<LISTA_ID> → <ID> , <LISTA_ID>
           | <ID>
```

### Problema: Decisão Ambígua

Ao ver `<CONSTANTE>`, qual produção escolher?
- Primeira: `<CONSTANTE> <LISTA_CONST>`
- Segunda: `<CONSTANTE>`

**Solução:** Lookahead de 1 token não é suficiente!

### ✅ Solução: Usar Iteração

```
<LISTA_CONST> → <CONSTANTE>+

<LISTA_VAR> → <VARIAVEL> ( ; <VARIAVEL> )*

<LISTA_ID> → <ID> ( , <ID> )*
```

### Implementação

```python
def parse_const_decl(self):
    """<DEF_CONST_LIST> → const <CONSTANTE>+"""
    self.consume('CONST')
    declarations = []
    
    # Uma ou mais constantes
    while not self.match('TYPE', 'VAR', 'FUNCTION', 'BEGIN'):
        name = self.consume('ID').lexeme
        self.consume('OP_ASSIGN')
        value = self.parse_const_value()
        self.consume('PONT_VIRG')
        declarations.append(ConstDecl(name, value))
    
    return declarations
```

---

## 🔴 PROBLEMA 4: Precedência de Operadores

### Hierarquia de Precedência (do menor para maior)

```
1. Operadores lógicos:  or, and
2. Operadores relacionais: =, <>, <, >, <=, >=
3. Operadores aditivos: +, -
4. Operadores multiplicativos: *, /
5. Operador unário: not
6. Primários: números, variáveis, parênteses
```

### Gramática para Precedência Correta

```
<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*
             ↓
<EXP_REL> → <EXP_AD> ( <OP_REL> <EXP_AD> )?
          ↓
<EXP_AD> → <EXP_MUL> ( (+|-) <EXP_MUL> )*
         ↓
<EXP_MUL> → <FATOR> ( (*|/) <FATOR> )*
          ↓
<FATOR> → <NUMERO>
        | <ID>
        | ( <EXP_LOGICA> )
        | not <FATOR>
```

### Exemplo: A + B * C

**Parsing:**
```
parse_expression()
  → parse_relation()
    → parse_simple_expression()
      → parse_term()  {A}
      → vê '+'
      → parse_term()
        → parse_factor() {B}
        → vê '*'
        → parse_factor() {C}
        → retorna BinOp('*', B, C)
      → retorna BinOp('+', A, BinOp('*', B, C))
```

**AST Gerada:**
```
    +
   / \
  A   *
     / \
    B   C
```

**TAC Gerado:**
```
MUL  T1  B  C
ADD  T2  A  T1
```

---

## 📊 Comparação: Antes vs Depois

### Expressões Lógicas

#### ❌ ANTES (Recursiva à Esquerda)
```
<EXP_LOGICA> → <EXP_LOGICA> and <EXP_REL>  # PROBLEMA!
             | <EXP_REL>
```

#### ✅ DEPOIS (Iterativa)
```
<EXP_LOGICA> → <EXP_REL> ( (and | or) <EXP_REL> )*
```

### Comandos IF-THEN-ELSE

#### ❌ ANTES (Ambíguo)
```
<COMANDO> → if <EXP> then <COMANDO>
          | if <EXP> then <COMANDO> else <COMANDO>
```

#### ✅ DEPOIS (Não Ambíguo)
```
<COMANDO> → <COMANDO_COMPLETO>
          | <COMANDO_INCOMPLETO>

<COMANDO_COMPLETO> → if <EXP> then <COMANDO_COMPLETO> else <COMANDO_COMPLETO>
                   | <OUTROS_COMANDOS>

<COMANDO_INCOMPLETO> → if <EXP> then <COMANDO>
```

### Listas

#### ❌ ANTES (Recursiva)
```
<LISTA_ID> → <ID> , <LISTA_ID>
           | <ID>
```

#### ✅ DEPOIS (Iterativa)
```
<LISTA_ID> → <ID> ( , <ID> )*
```

---

## 🎯 Resumo das Correções

| Problema | Solução | Técnica |
|----------|---------|---------|
| Dangling else | Comandos completos/incompletos | Separação de produções |
| Recursividade à esquerda | Iteração com while | Transformação em loop |
| Listas ambíguas | Notação `+` e `*` | Fatoração |
| Precedência | Hierarquia de não-terminais | Estruturação em níveis |

---

## ✅ Checklist de Verificação

### Gramática Corrigida
- [x] LL(1) - Sem recursividade à esquerda
- [x] Não ambígua - Dangling else resolvido
- [x] Fatorada - Listas com iteração
- [x] Precedência correta - Hierarquia implementada

### Parser
- [x] Recursivo descendente
- [x] Um procedimento por não-terminal
- [x] Lookahead de 1 token
- [x] Backtracking não necessário

### AST
- [x] Estrutura hierárquica correta
- [x] Precedência refletida na árvore
- [x] Pronta para análise semântica

---

## 📚 Referências

**Técnicas Utilizadas:**
1. Eliminação de recursividade à esquerda
2. Fatoração à esquerda
3. Resolução de ambiguidade (dangling else)
4. Análise LL(1)
5. Parser recursivo descendente

**Baseado em:**
- Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools"
- Teoria de Linguagens Formais e Autômatos
- Material didático da disciplina de Compiladores
