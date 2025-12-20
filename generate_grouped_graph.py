#!/usr/bin/env python3
"""
Generate a DOT file for complete-graph with nodes grouped by sheet.
"""

# Node definitions by sheet
sheets = {
    'types.sheet': {
        'nodes': {
            'class': {'visibility': 'public', 'label': 'class'},
            'metaType': {'visibility': 'public+1', 'label': 'mt'},
            'metaLevelType': {'visibility': 'public+1', 'label': 'mlt'},
            'metaRelation': {'visibility': 'public', 'label': 'mr'},
            'metaRelationSignature': {'visibility': 'public', 'label': 'mrs'},
            'metaNType': {'visibility': 'private', 'label': 'mnt'},
        }
    },
    'metaLevels.sheet': {
        'nodes': {
            'ml0': {'visibility': 'public', 'label': 'ml0'},
            'ml1': {'visibility': 'public', 'label': 'ml1'},
            'ml2': {'visibility': 'public+1', 'label': 'ml2'},
            'ml3': {'visibility': 'private', 'label': 'ml3'},
            'mlN': {'visibility': 'private', 'label': 'mlN'},
        }
    },
    'metaRelations.sheet': {
        'nodes': {
            'type_rel': {'visibility': 'public', 'label': 'type', 'color': '#0000FF'},
            'metaLevel_rel': {'visibility': 'public', 'label': 'ml', 'color': '#00AA00'},
            'signature_rel': {'visibility': 'public', 'label': 'sig', 'color': '#FF0000'},
            'sourceType_rel': {'visibility': 'public+1', 'label': 'st', 'color': '#FF8800'},
            'targetType_rel': {'visibility': 'public+1', 'label': 'tt', 'color': '#AA00FF'},
            'nextMetaLevel_rel': {'visibility': 'private', 'label': 'nml', 'color': '#8B4513'},
        }
    },
    'metaRelationSignatures.sheet': {
        'nodes': {
            'sig1': {'visibility': 'private', 'label': 'a2at'},
            'sig2': {'visibility': 'private', 'label': 'a2mlt'},
            'sig3': {'visibility': 'private', 'label': 'mnt2mnt'},
            'sig4': {'visibility': 'private', 'label': 'ml2ml'},
            'sig5': {'visibility': 'private', 'label': 'mr2mrs'},
            'sig6': {'visibility': 'private', 'label': 'mrs2mt'},
        }
    }
}

# All edges with their types
edges = [
    # From types.sheet
    ('class', 'metaType', 'type'),
    ('metaType', 'metaNType', 'type'),
    ('metaLevelType', 'metaNType', 'type'),
    ('metaRelation', 'metaNType', 'type'),
    ('metaRelationSignature', 'metaNType', 'type'),
    ('metaNType', 'metaNType', 'type'),
    ('class', 'ml2', 'metaLevel'),
    ('metaType', 'ml3', 'metaLevel'),
    ('metaLevelType', 'ml3', 'metaLevel'),
    ('metaRelation', 'ml3', 'metaLevel'),
    ('metaRelationSignature', 'ml3', 'metaLevel'),
    ('metaNType', 'mlN', 'metaLevel'),

    # From metaLevels.sheet
    ('ml0', 'metaLevelType', 'type'),
    ('ml1', 'metaLevelType', 'type'),
    ('ml2', 'metaLevelType', 'type'),
    ('ml3', 'metaLevelType', 'type'),
    ('mlN', 'metaLevelType', 'type'),
    ('ml0', 'ml2', 'metaLevel'),
    ('ml1', 'ml2', 'metaLevel'),
    ('ml2', 'ml2', 'metaLevel'),
    ('ml3', 'ml2', 'metaLevel'),
    ('mlN', 'ml2', 'metaLevel'),
    ('ml0', 'ml1', 'nextMetaLevel'),
    ('ml1', 'ml2', 'nextMetaLevel'),
    ('ml2', 'ml3', 'nextMetaLevel'),
    ('ml3', 'mlN', 'nextMetaLevel'),
    ('mlN', 'mlN', 'nextMetaLevel'),

    # From metaRelations.sheet
    ('type_rel', 'metaNType', 'type'),
    ('metaLevel_rel', 'metaNType', 'type'),
    ('signature_rel', 'metaNType', 'type'),
    ('sourceType_rel', 'metaNType', 'type'),
    ('targetType_rel', 'metaNType', 'type'),
    ('nextMetaLevel_rel', 'metaNType', 'type'),
    ('type_rel', 'ml3', 'metaLevel'),
    ('metaLevel_rel', 'ml3', 'metaLevel'),
    ('signature_rel', 'ml3', 'metaLevel'),
    ('sourceType_rel', 'ml3', 'metaLevel'),
    ('targetType_rel', 'ml3', 'metaLevel'),
    ('nextMetaLevel_rel', 'ml3', 'metaLevel'),
    ('type_rel', 'sig1', 'signature'),
    ('metaLevel_rel', 'sig2', 'signature'),
    ('signature_rel', 'sig3', 'signature'),
    ('signature_rel', 'sig5', 'signature'),
    ('nextMetaLevel_rel', 'sig4', 'signature'),
    ('sourceType_rel', 'sig3', 'signature'),
    ('sourceType_rel', 'sig6', 'signature'),
    ('targetType_rel', 'sig3', 'signature'),
    ('targetType_rel', 'sig6', 'signature'),

    # From metaRelationSignatures.sheet
    ('sig1', 'metaNType', 'type'),
    ('sig2', 'metaNType', 'type'),
    ('sig3', 'metaNType', 'type'),
    ('sig4', 'metaNType', 'type'),
    ('sig5', 'metaNType', 'type'),
    ('sig6', 'metaNType', 'type'),
    ('sig1', 'ml3', 'metaLevel'),
    ('sig2', 'ml3', 'metaLevel'),
    ('sig3', 'ml3', 'metaLevel'),
    ('sig4', 'ml3', 'metaLevel'),
    ('sig5', 'ml3', 'metaLevel'),
    ('sig6', 'ml3', 'metaLevel'),
    ('sig1', 'class', 'targetType'),
    ('sig1', 'metaType', 'targetType'),
    ('sig1', 'metaNType', 'targetType'),
    ('sig1', 'metaLevelType', 'targetType'),
    ('sig2', 'metaLevelType', 'targetType'),
    ('sig3', 'metaNType', 'targetType'),
    ('sig4', 'metaLevelType', 'targetType'),
    ('sig5', 'metaRelationSignature', 'targetType'),
    ('sig6', 'metaType', 'targetType'),
    ('sig3', 'metaNType', 'sourceType'),
    ('sig4', 'metaLevelType', 'sourceType'),
    ('sig5', 'metaRelation', 'sourceType'),
    ('sig6', 'metaRelationSignature', 'sourceType'),
]

