#!/usr/bin/env python3
"""
Analyze trigraph structure and generate radial layout centered on mnt node.
"""

import math
from collections import defaultdict, deque

# Define all nodes
white_nodes = {
    'class', 'metaType', 'metaLevelType', 'metaRelation', 'metaRelationSignature', 'metaNType',
    'ml0', 'ml1', 'ml2', 'ml3', 'mlN',
    'type_rel', 'metaLevel_rel', 'signature_rel', 'sourceType_rel', 'targetType_rel', 'nextMetaLevel_rel',
    'sig1', 'sig2', 'sig3', 'sig4', 'sig5', 'sig6'
}

black_nodes = {f'r{i}' for i in range(1, 74)}

# Build edge list from trigraph structure
# Each entry is (black_node, white_node, color)
edges = []

# From types.sheet
edges.extend([
    ('r1', 'class', 'red'), ('r1', 'metaType', 'green'), ('r1', 'type_rel', 'blue'),
    ('r2', 'metaType', 'red'), ('r2', 'metaNType', 'green'), ('r2', 'type_rel', 'blue'),
    ('r3', 'metaLevelType', 'red'), ('r3', 'metaNType', 'green'), ('r3', 'type_rel', 'blue'),
    ('r4', 'metaRelation', 'red'), ('r4', 'metaNType', 'green'), ('r4', 'type_rel', 'blue'),
    ('r5', 'metaRelationSignature', 'red'), ('r5', 'metaNType', 'green'), ('r5', 'type_rel', 'blue'),
    ('r6', 'metaNType', 'red'), ('r6', 'metaNType', 'green'), ('r6', 'type_rel', 'blue'),
    ('r7', 'class', 'red'), ('r7', 'ml2', 'green'), ('r7', 'metaLevel_rel', 'blue'),
    ('r8', 'metaType', 'red'), ('r8', 'ml3', 'green'), ('r8', 'metaLevel_rel', 'blue'),
    ('r9', 'metaLevelType', 'red'), ('r9', 'ml3', 'green'), ('r9', 'metaLevel_rel', 'blue'),
    ('r10', 'metaRelation', 'red'), ('r10', 'ml3', 'green'), ('r10', 'metaLevel_rel', 'blue'),
    ('r11', 'metaRelationSignature', 'red'), ('r11', 'ml3', 'green'), ('r11', 'metaLevel_rel', 'blue'),
    ('r12', 'metaNType', 'red'), ('r12', 'mlN', 'green'), ('r12', 'metaLevel_rel', 'blue'),
])

# From metaLevels.sheet
edges.extend([
    ('r13', 'ml0', 'red'), ('r13', 'metaLevelType', 'green'), ('r13', 'type_rel', 'blue'),
    ('r14', 'ml1', 'red'), ('r14', 'metaLevelType', 'green'), ('r14', 'type_rel', 'blue'),
    ('r15', 'ml2', 'red'), ('r15', 'metaLevelType', 'green'), ('r15', 'type_rel', 'blue'),
    ('r16', 'ml3', 'red'), ('r16', 'metaLevelType', 'green'), ('r16', 'type_rel', 'blue'),
    ('r17', 'mlN', 'red'), ('r17', 'metaLevelType', 'green'), ('r17', 'type_rel', 'blue'),
    ('r18', 'ml0', 'red'), ('r18', 'ml2', 'green'), ('r18', 'metaLevel_rel', 'blue'),
    ('r19', 'ml1', 'red'), ('r19', 'ml2', 'green'), ('r19', 'metaLevel_rel', 'blue'),
    ('r20', 'ml2', 'red'), ('r20', 'ml2', 'green'), ('r20', 'metaLevel_rel', 'blue'),
    ('r21', 'ml3', 'red'), ('r21', 'ml2', 'green'), ('r21', 'metaLevel_rel', 'blue'),
    ('r22', 'mlN', 'red'), ('r22', 'ml2', 'green'), ('r22', 'metaLevel_rel', 'blue'),
    ('r23', 'ml0', 'red'), ('r23', 'ml1', 'green'), ('r23', 'nextMetaLevel_rel', 'blue'),
    ('r24', 'ml1', 'red'), ('r24', 'ml2', 'green'), ('r24', 'nextMetaLevel_rel', 'blue'),
    ('r25', 'ml2', 'red'), ('r25', 'ml3', 'green'), ('r25', 'nextMetaLevel_rel', 'blue'),
    ('r26', 'ml3', 'red'), ('r26', 'mlN', 'green'), ('r26', 'nextMetaLevel_rel', 'blue'),
    ('r27', 'mlN', 'red'), ('r27', 'mlN', 'green'), ('r27', 'nextMetaLevel_rel', 'blue'),
])

