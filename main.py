import ezdxf
import logging
import re
import json
from dxf_extractor import extract_text_entities
from logging_config import setup_logging
from dxf_visualizer import dxf_visualizer, visualize_graph
from graph_creator import create_text_graph
from information_table_creator import create_table

setup_logging()

logger = logging.getLogger(__name__)


def strip_rtf(text):
    # Regular expression to remove RTF formatting
    return re.sub(r'\\f[^;]+;|\\H[^;]+;|\\[a-z]+\|[a-z0-9]+\|[a-z0-9]+;', '', text)


def app():

    # Load the DXF file
    dxf_path = 'LauriToru.dxf'
    doc = ezdxf.readfile(dxf_path)

    for block in doc.blocks:
        if block.name == 'Title Blocks ANSI - Large':
            all_entities = extract_text_entities(block)

    # Convert list to JSON
    json_output = json.dumps(all_entities, indent=4)
    with open('DXF.json', 'w') as f:
        f.write(json_output)

    # table = create_table('DXF.json')
    texts_graph = create_text_graph('DXF.json')

    # Visualize the DXF json
    dxf_visualizer('DXF.json')
    # visualize_graph(texts_graph)


app()