# Edge colors
edge_colors = {
    'type': '#0000FF',
    'metaLevel': '#00AA00',
    'signature': '#FF0000',
    'sourceType': '#FF8800',
    'targetType': '#AA00FF',
    'nextMetaLevel': '#8B4513',
}

# Visibility shapes
def get_shape(visibility):
    if visibility == 'public':
        return 'box'
    elif visibility == 'public+1':
        return 'hexagon'
    else:  # private
        return 'ellipse'

def generate_dot():
    output = []
    output.append("digraph complete_graph_grouped {")
    output.append("  rankdir=TB;")
    output.append("  compound=true;")
    output.append("  newrank=true;")
    output.append("  splines=true;")
    output.append("  overlap=false;")
    output.append("  ")

    # Generate clusters for each sheet
    cluster_id = 0
    for sheet_name, sheet_data in sheets.items():
        output.append(f"  subgraph cluster_{cluster_id} {{")
        output.append(f'    label="{sheet_name}";')
        output.append("    style=filled;")
        output.append("    color=lightgrey;")
        output.append("    node [style=filled];")
        output.append("    ")

        # Add nodes
        for node_id, node_data in sheet_data['nodes'].items():
            label = node_data['label']
            visibility = node_data['visibility']
            shape = get_shape(visibility)

            # Check if this is a colored relation node
            if 'color' in node_data:
                color = node_data['color']
                output.append(f'    {node_id} [label="{label}", shape={shape}, fillcolor="{color}", fontcolor=white];')
            else:
                output.append(f'    {node_id} [label="{label}", shape={shape}, fillcolor=white];')

        output.append("  }")
        output.append("  ")
        cluster_id += 1

    # Add edges
    output.append("  // Edges")
    for source, target, edge_type in edges:
        color = edge_colors[edge_type]
        output.append(f'  {source} -> {target} [color="{color}"];')

    output.append("  ")

    # Add legend
    output.append("  // Legend")
    output.append("  subgraph cluster_legend {")
    output.append('    label="Legend";')
    output.append("    style=filled;")
    output.append("    color=lightyellow;")
    output.append("    ")
    output.append('    legend_shape [label="Shapes:", shape=plaintext];')
    output.append('    legend_public [label="public", shape=box, fillcolor=white, style=filled];')
    output.append('    legend_public1 [label="public+1", shape=hexagon, fillcolor=white, style=filled];')
    output.append('    legend_private [label="private", shape=ellipse, fillcolor=white, style=filled];')
    output.append("    ")
    output.append('    legend_edges [label="Edge Colors:", shape=plaintext];')
    output.append('    legend_type [label="type", shape=plaintext, fontcolor="#0000FF"];')
    output.append('    legend_metaLevel [label="metaLevel", shape=plaintext, fontcolor="#00AA00"];')
    output.append('    legend_signature [label="signature", shape=plaintext, fontcolor="#FF0000"];')
    output.append('    legend_sourceType [label="sourceType", shape=plaintext, fontcolor="#FF8800"];')
    output.append('    legend_targetType [label="targetType", shape=plaintext, fontcolor="#AA00FF"];')
    output.append('    legend_nextMetaLevel [label="nextMetaLevel", shape=plaintext, fontcolor="#8B4513"];')
    output.append("    ")
    output.append("    {rank=same; legend_shape; legend_public; legend_public1; legend_private;}")
    output.append("    {rank=same; legend_edges; legend_type; legend_metaLevel; legend_signature;}")
    output.append("    {rank=same; legend_sourceType; legend_targetType; legend_nextMetaLevel;}")
    output.append("  }")

    output.append("}")
    return "\n".join(output)

dot_content = generate_dot()

with open('complete-graph-grouped.dot', 'w') as f:
    f.write(dot_content)

print("Generated complete-graph-grouped.dot")
print("To render:")
print("  dot -Tpng complete-graph-grouped.dot -o complete-graph-grouped.png")
print("  dot -Tsvg complete-graph-grouped.dot -o complete-graph-grouped.svg")
