import json
import re

import logging

logger = logging.getLogger(__name__)

def strip_rtf(text):
    return re.sub(r'\\f[^;]+;|\\H[^;]+;|\\[a-z]+\|[a-z0-9]+\|[a-z0-9]+;', '', text)

def generate_json(entities, filename='output.json'):
    # Convert list to JSON
    json_output = json.dumps(entities, indent=4)
    with open(filename, 'w') as f:
        f.write(json_output)

def extract_text_entities(text_block):
    text_entities = []
    line_entities = []
    for entity in text_block:
        #logger.info(f"  Type: {entity.dxftype()}")
        if entity.dxftype() in ['TEXT', 'MTEXT', 'ATTDEF']:
            text_value = getattr(entity.dxf, 'text', '')
            text_value = strip_rtf(text_value)
            text_coordinates = getattr(entity.dxf, 'insert', (0, 0))
            text_style = entity.dxf.style
            #logger.info(f"  Type: {entity.dxftype()}, Text: {text_value}, Style: {text_style}, Coordinates: {text_coordinates}")
                    
            text_coordinates = (text_coordinates.x, text_coordinates.y)

            text_entities.append({
                    "type": entity.dxftype(),
                    "text": text_value,
                    "style": text_style,
                    "coordinates": text_coordinates
            })

        if entity.dxftype() in ['LINE']:
            start = getattr(entity.dxf, 'start', (0, 0))
            end = getattr(entity.dxf, 'end', (0, 0))

            start_point = (start.x, start.y)
            end_point = (end.x, end.y)

            line_entities.append({
                "type": "LINE",
                "start": start_point,  
                "end": end_point       
            })
            #logger.info(f"  Type: {entity.dxftype()}, Start: {start_point}, End: {end_point}")
    
    all_entities = text_entities + line_entities
    return all_entities
    