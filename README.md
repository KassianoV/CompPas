# 🎓 Compilador Pascal Simplificado - Projeto Completo

> **Trabalho Acadêmico de Compiladores**
> **Autores:** Kassiano Vieira e Claudio Nunes
> **Data:** Dezembro 2025

## 📋 Resumo do Projeto

Este projeto implementa um compilador completo para uma versão simplificada da linguagem Pascal, incluindo:

1.  **Análise Léxica** - Reconhecimento de tokens
2.  **Análise Sintática** - Construção da AST (Árvore Sintática Abstrata)
3.  **Análise Semântica** - Verificação de tipos, escopos e regras
4.  **Geração de Código Intermediário** - TAC (Three-Address Code)
5.  **Otimização de Código** - 5 técnicas de otimização implementadas (EXTRA!)

### Destaques do Projeto ⭐

- **Interface Interativa** - Menu amigável com 10 opções de uso
- **Exportação de AST** - Formatos JSON e DOT (visualização gráfica)
- **Código Otimizado** - Sistema de otimização com comparação visual
- **Documentação Completa** - Guias detalhados e exemplos práticos
- **Testes Inclusos** - 4 arquivos de exemplo prontos para uso

### 💻 Código-Fonte
- **`lexer.py`** - Analisador Léxico
- **`parser.py`** - Analisador Sintático + Semântico
- **`ast_nodes.py`** - Definição dos nós da AST
- **`ast_exporter.py`** - Exportador de AST (JSON/DOT)
- **`ast_to_png.py`** - Conversor de AST para PNG
- **`tac_generator.py`** - Gerador de Código Intermediário (TAC)
- **`optimizer.py`** - Otimizador de Código TAC
- **`test_optimizer.py`** - Testes do otimizador
- **`main_menu.py`** - Interface principal atualizada

### 🧪 Exemplos de Teste
- **`exemplo.pas`** / **`exemplo1.pas`** - Programa básico com expressões
- **`exemplo2.pas`** - Estruturas de controle (IF e WHILE)
- **`exemplo3.pas`** - Funções e chamadas de função
- **`exemplo_otimizacao.pas`** - ✨ Demonstração de otimizações de código

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Nenhuma biblioteca externa necessária

### Execução Passo a Passo


#### 2️⃣ Executar o Compilador
```bash
# Execute o compilador interativo
python main_menu.py
```

#### 3️⃣ Usar o Menu Interativo

```
═══════════════════════════════════════════════════════════════════
               COMPILADOR PASCAL SIMPLIFICADO
═══════════════════════════════════════════════════════════════════
ANÁLISE:
  1 - Testar apenas Léxico (tokens)
  2 - Testar apenas Sintático (AST)
  3 - Testar Sintático + Semântico
  4 - Processar completo (Léxico + Sintático + Semântico + TAC) ⭐

GERAÇÃO DE CÓDIGO:
  5 - Gerar código intermediário (TAC) da última AST
  6 - Otimizar código TAC (aplica todas as otimizações) ✨
  7 - Comparar código original vs otimizado

EXPORTAÇÃO:
  8 - Exportar AST (JSON / DOT)
  9 - Exportar código TAC original
 10 - Exportar código TAC otimizado

  0 - Sair
═══════════════════════════════════════════════════════════════════
```

**Recomendação:** Use a **Opção 4** para processamento completo!

## 📖 Guia Completo de Uso

### Exemplo 1: Processo Completo Passo a Passo

#### Passo 1: Criar arquivo Pascal

Crie um arquivo chamado `teste.pas`:
```pascal
program teste;
var
  A, B, resultado : integer;
begin
  A := 5;
  B := 10;
  resultado := A + B * 2;
  write(resultado);
end.
```

#### Passo 2: Executar o compilador

```bash
python main_completo.py
```

Você verá o menu. Digite **4** para processar completo.

#### Passo 3: Informar o arquivo

```
Escolha uma opção: 4
Informe o caminho do arquivo .pas: teste.pas
```

#### Passo 4: Ver os resultados