# From metaRelations.sheet
edges.extend([
    ('r28', 'type_rel', 'red'), ('r28', 'metaNType', 'green'), ('r28', 'type_rel', 'blue'),
    ('r29', 'metaLevel_rel', 'red'), ('r29', 'metaNType', 'green'), ('r29', 'type_rel', 'blue'),
    ('r30', 'signature_rel', 'red'), ('r30', 'metaNType', 'green'), ('r30', 'type_rel', 'blue'),
    ('r31', 'sourceType_rel', 'red'), ('r31', 'metaNType', 'green'), ('r31', 'type_rel', 'blue'),
    ('r32', 'targetType_rel', 'red'), ('r32', 'metaNType', 'green'), ('r32', 'type_rel', 'blue'),
    ('r33', 'nextMetaLevel_rel', 'red'), ('r33', 'metaNType', 'green'), ('r33', 'type_rel', 'blue'),
    ('r34', 'type_rel', 'red'), ('r34', 'ml3', 'green'), ('r34', 'metaLevel_rel', 'blue'),
    ('r35', 'metaLevel_rel', 'red'), ('r35', 'ml3', 'green'), ('r35', 'metaLevel_rel', 'blue'),
    ('r36', 'signature_rel', 'red'), ('r36', 'ml3', 'green'), ('r36', 'metaLevel_rel', 'blue'),
    ('r37', 'sourceType_rel', 'red'), ('r37', 'ml3', 'green'), ('r37', 'metaLevel_rel', 'blue'),
    ('r38', 'targetType_rel', 'red'), ('r38', 'ml3', 'green'), ('r38', 'metaLevel_rel', 'blue'),
    ('r39', 'nextMetaLevel_rel', 'red'), ('r39', 'ml3', 'green'), ('r39', 'metaLevel_rel', 'blue'),
    ('r40', 'type_rel', 'red'), ('r40', 'sig1', 'green'), ('r40', 'signature_rel', 'blue'),
    ('r41', 'metaLevel_rel', 'red'), ('r41', 'sig2', 'green'), ('r41', 'signature_rel', 'blue'),
    ('r42', 'signature_rel', 'red'), ('r42', 'sig3', 'green'), ('r42', 'signature_rel', 'blue'),
    ('r43', 'signature_rel', 'red'), ('r43', 'sig5', 'green'), ('r43', 'signature_rel', 'blue'),
    ('r44', 'nextMetaLevel_rel', 'red'), ('r44', 'sig4', 'green'), ('r44', 'signature_rel', 'blue'),
    ('r45', 'sourceType_rel', 'red'), ('r45', 'sig3', 'green'), ('r45', 'signature_rel', 'blue'),
    ('r46', 'sourceType_rel', 'red'), ('r46', 'sig6', 'green'), ('r46', 'signature_rel', 'blue'),
    ('r47', 'targetType_rel', 'red'), ('r47', 'sig3', 'green'), ('r47', 'signature_rel', 'blue'),
    ('r48', 'targetType_rel', 'red'), ('r48', 'sig6', 'green'), ('r48', 'signature_rel', 'blue'),
])

