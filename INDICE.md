# 📑 Índice Geral do Projeto - Compilador Pascal Simplificado

## 🎯 Navegação Rápida

### 📖 Para Começar
1. **Leia primeiro:** [`README.md`](README.md)
2. **Execute:** `python main_completo.py`
3. **Teste com:** `exemplo1_simples.pas`

### 📚 Documentação Completa

| Arquivo | Conteúdo | Quando Ler |
|---------|----------|------------|
| **README.md** | Visão geral e instruções rápidas | 👈 **COMECE AQUI** |
| **RELATORIO_COMPILADOR.md** | Relatório das 4 etapas (detalhado) | Para avaliação acadêmica |
| **GUIA_DE_USO.md** | Manual prático com exemplos | Para usar o compilador |
| **CORRECOES_GRAMATICA.md** | Análise das correções | Para entender a gramática |

### 💻 Código-Fonte

| Arquivo | Função | Status |
|---------|--------|--------|
| **`main_completo.py`** | Interface principal **[USAR ESTE]** | ⭐ Atualizado |
| `tac_generator.py` | Gerador de código intermediário | ✅ Novo |
| `parser.py` | Análise sintática + semântica | ✅ Original |
| `lexer.py` | Análise léxica | ✅ Original |
| `ast_nodes.py` | Definições da AST | ✅ Original |
| `ast_exporter.py` | Exportação JSON/DOT | ✅ Original |

### 🧪 Exemplos de Teste

| Arquivo | Testa | Complexidade |
|---------|-------|--------------|
| `exemplo1_simples.pas` | Expressões aritméticas | ⭐ Básico |
| `exemplo2_controle.pas` | IF-THEN-ELSE e WHILE | ⭐⭐ Intermediário |
| `exemplo3_funcao.pas` | Funções com parâmetros | ⭐⭐⭐ Avançado |

---

## 📋 Sumário Executivo

### ✅ O Que Foi Implementado

#### 1️⃣ **Análise Léxica** (lexer.py)
- Reconhecimento de 35+ tipos de tokens
- Palavras-chave, identificadores, operadores
- Números inteiros e reais
- Strings e comentários
- Rastreamento de linha e coluna

#### 2️⃣ **Análise Sintática** (parser.py)
- Parser recursivo descendente
- Gramática LL(1) sem ambiguidades
- Construção da AST
- Precedência de operadores correta

#### 3️⃣ **Análise Semântica** (integrada no parser.py)
- Tabela de símbolos com escopos aninhados
- Verificação de declaração antes do uso
- Compatibilidade de tipos
- Validação de parâmetros de funções
- 8 regras semânticas implementadas

#### 4️⃣ **Código Intermediário** (tac_generator.py) ⭐ **NOVO!**
- Formato de 3 endereços (TAC)
- 15+ tipos de instruções
- Geração de temporários e labels
- Suporte completo a:
  - Expressões aritméticas e lógicas
  - Estruturas de controle (IF, WHILE)
  - Funções e chamadas
  - I/O (READ, WRITE)

### 📊 Estatísticas

```
Linhas de Código:     ~2500
Módulos Python:       7 arquivos
Tokens Suportados:    35+ tipos
Produções Gramaticais: 40+
Regras Semânticas:    8 principais
Instruções TAC:       15+ tipos
```

### 🎓 Conceitos Implementados

✅ Teoria de Compiladores
- Análise léxica com expressões regulares
- Gramáticas livres de contexto
- Eliminação de ambiguidades
- Análise LL(1)
- Parser recursivo descendente

✅ Estruturas de Dados
- Árvores (AST)
- Tabela hash (símbolos)
- Pilha (escopos)

✅ Análise Semântica
- Verificação de tipos
- Escopo léxico
- Sistemas de tipos

✅ Código Intermediário
- Three-Address Code (TAC)
- Geração de código
- Otimização (preparado para)

---

## 📝 As 4 Etapas do Trabalho

### Etapa 1: Classificação e Gramática
📄 **Documento:** `RELATORIO_COMPILADOR.md` (Seção: Etapa 1)  
📄 **Detalhes:** `CORRECOES_GRAMATICA.md`

**Conteúdo:**
- ✅ Tabela de tokens com expressões regulares
- ✅ Gramática original identificada
- ✅ Ambiguidades detectadas (dangling else)
- ✅ Recursividade à esquerda eliminada
- ✅ Gramática corrigida (LL(1))

### Etapa 2: Implementação
📄 **Documento:** `RELATORIO_COMPILADOR.md` (Seção: Etapa 2)  
💻 **Código:** `lexer.py`, `parser.py`, `ast_nodes.py`

**Conteúdo:**
- ✅ Analisador léxico completo
- ✅ Analisador sintático funcional
- ✅ Construção da AST
- ✅ Análise semântica integrada

### Etapa 3: Regras Semânticas
📄 **Documento:** `RELATORIO_COMPILADOR.md` (Seção: Etapa 3)  
💻 **Código:** `parser.py` (classe SymbolTable, métodos semânticos)

