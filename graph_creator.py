import json
import networkx as nx

def create_text_graph(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    G = nx.Graph()  # Initialize an empty graph

    for item in data:
        if item['type'] in ['TEXT', 'MTEXT', 'ATTDEF']:
            x, y = item['coordinates']
            text = item['text']
            G.add_node(text, pos=(x, y))

    # Add edges between all text nodes (fully connected graph for demonstration)
    for node1 in G.nodes:
        for node2 in G.nodes:
            if node1 != node2:
                G.add_edge(node1, node2)

    return G