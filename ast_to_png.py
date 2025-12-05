#!/usr/bin/env python3
"""
Script para converter o AST JSON em uma visualização PNG da árvore.
Requer: pip install graphviz
"""

import json
import sys
from graphviz import Digraph

def add_node(graph, node, parent_id=None, edge_label='', node_counter=[0]):
    """
    Adiciona um nó à árvore recursivamente.

    Args:
        graph: Objeto Digraph do graphviz
        node: Nó atual do AST
        parent_id: ID do nó pai
        edge_label: Label da aresta que conecta ao pai
        node_counter: Lista com contador de nós (para IDs únicos)

    Returns:
        ID do nó atual
    """
    # Gera ID único para este nó
    current_id = f"node_{node_counter[0]}"
    node_counter[0] += 1

    # Determina o tipo do nó
    if isinstance(node, dict):
        node_type = node.get('type', 'Unknown')

        # Cria o label do nó com informações relevantes
        label_parts = [node_type]

        # Adiciona informações extras dependendo do tipo
        if node_type == 'Program':
            label_parts.append(f"name: {node.get('name', '')}")
        elif node_type == 'Var':
            label_parts.append(f"name: {node.get('name', '')}")
        elif node_type == 'Num':
            label_parts.append(f"value: {node.get('value', '')}")
        elif node_type == 'BinOp':
            label_parts.append(f"op: {node.get('op', '')}")
        elif node_type == 'VarDecl':
            names = ', '.join(node.get('names', []))
            label_parts.append(f"names: {names}")
            label_parts.append(f"type: {node.get('type_name', '')}")
        elif node_type == 'Call':
            label_parts.append(f"name: {node.get('name', '')}")

        label = '\\n'.join(label_parts)

        # Define cor baseada no tipo de nó
        colors = {
            'Program': '#E3F2FD',
            'VarDecl': '#FFF3E0',
            'Compound': '#F3E5F5',
            'Assign': '#E8F5E9',
            'While': '#FFF9C4',
            'If': '#FFECB3',
            'BinOp': '#FFCDD2',
            'Var': '#C8E6C9',
            'Num': '#B2DFDB',
            'Call': '#D1C4E9'
        }

        color = colors.get(node_type, '#FFFFFF')
        graph.node(current_id, label, style='filled', fillcolor=color, shape='box')

        # Conecta ao pai se existir
        if parent_id is not None:
            graph.edge(parent_id, current_id, label=edge_label)

        # Processa filhos recursivamente
        for key, value in node.items():
            if key == 'type':
                continue

            if isinstance(value, dict):
                # Filho único
                add_node(graph, value, current_id, key, node_counter)

            elif isinstance(value, list) and value:
                # Lista de filhos
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        list_label = f"{key}[{i}]"
                        add_node(graph, item, current_id, list_label, node_counter)

    elif isinstance(node, list):
        # Lista de nós
        for i, item in enumerate(node):
            if isinstance(item, dict):
                add_node(graph, item, parent_id, f"[{i}]", node_counter)

    return current_id


def create_ast_visualization(json_file, output_file='export/ast.png'):
    """
    Cria uma visualização PNG da AST a partir de um arquivo JSON.

    Args:
        json_file: Caminho para o arquivo JSON da AST
        output_file: Caminho para o arquivo PNG de saída
    """
    # Lê o arquivo JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        ast_data = json.load(f)

    # Cria o grafo direcionado
    graph = Digraph(comment='Abstract Syntax Tree')
    graph.attr(rankdir='TB')  # Top to Bottom
    graph.attr('node', fontname='Arial', fontsize='10')
    graph.attr('edge', fontname='Arial', fontsize='8')

    # Adiciona os nós recursivamente
    add_node(graph, ast_data)

    # Renderiza o grafo
    output_path = output_file.replace('.png', '')
    graph.render(output_path, format='png', cleanup=True)

    print(f"Árvore AST gerada com sucesso: {output_file}")


if __name__ == '__main__':
    # Usa argumentos da linha de comando ou valores padrão
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'export/ast.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'export/ast.png'

    create_ast_visualization(json_file, output_file)
