# Compilador para Pascal Simplificado

> Projeto acadêmico de um compilador para uma versão simplificada da linguagem Pascal. O projeto inclui um analisador léxico, sintático e a construção de uma Árvore Sintática Abstrata (AST), desenvolvido em Python sem dependências externas.

## Visão Geral

Este projeto implementa as fases iniciais (front-end) de um compilador. O objetivo é processar um código-fonte escrito em uma gramática específica de Pascal, verificar sua validade léxica e sintática e, por fim, gerar uma representação estruturada do código na forma de uma AST.

A AST gerada pode ser exportada para os formatos **JSON** (para análise de dados) e **DOT** (para visualização gráfica), facilitando a depuração e o entendimento da estrutura do código.

## Linguagem Suportada

O compilador foi construído com base em uma gramática formal e suporta as seguintes construções da linguagem:

* **Estrutura do Programa:** `program`, `begin`, `end.`
* **Declarações:**
    * `const` para constantes (com `:=`).
    * `type` para tipos customizados (com `=`).
    * `var` para variáveis (com tipos primitivos como `integer`, `real` ou customizados).
    * `function` com parâmetros, tipo de retorno e variáveis locais.
* **Tipos de Dados Primitivos:** `integer`, `real`, `string`, `boolean`.
* **Comandos:**
    * Atribuição (`:=`).
    * Comandos condicionais `if-then-else`.
    * Laços de repetição `while-do`.
    * Blocos aninhados `begin`/`end`.
* **Expressões:**
    * Operadores aritméticos (`+`, `-`, `*`, `/`) com precedência correta.
    * Operadores relacionais (`=`, `<>`, `<`, `>`).
    * Operadores lógicos (`and`, `or`, `not`).
* **Entrada e Saída:** Chamadas a `read(...)` e `write(...)`.
* **Comentários:** Comentários no formato `{# ... #}` são ignorados.

## Como Executar

Este projeto foi escrito em Python 3 e não requer nenhuma biblioteca externa.

**1. Clone o Repositório:**
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

**2. Execute o Programa Principal:**
O projeto possui uma interface de linha de comando interativa. Para iniciar, execute o arquivo `main.py`:
```bash
python main.py
```

**3. Siga o Menu Interativo:**
O menu permitirá que você:
* **Opção 1:** Teste apenas o analisador léxico em um arquivo `.pas` e veja a lista de tokens gerados.
* **Opção 2:** Execute o pipeline completo (léxico e sintático) para gerar a AST a partir de um arquivo `.pas`. A AST será impressa no console.
* **Opção 3:** Exporte a última AST gerada para os formatos `.json` e `.dot`.
* **Opção 4:** Sair do programa.

## Estrutura do Projeto

O código está organizado nos seguintes arquivos:

* `main.py`: Ponto de entrada do programa, contém o menu interativo e a lógica principal.
* `lexer.py`: Implementação do Analisador Léxico (Scanner), que converte o código-fonte em tokens.
* `parser.py`: Implementação do Analisador Sintático (Parser), que valida a gramática e constrói a AST.
* `ast_nodes.py`: Contém as definições (`dataclasses`) para cada tipo de nó da Árvore Sintática Abstrata.
* `ast_exporter.py`: Ferramentas para exportar a AST para os formatos JSON e DOT (Graphviz).
* `exemplo.pas`: Arquivos de exemplo com código na linguagem Pascal simplificada para testes.

## Visualizando a Árvore Sintática (AST)

Uma das funcionalidades mais úteis deste projeto é a capacidade de visualizar a AST. Após executar a opção 2 e depois a 3 no menu, um arquivo `export/ast.dot` será gerado.

Para visualizar o gráfico:
1.  Abra o arquivo `export/ast.dot` em um editor de texto e copie todo o seu conteúdo.
2.  Acesse o site **[Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)**.
3.  Cole o conteúdo na caixa de texto à esquerda. A imagem da árvore será renderizada automaticamente à direita.

---

**Autor**

Kassiano Vieira e Claudio Nunes