# From metaRelationSignatures.sheet
edges.extend([
    ('r49', 'sig1', 'red'), ('r49', 'metaNType', 'green'), ('r49', 'type_rel', 'blue'),
    ('r50', 'sig2', 'red'), ('r50', 'metaNType', 'green'), ('r50', 'type_rel', 'blue'),
    ('r51', 'sig3', 'red'), ('r51', 'metaNType', 'green'), ('r51', 'type_rel', 'blue'),
    ('r52', 'sig4', 'red'), ('r52', 'metaNType', 'green'), ('r52', 'type_rel', 'blue'),
    ('r53', 'sig5', 'red'), ('r53', 'metaNType', 'green'), ('r53', 'type_rel', 'blue'),
    ('r54', 'sig6', 'red'), ('r54', 'metaNType', 'green'), ('r54', 'type_rel', 'blue'),
    ('r55', 'sig1', 'red'), ('r55', 'ml3', 'green'), ('r55', 'metaLevel_rel', 'blue'),
    ('r56', 'sig2', 'red'), ('r56', 'ml3', 'green'), ('r56', 'metaLevel_rel', 'blue'),
    ('r57', 'sig3', 'red'), ('r57', 'ml3', 'green'), ('r57', 'metaLevel_rel', 'blue'),
    ('r58', 'sig4', 'red'), ('r58', 'ml3', 'green'), ('r58', 'metaLevel_rel', 'blue'),
    ('r59', 'sig5', 'red'), ('r59', 'ml3', 'green'), ('r59', 'metaLevel_rel', 'blue'),
    ('r60', 'sig6', 'red'), ('r60', 'ml3', 'green'), ('r60', 'metaLevel_rel', 'blue'),
    ('r61', 'sig1', 'red'), ('r61', 'class', 'green'), ('r61', 'targetType_rel', 'blue'),
    ('r62', 'sig1', 'red'), ('r62', 'metaType', 'green'), ('r62', 'targetType_rel', 'blue'),
    ('r63', 'sig1', 'red'), ('r63', 'metaNType', 'green'), ('r63', 'targetType_rel', 'blue'),
    ('r64', 'sig1', 'red'), ('r64', 'metaLevelType', 'green'), ('r64', 'targetType_rel', 'blue'),
    ('r65', 'sig2', 'red'), ('r65', 'metaLevelType', 'green'), ('r65', 'targetType_rel', 'blue'),
    ('r66', 'sig3', 'red'), ('r66', 'metaNType', 'green'), ('r66', 'targetType_rel', 'blue'),
    ('r67', 'sig4', 'red'), ('r67', 'metaLevelType', 'green'), ('r67', 'targetType_rel', 'blue'),
    ('r68', 'sig5', 'red'), ('r68', 'metaRelationSignature', 'green'), ('r68', 'targetType_rel', 'blue'),
    ('r69', 'sig6', 'red'), ('r69', 'metaType', 'green'), ('r69', 'targetType_rel', 'blue'),
    ('r70', 'sig3', 'red'), ('r70', 'metaNType', 'green'), ('r70', 'sourceType_rel', 'blue'),
    ('r71', 'sig4', 'red'), ('r71', 'metaLevelType', 'green'), ('r71', 'sourceType_rel', 'blue'),
    ('r72', 'sig5', 'red'), ('r72', 'metaRelation', 'green'), ('r72', 'sourceType_rel', 'blue'),
    ('r73', 'sig6', 'red'), ('r73', 'metaRelationSignature', 'green'), ('r73', 'sourceType_rel', 'blue'),
])

# Build adjacency graph
graph = defaultdict(set)
for black, white, color in edges:
    graph[black].add(white)
    graph[white].add(black)

# BFS from metaNType to assign shells
center = 'metaNType'
shell_assignment = {}
shell_assignment[center] = 0

queue = deque([center])
visited = {center}