```
📂 Carregando arquivo: teste.pas

📝 Código fonte (78 caracteres):
----------------------------------------------------------------------
  1: program teste;
  2: var
  3:   A, B, resultado : integer;
  4: begin
  5:   A := 5;
  6:   B := 10;
  7:   resultado := A + B * 2;
  8:   write(resultado);
  9: end.
----------------------------------------------------------------------

🔍 ETAPA 1: Análise Léxica
✅ 25 tokens identificados

🔍 ETAPA 2: Análise Sintática e Semântica
✅ AST construída com sucesso
✅ Verificações semânticas concluídas

🔍 ETAPA 3: Geração de Código Intermediário
═══════════════════════════════════════════════════════════════════
                    CÓDIGO INTERMEDIÁRIO (TAC)
═══════════════════════════════════════════════════════════════════
Nº    OPERAÇÃO   ENDEREÇO 1    ENDEREÇO 2    ENDEREÇO 3
───────────────────────────────────────────────────────────────────
1     LABEL      MAIN
2     ATR        A             5
3     ATR        B             10
4     MUL        T1            B             2
5     ADD        T2            A             T1
6     ATR        resultado     T2
7     WRITE      resultado
8     HALT
═══════════════════════════════════════════════════════════════════
✅ 8 instruções TAC geradas
```

---

### Exemplo 2: Gerando e Visualizando a Árvore AST 🌳

#### Passo 1: Exportar a AST

Após processar o arquivo (opção 4), escolha a **opção 8** para exportar:

```
Escolha uma opção: 8
```

Resultado:
```
✅ AST exportada com sucesso!
  → export/ast.json
  → export/ast.dot (visualize em https://dreampuf.github.io/GraphvizOnline/)
```

#### Passo 2: Visualizar no Terminal (formato texto)

A AST já é exibida no terminal durante a análise sintática:
```
===== ÁRVORE SINTÁTICA ABSTRATA =====
Program(name='teste')
  Declarações:
    VarDecl(names=['A', 'B', 'resultado'], type=integer)
  Bloco principal:
    Compound:
      Assign:
        Var(name='A')
        Num(value=5)
      Assign:
        Var(name='B')
        Num(value=10)
      Assign:
        Var(name='resultado')
        BinOp(op='+')
          Var(name='A')
          BinOp(op='*')
            Var(name='B')
            Num(value=2)
      Call(name='write')
        Var(name='resultado')
=====================================
```

#### Passo 3: Visualizar Graficamente (formato gráfico) 🎨

1. **Abra o arquivo exportado:**
   - Navegue até a pasta `export/`
   - Abra o arquivo `ast.dot` em um editor de texto

2. **Copie o conteúdo** (exemplo):
   ```dot
   digraph AST {
     node [shape=box];
     node1 [label="Program\nteste"];
     node2 [label="VarDecl\nA, B, resultado : integer"];
     node3 [label="Compound"];
     node4 [label="Assign"];
     node5 [label="Var\nA"];
     node6 [label="Num\n5"];
     node1 -> node2;
     node1 -> node3;
     node3 -> node4;
     node4 -> node5;
     node4 -> node6;
     ...
   }
   ```

3. **Visualize online:**
   - Acesse: https://dreampuf.github.io/GraphvizOnline/
   - Cole o conteúdo do arquivo `ast.dot`
   - Veja a árvore renderizada graficamente!

4. **Ou use o Graphviz local** (se instalado):
   ```bash
   dot -Tpng export/ast.dot -o arvore.png
   ```
   Isso gera uma imagem PNG da árvore.

#### Formatos de Exportação da AST

| Formato | Arquivo | Uso |
|---------|---------|-----|
| **JSON** | `export/ast.json` | Processamento programático, análise detalhada |
| **DOT** | `export/ast.dot` | Visualização gráfica, documentação |

---

### Exemplo 3: Otimização de Código ✨

#### Passo 1: Processar um arquivo com expressões redundantes

Crie `exemplo_otimizacao.pas`:
```pascal
program otimizacao;
var
  x, y, z : integer;
begin
  x := 2 + 3;
  y := x;
  z := y + 0;
  write(z);
end.
```

#### Passo 2: Gerar código TAC

Execute e escolha **opção 4**:
```
Escolha uma opção: 4
Informe o caminho do arquivo .pas: exemplo_otimizacao.pas
```

#### Passo 3: Otimizar o código

Escolha **opção 6**:
```
Escolha uma opção: 6
```