**Conteúdo:**
- ✅ Mapeamento de regras para produções
- ✅ Implementação da tabela de símbolos
- ✅ Verificações de tipo
- ✅ Validação de escopo
- ✅ Verificação de parâmetros

### Etapa 4: Código Intermediário
📄 **Documento:** `RELATORIO_COMPILADOR.md` (Seção: Etapa 4)  
💻 **Código:** `tac_generator.py`  ⭐ **NOVO!**

**Conteúdo:**
- ✅ Definição do formato TAC
- ✅ Instruções de 3 endereços
- ✅ Gerador completo implementado
- ✅ Exemplos de código gerado
- ✅ Otimizações possíveis identificadas

---

## 🚀 Quick Start - 3 Passos

### 1️⃣ Abra o Terminal
```bash
cd pasta_do_projeto
```

### 2️⃣ Execute o Compilador
```bash
python main_completo.py
```

### 3️⃣ Escolha a Opção 4
```
Opção: 4
Caminho: exemplo1_simples.pas
```

**Resultado:** Verá as 4 etapas em ação! 🎉

---

## 📊 Mapa de Leitura Sugerido

### Para Avaliadores Acadêmicos

```
1. README.md                     (5 min)  - Visão geral
   ↓
2. RELATORIO_COMPILADOR.md       (30 min) - Trabalho completo
   ├── Etapa 1: Tokens e gramática
   ├── Etapa 2: Implementação
   ├── Etapa 3: Regras semânticas
   └── Etapa 4: Código intermediário
   ↓
3. CORRECOES_GRAMATICA.md        (10 min) - Detalhes das correções
   ↓
4. Executar: python main_completo.py  (15 min) - Testar exemplos
   ↓
5. Analisar código-fonte          (30 min) - Implementação
```

**Tempo Total:** ~90 minutos

### Para Usuários

```
1. README.md                      (5 min)  - Como usar
   ↓
2. GUIA_DE_USO.md                (15 min) - Exemplos práticos
   ↓
3. Executar: python main_completo.py (20 min) - Prática
```

**Tempo Total:** ~40 minutos

---

## 🎯 Destaques do Projeto

### 🌟 Pontos Fortes

1. **Implementação Completa**
   - Todas as 4 etapas funcionando
   - Código limpo e bem documentado
   - Testes incluídos

2. **Análise Semântica Robusta**
   - 8 regras implementadas
   - Tabela de símbolos com escopos
   - Mensagens de erro claras

3. **Código Intermediário (TAC)**
   - Gerador completo e funcional
   - Formato padronizado
   - Pronto para otimização

4. **Documentação Excelente**
   - 4 arquivos MD detalhados
   - Exemplos práticos
   - Código comentado

### 🔧 Recursos Extras

- ✅ Exportação de AST (JSON/DOT)
- ✅ Visualização gráfica da árvore
- ✅ Menu interativo amigável
- ✅ Múltiplos exemplos de teste
- ✅ Tratamento de erros robusto

---

## 📞 Estrutura de Suporte

### Se você está...

**🎓 Avaliando o trabalho acadêmico:**
→ Leia `RELATORIO_COMPILADOR.md`

**💻 Querendo usar o compilador:**
→ Leia `GUIA_DE_USO.md`

**🔍 Entendendo a gramática:**
→ Leia `CORRECOES_GRAMATICA.md`

**⚡ Com pressa:**
→ Leia `README.md` e execute os exemplos

**🐛 Encontrou um erro:**
→ Verifique os exemplos em `GUIA_DE_USO.md`

---

## ✅ Checklist Final

### Documentação
- [x] README.md com visão geral
- [x] RELATORIO_COMPILADOR.md (4 etapas)
- [x] GUIA_DE_USO.md (manual prático)
- [x] CORRECOES_GRAMATICA.md (análise técnica)
- [x] Este índice (INDICE.md)

### Código
- [x] Analisador léxico
- [x] Analisador sintático
- [x] Análise semântica
- [x] Gerador de código TAC
- [x] Interface principal

### Testes
- [x] Exemplo básico
- [x] Exemplo com controle
- [x] Exemplo com funções

### Extras
- [x] Exportação de AST
- [x] Código comentado
- [x] Menu interativo

---

## 🎉 Conclusão

Este projeto implementa um **compilador completo e funcional** para Pascal simplificado, incluindo todas as etapas desde a análise léxica até a geração de código intermediário.

**Principais Conquistas:**
- ✅ Gramática corrigida sem ambiguidades
- ✅ Parser recursivo descendente eficiente
- ✅ Análise semântica robusta
- ✅ Geração de código TAC funcional
- ✅ Documentação completa e clara

**Pronto para:**
- Avaliação acadêmica
- Uso prático
- Extensões futuras (otimização, geração de código de máquina)

---

**👥 Autores:** Kassiano Vieira e Claudio Nunes  
**📅 Data:** Novembro 2025  
**🎓 Disciplina:** Compiladores

---

**🚀 Comece pelo README.md e boa sorte! 🚀**