while queue:
    node = queue.popleft()
    current_shell = shell_assignment[node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            shell_assignment[neighbor] = current_shell + 1
            queue.append(neighbor)

# Group nodes by shell
shells = defaultdict(list)
for node, shell in shell_assignment.items():
    shells[shell].append(node)

# Sort shells
max_shell = max(shells.keys())

print(f"Total shells: {max_shell + 1}")
for i in range(max_shell + 1):
    nodes_in_shell = shells[i]
    black_count = sum(1 for n in nodes_in_shell if n in black_nodes or n.startswith('r'))
    white_count = len(nodes_in_shell) - black_count
    print(f"Shell {i}: {len(nodes_in_shell)} nodes ({black_count} black, {white_count} white)")

# Optimize node order in shells to minimize edge crossings
# Simple heuristic: order nodes by their connections to previous shell

def optimize_shell_order(shell_nodes, prev_shell_nodes, graph):
    """Order nodes in a shell to minimize crossings."""
    if not prev_shell_nodes:
        return shell_nodes

    # Calculate average angle of neighbors in previous shell
    prev_positions = {node: i for i, node in enumerate(prev_shell_nodes)}

    def neighbor_score(node):
        neighbors_in_prev = [n for n in graph[node] if n in prev_positions]
        if not neighbors_in_prev:
            return 0
        return sum(prev_positions[n] for n in neighbors_in_prev) / len(neighbors_in_prev)

    return sorted(shell_nodes, key=neighbor_score)

# Optimize all shells
optimized_shells = {}
optimized_shells[0] = shells[0]  # Center node

for i in range(1, max_shell + 1):
    optimized_shells[i] = optimize_shell_order(shells[i], optimized_shells[i-1], graph)

# Generate DOT file with radial layout
def generate_dot():
    output = []
    output.append("graph trigraph_radial {")
    output.append("  layout=neato;")
    output.append("  overlap=false;")
    output.append("  splines=true;")
    output.append("  ")

    # Node styles
    output.append("  // White nodes")
    output.append("  node [shape=circle, style=filled, fillcolor=white, fontcolor=black];")
    output.append("  ")

    # Calculate positions
    positions = {}

    # Center node
    positions[center] = (0, 0)
    output.append(f'  {center} [pos="0,0!", label="mnt"];')
    output.append("  ")

    # Other shells
    base_radius = 2.0
    for shell_idx in range(1, max_shell + 1):
        nodes_in_shell = optimized_shells[shell_idx]
        n = len(nodes_in_shell)

        # Calculate minimum radius needed for non-overlapping nodes
        # Account for Graphviz margins - use larger spacing
        min_radius = (n * 1.0) / (2 * math.pi)
        radius = max(base_radius * shell_idx, min_radius)

        if shell_idx % 2 == 1:  # Black nodes
            output.append("  // Black nodes")
            output.append("  node [shape=circle, style=filled, fillcolor=black, label=\"\", width=0.3, height=0.3];")
        else:  # White nodes
            output.append("  // White nodes")
            output.append("  node [shape=circle, style=filled, fillcolor=white, fontcolor=black, width=0.5, height=0.5];")

        for i, node in enumerate(nodes_in_shell):
            angle = 2 * math.pi * i / n
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            positions[node] = (x, y)

            label = "" if node.startswith('r') else node.replace('_rel', '').replace('Type', '')
            output.append(f'  {node} [pos="{x:.2f},{y:.2f}!", label="{label}"];')

        output.append("  ")

    # Edges with colors
    output.append("  // Edges")
    edge_set = set()
    for black, white, color in edges:
        edge_key = tuple(sorted([black, white]))
        if edge_key not in edge_set:
            edge_set.add(edge_key)
            color_hex = {'red': '#FF0000', 'green': '#00AA00', 'blue': '#0000FF'}[color]
            output.append(f'  {black} -- {white} [color="{color_hex}"];')

    output.append("}")
    return "\n".join(output)

dot_content = generate_dot()

with open('mnt-radial.dot', 'w') as f:
    f.write(dot_content)

print(f"\nGenerated mnt-radial.dot")
print("To render: neato -Tpng mnt-radial.dot -o mnt-radial.png")
print("Or: neato -Tsvg mnt-radial.dot -o mnt-radial.svg")
