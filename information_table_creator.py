import json
import matplotlib.pyplot as plt
import random


def round_point(point, precision=6):
    return round(point[0], precision), round(point[1], precision)


def find_intersections(lines, precision=6):
    intersections = set()

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]

            # Extract points
            x1, y1 = line1['start']
            x2, y2 = line1['end']
            x3, y3 = line2['start']
            x4, y4 = line2['end']

            # Calculate the determinant
            denominator = (x2-x1)*(y3-y4) - (y2-y1)*(x3-x4)
            if denominator == 0:
                continue  # Lines are parallel or coincident

            # Calculate the intersection point
            t = ((x3-x1)*(y3-y4) + (x4-x3)*(y3-y1)) / denominator
            u = ((x3-x1)*(y1-y2) + (x2-x1)*(y3-y1)) / denominator

            if 0 <= t <= 1 and 0 <= u <= 1:
                x = x1 + t*(x2-x1)
                y = y1 + t*(y2-y1)
                intersections.add(round_point((x, y), precision))

    return intersections


def extract_unique_points(lines, precision=6):
    unique_points = set()

    for line in lines:
        start = round_point(tuple(line['start']), precision)
        end = round_point(tuple(line['end']), precision)
        unique_points.add(start)
        unique_points.add(end)

    return unique_points


def find_smallest_rectangles(points):
    points_set = set(points)
    rectangles = []

    for (x_i, y_i) in points:
        min_area = float('inf')
        best_rectangles_list = []
        best_rectangle = None

        # Iterate through all possible diagonal points
        for (x_j, y_j) in points:
            # Skip if the same point
            if x_i == x_j or y_i == y_j:
                continue
            # Check if the other two points needed to form a rectangle exist
            if (x_i, y_j) in points_set and (x_j, y_i) in points_set:
                area = abs(x_i - x_j) * abs(y_i - y_j)
                if area < min_area:
                    min_area = area
                    best_rectangle = [(x_i, y_i), (x_i, y_j), (x_j, y_j), (x_j, y_i)]
                    best_rectangles_list.append(best_rectangle)

        if best_rectangle not in rectangles:
            rectangles.append(best_rectangle)

    return rectangles


def create_table(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    lines = [item for item in data if item['type'] == 'LINE']

    unique_points = extract_unique_points(lines)
    intersections = find_intersections(lines)

    all_points = unique_points.union(intersections)
    for point in all_points:
        print("Point: ", point)

    cells = find_smallest_rectangles(all_points)
    for cell in cells:
        print("Rectangle: ", cell)

    '''
    # Visualize the lines
    plt.figure(figsize=(10, 8))
    for i, line in enumerate(lines):
        start = line['start']
        end = line['end']
        plt.plot([start[0], end[0]], [start[1], end[1]], marker='o', label=f'L{i + 1}')
        plt.text(start[0], start[1], f'L{i + 1}', fontsize=9, ha='right')
        plt.text(end[0], end[1], f'L{i + 1}', fontsize=9, ha='right')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Line Visualization with Labels')
    plt.show()
    '''

    '''
    # Visualize the unique points
    x_coords = [point[0] for point in all_points]
    y_coords = [point[1] for point in all_points]

    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords, c='red', marker='o')

    for idx, point in enumerate(all_points):
        plt.text(point[0], point[1], f'P{idx + 1}', fontsize=9, ha='right')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Unique Points and Intersections Visualization with Labels')
    plt.show()
    '''

    # Visualize the selected rectangles
    plt.figure(figsize=(10, 8))
    for idx, rect in enumerate(cells):
        x_values = [p[0] for p in rect] + [rect[0][0]]
        y_values = [p[1] for p in rect] + [rect[0][1]]
        color = (random.random(), random.random(), random.random())
        plt.plot(x_values, y_values, color=color, linewidth=2)

        # Calculate the midpoint of the diagonals to place the label
        mid_x = (rect[0][0] + rect[2][0]) / 2
        mid_y = (rect[0][1] + rect[2][1]) / 2

        # Add the label to the plot
        plt.text(mid_x, mid_y, f'R{idx + 1}', ha='center', va='center', fontsize=9, color=color)

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Smallest Rectangles Visualization')
    plt.show()