Você verá:
```
🔧 OTIMIZANDO CÓDIGO INTERMEDIÁRIO...
======================================================================

📋 CÓDIGO ORIGINAL:
----------------------------------------------------------------------
Nº    OPERAÇÃO   ENDEREÇO 1    ENDEREÇO 2    ENDEREÇO 3
----------------------------------------------------------------------
1     LABEL      MAIN
2     ADD        T1            2             3
3     ATR        x             T1
4     ATR        y             x
5     ADD        T2            y             0
6     ATR        z             T2
7     WRITE      z
8     HALT

✅ Constant Folding: 1 otimizações aplicadas
✅ Constant Propagation: 2 substituições
✅ Copy Propagation: 1 cópias propagadas
✅ Dead Code Elimination: 3 instruções removidas

📋 CÓDIGO OTIMIZADO:
----------------------------------------------------------------------
Nº    OPERAÇÃO   ENDEREÇO 1    ENDEREÇO 2    ENDEREÇO 3
----------------------------------------------------------------------
1     LABEL      MAIN
2     ATR        x             5
3     ATR        z             5
4     WRITE      z
5     HALT
```

#### Passo 4: Comparar lado a lado

Escolha **opção 7**:
```
Escolha uma opção: 7
```

Verá uma comparação visual:
```
======================================================================
                    COMPARAÇÃO DE CÓDIGO TAC
======================================================================

ORIGINAL                            | OTIMIZADO
-----------------------------------+------------------------------------
LABEL    MAIN                      | LABEL    MAIN
ADD      T1         2          3   | ATR      x          5
ATR      x          T1             | ATR      z          5
ATR      y          x              | WRITE    z
ADD      T2         y          0   | HALT
ATR      z          T2             |
WRITE    z                         |
HALT                               |
----------------------------------------------------------------------
Total de instruções: 8             | 5
Redução: 3 instruções (37.5%)
======================================================================
```

#### Passo 5: Exportar código otimizado

Escolha **opção 10**:
```
Escolha uma opção: 10

✅ Código TAC exportado com sucesso!
  → export/codigo_intermediario_otimizado.tac
```

## 📦 Arquivos Gerados

Ao exportar (opções 8, 9 e 10), são criados na pasta `export/`:

```
export/
├── ast.json                              # AST em formato JSON
├── ast.dot                               # AST em formato Graphviz DOT
├── codigo_intermediario.tac              # Código TAC original
└── codigo_intermediario_otimizado.tac    # Código TAC otimizado ✨
```

### Visualizar AST Graficamente
1. Abra https://dreampuf.github.io/GraphvizOnline/
2. Cole o conteúdo de `ast.dot`
3. Veja o gráfico da árvore renderizado

### Ou usando Graphviz Local
```bash
# Instale o Graphviz (se não tiver)
# Windows: choco install graphviz
# Linux: sudo apt-get install graphviz
# Mac: brew install graphviz

# Gere a imagem da árvore
dot -Tpng export/ast.dot -o arvore_exemplo.png
```

## 🔍 Testes Incluídos

### Exemplo 1: Programa Simples
**Arquivo:** `exemplo1.pas`
**Testa:** Atribuições e expressões aritméticas

### Exemplo 2: Estruturas de Controle
**Arquivo:** `exemplo2.pas`
**Testa:** IF-THEN-ELSE e WHILE-DO

### Exemplo 3: Funções
**Arquivo:** `exemplo3.pas`
**Testa:** Declaração e chamada de funções com parâmetros

### Exemplo 4: Otimizações ✨
**Arquivo:** `exemplo_otimizacao.pas`
**Testa:**
- Constant Folding (2 + 3 → 5)
- Copy Propagation (y := x → substituição direta)
- Operações com identidade (x + 0 → x)
- Dead Code Elimination (remoção de temporários não usados)

## 🐛 Erros Comuns

### Erro Léxico
```
❌ Caractere inesperado '$' na linha 5
```
**Solução:** Remova caracteres não suportados

### Erro Sintático
```
❌ Esperado PONT_VIRG, encontrado END
```
**Solução:** Adicione ponto-e-vírgula

### Erro Semântico
```
❌ Variável 'X' não foi declarada
```
**Solução:** Declare na seção `var`

## 🎓 Conceitos Implementados

### Gramática Livre de Contexto
- ✅ Remoção de ambiguidades (dangling else)
- ✅ Eliminação de recursividade à esquerda
- ✅ Fatoração de produções

