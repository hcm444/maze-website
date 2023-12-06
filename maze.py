import numpy as np
from PIL import Image, ImageDraw
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = set()
        self.queue = []

    def empty(self):
        return not self.queue

    def put(self, item, priority):
        if item not in self.elements or priority < self.elements[item]:
            heapq.heappush(self.queue, (priority, item))
            self.elements.add(item)

    def get(self):
        priority, item = heapq.heappop(self.queue)
        self.elements.remove(item)
        return item

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(matrix, start_row, start_col, end_row, end_col):
    rows, cols = matrix.shape
    open_set = PriorityQueue()
    open_set.put((start_row, start_col), 0)
    came_from = {}
    g_score = np.full((rows, cols), np.inf)
    g_score[start_row, start_col] = 0

    while not open_set.empty():
        current_row, current_col = open_set.get()
        current_g_score = g_score[current_row, current_col]

        if current_row == end_row and current_col == end_col:
            path = []
            while (current_row, current_col) in came_from:
                path.append((current_row, current_col))
                current_row, current_col = came_from[(current_row, current_col)]
            return path[::-1]

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = current_row + dr, current_col + dc
            valid_move = 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row, new_col] != 1

            if valid_move:
                tentative_g_score = current_g_score + 1

                if tentative_g_score < g_score[new_row, new_col]:
                    g_score[new_row, new_col] = tentative_g_score
                    priority = tentative_g_score + heuristic((new_row, new_col), (end_row, end_col))
                    open_set.put((new_row, new_col), priority)
                    came_from[(new_row, new_col)] = (current_row, current_col)

    return None

def find_path_from_array(maze):
    start_row, start_col = np.where(maze == 2)
    end_row, end_col = np.where(maze == 3)

    if len(start_row) == 0 or len(end_row) == 0:
        print("Start or end position not found.")
        return

    start_row, start_col = start_row[0], start_col[0]
    end_row, end_col = end_row[0], end_col[0]

    path = a_star(maze, start_row, start_col, end_row, end_col)

    if path:
        for row, col in path:
            maze[row, col] = 2
    else:
        print("No valid path found.")

def update_maze_image(input_path, output_path):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    border_thickness = 1
    draw.rectangle([0, 0, width - 1, height - 1], outline="black", width=border_thickness)

    pixel_values = {(255, 255, 255, 255): 0, (0, 0, 255, 255): 2, (255, 0, 0, 255): 3}
    image_array = np.zeros((height, width), dtype=np.uint8)

    for i1 in range(height):
        for j1 in range(width):
            image_array[i1, j1] = pixel_values.get(image.getpixel((j1, i1)), 1)

    image_array[:2, :2] = 2
    image_array[height-2:, width-2:] = 3
    image_array[0, :] = 1
    image_array[:, 0] = 1
    image_array[:, width-1] = 1
    image_array[height-1, :] = 1

    maze_array = image_array.copy()
    path = find_path_from_array(maze_array)

    new_image = Image.new("RGBA", (width, height), color=(255, 255, 255, 255))
    pixel_colors = {0: (255, 255, 255, 255), 2: (0, 0, 255, 255), 3: (255, 0, 0, 255), 1: (128, 128, 128, 255)}

    for i in range(height):
        for j in range(width):
            color = pixel_colors.get(maze_array[i, j], (128, 128, 128, 255))
            new_image.putpixel((j, i), color)

    if path:
        for row, col in path:
            new_image.putpixel((col, row), (0, 255, 0, 255))  # Highlight the path in green

    new_image.save(output_path, "PNG")



