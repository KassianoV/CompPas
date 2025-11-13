# Guia de Uso do Compilador Pascal Simplificado

## Estrutura de Arquivos

```
projeto/
├── lexer.py                    # Analisador Léxico
├── parser.py                   # Analisador Sintático + Semântico
├── ast_nodes.py                # Definição dos nós da AST
├── ast_exporter.py             # Exportador de AST (JSON/DOT)
├── tac_generator.py            # Gerador de Código Intermediário (TAC)
├── main_completo.py            # Interface principal (USAR ESTE!)
├── regras.txt                  # Regras semânticas
├── RELATORIO_COMPILADOR.md     # Documentação completa
├── exemplo1_simples.pas        # Exemplo básico
├── exemplo2_controle.pas       # Exemplo com IF/WHILE
├── exemplo3_funcao.pas         # Exemplo com funções
└── export/                     # Pasta para arquivos exportados
    ├── ast.json
    ├── ast.dot
    └── codigo_intermediario.tac
```

## Como Executar

### 1. Executar o Compilador Interativo

```bash
python main_completo.py
```

Isso abrirá um menu com as seguintes opções:

```
1 - Testar apenas Léxico (tokens)
2 - Testar apenas Sintático (AST)
3 - Testar Sintático + Semântico
4 - Processar completo (Léxico + Sintático + Semântico + TAC)
5 - Gerar código intermediário (TAC) da última AST
6 - Exportar AST (JSON / DOT)
7 - Exportar código TAC
8 - Sair
```

### 2. Testar Cada Etapa Separadamente

#### Opção 1: Análise Léxica
- Mostra todos os tokens identificados
- Exibe linha, coluna, tipo e lexema
- Útil para verificar se todos os símbolos foram reconhecidos

#### Opção 2: Análise Sintática
- Constrói a AST sem verificações semânticas
- Mostra a estrutura hierárquica do programa
- Útil para verificar se a gramática está correta

#### Opção 3: Análise Sintática + Semântica
- Constrói a AST com todas as verificações semânticas
- Valida:
  - Declaração de variáveis antes do uso
  - Compatibilidade de tipos
  - Escopo de identificadores
  - Parâmetros de funções

#### Opção 4: Processamento Completo
- Executa todas as etapas em sequência:
  1. Análise Léxica
  2. Análise Sintática
  3. Análise Semântica
  4. Geração de Código Intermediário (TAC)
- **RECOMENDADO para verificação completa**

## Exemplos de Uso

### Exemplo 1: Programa Simples

Arquivo: `exemplo1_simples.pas`
```pascal
program exemplo_simples;
var
  A, B, C, resultado : integer;
begin
  A := 5;
  B := 10;
  C := 15;
  resultado := A + B * C;
end.
```

**Executar:**
```
Opção: 4
Caminho: exemplo1_simples.pas
```

**Código TAC Gerado:**
```
1. LABEL    MAIN
2. ATR      A          5
3. ATR      B          10
4. ATR      C          15
5. MUL      T1         B          C
6. ADD      T2         A          T1
7. ATR      resultado  T2
8. HALT
```

### Exemplo 2: Estruturas de Controle

Arquivo: `exemplo2_controle.pas`
```pascal
program exemplo_controle;
var
  i, soma, n : integer;
begin
  n := 10;
  soma := 0;
  i := 1;
  
  while i < n do
  begin
    if i > 5 then
      soma := soma + i
    else
      soma := soma + 1;
    i := i + 1;
  end;
  
  write(soma);
end.
```

**Código TAC Gerado:**
```
1.  LABEL    MAIN
2.  ATR      n          10
3.  ATR      soma       0
4.  ATR      i          1
5.  LABEL    L1         {# início do while #}
6.  LT       T1         i          n
7.  JZ       L2         T1         {# sai do while se falso #}
8.  GT       T2         i          5
9.  JZ       L3         T2         {# vai para else se falso #}
10. ADD      T3         soma       i
11. ATR      soma       T3
12. JMP      L4         {# pula o else #}
13. LABEL    L3         {# else #}
14. ADD      T4         soma       1
15. ATR      soma       T4
16. LABEL    L4         {# fim do if #}
17. ADD      T5         i          1
18. ATR      i          T5
19. JMP      L1         {# volta para início do while #}
20. LABEL    L2         {# fim do while #}
21. WRITE    soma
22. HALT
```

### Exemplo 3: Com Função

Arquivo: `exemplo3_funcao.pas`

