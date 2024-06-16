import json
import networkx as nx
import matplotlib.pyplot as plt


def dxf_visualizer(json_file):
    # Load JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Initialize plot
    fig, ax = plt.subplots()

    # Iterate through each item in the JSON data
    for item in data:
        if item['type'] == 'LINE':
            # Extract start and end points
            start_x, start_y = item['start']
            end_x, end_y = item['end']
            # Plot line
            ax.plot([start_x, end_x], [start_y, end_y], marker='o')
        elif item['type'] in ['TEXT', 'MTEXT', 'ATTDEF']:
            # Extract coordinates and text
            x, y = item['coordinates']
            text = item['text']
            # Plot text
            ax.text(x, y, text, fontsize=12, ha='left', va='bottom')

    # Set plot title and labels
    ax.set_title('DXF Plot')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.axis('equal')  # Equal scaling

    # Show plot
    plt.show()


def visualize_graph(G):
    fig, ax = plt.subplots()
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='blue', node_size=500, ax=ax)
    ax.set_title('DXF Text Graph')
    plt.show()