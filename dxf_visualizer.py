import json
import networkx as nx
import matplotlib.pyplot as plt

style_attributes = {
    "Note Text (ANSI)": {"fontsize": 12, "fontstyle": "normal"},
    "Text Style38": {"fontsize": 12, "fontstyle": "italic"},
    "Text Style39": {"fontsize": 10, "fontstyle": "normal"},
    "Text Style30": {"fontsize": 12, "fontstyle": "normal"},
    # Add more styles as needed
}


def dxf_visualizer(json_file):
    # Load JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Initialize plot
    fig, ax = plt.subplots(figsize=(20, 10))

    # Iterate through each item in the JSON data
    for item in data:
        if item['type'] == 'LINE':
            # Extract start and end points
            start_x, start_y = item['start']
            end_x, end_y = item['end']
            # Plot line
            ax.plot([start_x, end_x], [start_y, end_y], marker='o')
        elif item['type'] in ['TEXT', 'MTEXT', 'ATTDEF']:
            # Extract coordinates, text, and style
            x, y = item['coordinates']
            text = item['text']
            style = item['style']
            # Get font attributes based on style
            font_attrs = style_attributes.get(style, {"fontsize": 10, "fontstyle": "normal"})
            # Plot text with specified font size and style
            ax.text(x, y, text, fontsize=font_attrs["fontsize"], fontstyle=font_attrs["fontstyle"], ha='left', va='center')
    ax.axis('off')

    # Show plot
    plt.show()


def visualize_graph(G):
    fig, ax = plt.subplots()
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='blue', node_size=500, ax=ax)
    ax.set_title('DXF Text Graph')
    plt.show()