**Código TAC Gerado:**
```
1.  LABEL    FUNC_soma
2.  ADD      T1         a          b
3.  ATR      soma       T1
4.  RETURN   soma

5.  LABEL    FUNC_fatorial
6.  ATR      fat        1
7.  ATR      i          2
8.  LABEL    L1
9.  LT       T2         i          n
10. JZ       L2         T2
11. MUL      T3         fat        i
12. ATR      fat        T3
13. ADD      T4         i          1
14. ATR      i          T4
15. JMP      L1
16. LABEL    L2
17. ATR      fatorial   fat
18. RETURN   fatorial

19. LABEL    MAIN
20. ATR      x          5
21. ATR      y          3
22. PARAM    x
23. PARAM    y
24. CALL     FUNC_soma  2
25. ATR      T5         RETVAL
26. ATR      resultado  T5
27. WRITE    resultado
28. PARAM    5
29. CALL     FUNC_fatorial 1
30. ATR      T6         RETVAL
31. ATR      resultado  T6
32. WRITE    resultado
33. HALT
```

## Verificações Semânticas Implementadas

### 1. Declaração Única por Escopo
```pascal
var A : integer;
var A : real;  {# ERRO: 'A' já foi declarado #}
```

### 2. Declaração Antes do Uso
```pascal
begin
  B := 5;      {# ERRO: 'B' não foi declarado #}
end.
```

### 3. Compatibilidade de Tipos
```pascal
var x : integer;
var y : real;
begin
  x := y;      {# OK: real pode ser atribuído a integer #}
  x := x + y;  {# OK: resultado é real #}
end.
```

### 4. Parâmetros de Função
```pascal
function soma(a: integer; b: integer) : integer;
begin
  soma := a + b;
end;

begin
  soma(5);           {# ERRO: esperava 2 parâmetros, recebeu 1 #}
  soma(5, "texto");  {# ERRO: tipo incompatível no parâmetro 2 #}
end.
```

## Exportação de Arquivos

### AST em JSON
Arquivo: `export/ast.json`
```json
{
  "type": "Program",
  "name": "exemplo_simples",
  "decls": [...],
  "block": {
    "type": "Compound",
    "statements": [...]
  }
}
```

### AST em DOT (Graphviz)
Arquivo: `export/ast.dot`

Para visualizar:
1. Abra https://dreampuf.github.io/GraphvizOnline/
2. Cole o conteúdo do arquivo
3. Veja o gráfico da árvore

### Código TAC
Arquivo: `export/codigo_intermediario.tac`

Formato legível para análise e otimização posterior.

## Erros Comuns e Soluções

### Erro Léxico
```
❌ Erro léxico: Caractere inesperado '$' na linha 5, coluna 10
```
**Solução:** Remova caracteres especiais não suportados

### Erro Sintático
```
❌ Erro sintático: Esperado token PONT_VIRG, mas encontrado END (end)
```
**Solução:** Adicione ponto-e-vírgula onde necessário

### Erro Semântico
```
❌ Erro Semântico: Variável 'X' não foi declarada
```
**Solução:** Declare a variável na seção `var`

## Gramática Suportada

### Estrutura do Programa
```
program <nome>;
[const ...]
[type ...]
[var ...]
[function ...]
begin
  <comandos>
end.
```

### Tipos Suportados
- `integer` - Números inteiros
- `real` - Números reais
- `boolean` - Booleanos (true/false)
- `string` - Strings entre aspas duplas

### Comandos
- Atribuição: `variavel := expressão;`
- Condicional: `if <cond> then <cmd> [else <cmd>]`
- Laço: `while <cond> do <cmd>`
- Leitura: `read(variavel)`
- Escrita: `write(expressão)`

### Expressões
- Aritméticas: `+`, `-`, `*`, `/`
- Relacionais: `=`, `<>`, `<`, `>`, `<=`, `>=`
- Lógicas: `and`, `or`, `not`
- Precedência correta implementada

### Comentários
```pascal
{# Isto é um comentário #}
```

## Próximos Passos (Extensões Futuras)

1. **Arrays e Records**
   - Suporte completo a acesso por índice `[i]`
   - Suporte a acesso a membros `.campo`

2. **Otimização do Código TAC**
   - Eliminação de código morto
   - Propagação de constantes
   - Eliminação de subexpressões comuns

3. **Geração de Código Assembly**
   - Tradução de TAC para MIPS/x86

4. **Interpretador**
   - Executar código TAC diretamente

5. **IDE Integrada**
   - Interface gráfica
   - Editor com syntax highlighting
   - Visualização da AST interativa

## Contato

**Autores:**
- Kassiano Vieira
- Claudio Nunes

**Instituição:** [Nome da Instituição]  
**Disciplina:** Compiladores  
**Ano:** 2025