### Tabela de Símbolos
- ✅ Estrutura hierárquica de escopos
- ✅ Inserção, busca e validação
- ✅ Suporte a funções e tipos customizados

### Código de Três Endereços
- ✅ Formato intermediário padronizado
- ✅ Geração de temporários
- ✅ Geração de labels
- ✅ Pronto para otimização

## 📊 Estatísticas do Projeto

- **Linhas de Código:** ~3500+ linhas
- **Módulos:** 9 arquivos Python principais
- **Tokens Reconhecidos:** 35+ tipos
- **Regras Gramaticais:** 40+ produções
- **Verificações Semânticas:** 8 regras principais
- **Instruções TAC:** 15+ tipos
- **Técnicas de Otimização:** 5 implementadas ✨

## 🔮 Possíveis Extensões Futuras

1. **Arrays e Records Completos**
   - Implementar acesso completo `a[i]` e `r.campo`
   - Suporte a arrays multidimensionais

2. **Otimizações Avançadas** (além das já implementadas)
   - Loop unrolling
   - Strength reduction
   - Register allocation
   - Peephole optimization

3. **Geração de Código de Máquina**
   - Tradução para Assembly MIPS
   - Ou Assembly x86/x64
   - Geração de executável final

4. **Interpretador TAC**
   - Executar código intermediário diretamente
   - Modo de depuração passo a passo
   - Visualização da memória e pilha

5. **IDE ou Editor Integrado**
   - Syntax highlighting para Pascal
   - Debugger visual
   - Análise em tempo real

## 👥 Autores

**Kassiano Vieira** e **Claudio Nunes**

## 📝 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

---

## 🎯 Checklist de Avaliação

### Etapa 1: Classificação e Gramática ✅
- [x] Tokens classificados
- [x] Expressões regulares definidas
- [x] Ambiguidades identificadas e corrigidas
- [x] Recursividade à esquerda eliminada

### Etapa 2: Implementação ✅
- [x] Analisador léxico funcional
- [x] Analisador sintático funcional
- [x] AST construída corretamente
- [x] Análise semântica integrada

### Etapa 3: Regras Semânticas ✅
- [x] Tabela de símbolos implementada
- [x] Verificação de escopo
- [x] Verificação de tipos
- [x] Validação de funções
- [x] Regras mapeadas para gramática

### Etapa 4: Código Intermediário ✅
- [x] Gerador TAC implementado
- [x] Instruções de 3 endereços
- [x] Geração de temporários
- [x] Geração de labels
- [x] Suporte a estruturas de controle
- [x] Suporte a funções

### Otimização de Código ✅ (Extra)
- [x] Simplificação de Constantes
- [x] Propagação de Constantes
- [x] Propagação de Cópias
- [x] Eliminação de Código Morto
- [x] Eliminação de Subexpressões Comuns (ESC)
- [x] Comparação visual de código
- [x] Exportação de código otimizado

---

## 🎯 Fluxo Completo de Compilação

```
┌─────────────────┐
│  Código Pascal  │
│   (teste.pas)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Análise Léxica  │  ← Gera tokens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Análise        │  ← Constrói AST
│  Sintática      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Análise        │  ← Verifica tipos, escopos
│  Semântica      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Geração TAC    │  ← Gera código intermediário
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Otimização     │  ← Aplica 5 técnicas de otimização ✨
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Código Final   │  ← Código TAC otimizado
└─────────────────┘
```

---

## ⚡ Dicas Rápidas de Uso

### Para iniciantes:
```bash
1. python main_completo.py
2. Digite "4" (Processar completo)
3. Digite o caminho do arquivo: exemplo1.pas
4. Veja todos os resultados de uma vez!
```

### Para visualizar a árvore AST:
```bash
1. Execute a opção 4 primeiro
2. Depois escolha a opção 8 (Exportar AST)
3. Abra https://dreampuf.github.io/GraphvizOnline/
4. Cole o conteúdo de export/ast.dot
python ast_to_png.py export/ast.json export/minha_arvore.png
```

### Para testar otimizações:
```bash
1. Execute a opção 4 com exemplo_otimizacao.pas
2. Escolha a opção 6 (Otimizar)
3. Escolha a opção 7 (Comparar)
4. Veja a redução de instruções!
```


# Ver conteúdo de um exemplo
type exemplo1.pas   # Windows
cat exemplo1.pas    # Linux/Mac
```

---