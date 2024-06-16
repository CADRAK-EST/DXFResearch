import json
import itertools
from shapely.geometry import LineString, Point, box

def find_intersections(lines):
    intersections = []
    for line1, line2 in itertools.combinations(lines, 2):
        line1_geom = LineString([line1['start'], line1['end']])
        line2_geom = LineString([line2['start'], line2['end']])
        if line1_geom.intersects(line2_geom):
            intersection = line1_geom.intersection(line2_geom)
            if isinstance(intersection, Point):
                intersections.append((intersection.x, intersection.y))
    return intersections

def group_into_cells(intersections):
    intersections = sorted(intersections)
    cells = []
    used_points = set()

    for i, (x1, y1) in enumerate(intersections):
        for (x2, y2) in intersections[i+1:]:
            if x1 < x2 and y1 < y2:
                cell = ((x1, y1), (x2, y2))
                cell_box = box(x1, y1, x2, y2)
                if not any(cell_box.contains(Point(px, py)) for px, py in used_points):
                    cells.append(cell)
                    used_points.update([(x1, y1), (x2, y2)])
    return cells

def assign_text_to_cells(cells, texts):
    cell_texts = []
    for cell in cells:
        (x1, y1), (x2, y2) = cell
        cell_text = []
        for text in texts:
            tx, ty = text['coordinates']
            if x1 <= tx <= x2 and y1 <= ty <= y2:
                cell_text.append(text['text'])
        cell_texts.append({
            'cell': cell,
            'texts': cell_text
        })
    return cell_texts

def create_table(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    lines = [item for item in data if item['type'] == 'LINE']
    texts = [item for item in data if item['type'] in ['TEXT', 'MTEXT', 'ATTDEF']]

    intersections = find_intersections(lines)
    cells = group_into_cells(intersections)
    cell_texts = assign_text_to_cells(cells, texts)

    return cell_texts