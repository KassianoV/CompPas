# Visualização da Árvore Sintática Abstrata (AST)

Este guia explica como converter o arquivo `export/ast.json` em uma imagem PNG da árvore.

## Pré-requisitos

1. **Python 3** instalado
2. **Graphviz** instalado no sistema
3. **Biblioteca Python graphviz**

## Instalação

### 1. Instalar Graphviz no sistema

#### Windows:
```bash
# Opção 1: Usando Chocolatey
choco install graphviz

# Opção 2: Baixar o instalador
# Baixe de: https://graphviz.org/download/
# Execute o instalador e adicione ao PATH
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install graphviz
```

#### macOS:
```bash
brew install graphviz
```

### 2. Instalar a biblioteca Python

```bash
pip install graphviz
```

## Uso

### Forma básica (usa valores padrão):
```bash
python ast_to_png.py
```
Isso irá:
- Ler `export/ast.json`
- Gerar `export/ast.png`

### Especificar arquivos customizados:
```bash
python ast_to_png.py <arquivo_entrada.json> <arquivo_saida.png>
```

Exemplo:
```bash
python ast_to_png.py export/ast.json export/minha_arvore.png
```

## Características da Visualização

A visualização gerada inclui:

- **Cores diferentes** para cada tipo de nó:
  - Program (azul claro)
  - VarDecl (laranja claro)
  - Compound (roxo claro)
  - Assign (verde claro)
  - While (amarelo)
  - If (laranja)
  - BinOp (vermelho claro)
  - Var (verde)
  - Num (azul-verde)
  - Call (roxo)

- **Labels nas arestas** indicando a relação entre nós
- **Informações detalhadas** em cada nó (nome, valor, operador, etc.)
- **Estrutura hierárquica** de cima para baixo

## Resolução de Problemas

### Erro: "graphviz not found"
- Certifique-se de que o Graphviz está instalado no sistema (não apenas o pacote Python)
- Verifique se está no PATH do sistema

### Erro: "No module named 'graphviz'"
```bash
pip install graphviz
```

### A imagem fica muito grande
Você pode ajustar o tamanho editando o script e adicionando:
```python
graph.attr(size='10,10')  # largura,altura em polegadas
```
