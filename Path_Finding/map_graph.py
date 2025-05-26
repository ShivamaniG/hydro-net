import random

class WeightedGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.weights = {}

    def in_bounds(self, node):
        x, y = node
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, node):
        return node not in self.walls

    def neighbors(self, node):
        x, y = node
        results = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def display(self, path=None):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        for (x, y) in self.walls:
            grid[y][x] = "#"
        for (x, y), cost in self.weights.items():
            grid[y][x] = "~"

        if path:
            for (x, y) in path:
                if grid[y][x] == ".":
                    grid[y][x] = "\033[31mR\033[0m"  # Red color for the path

        grid[0][0] = "\033[32mS\033[0m"  # Green for start
        grid[self.height - 1][self.width - 1] = "\033[34mG\033[0m"  # Blue for goal

        for row in grid:
            print(" ".join(row))


def create_map():
    grid = WeightedGrid(10, 10)

    # Randomly generate walls
    wall_count = 25  # Adjust for more or fewer walls
    grid.walls = set()
    while len(grid.walls) < wall_count:
        wall = (random.randint(0, grid.width - 1), random.randint(0, grid.height - 1))
        if wall != (0, 0) and wall != (grid.width - 1, grid.height - 1):
            grid.walls.add(wall)
    grid.walls = list(grid.walls)

    # Add different weight regions
    grid.weights = {}

    # Define weight zones
    weight_zones = [
        {"x_range": (0, 4), "y_range": (0, 4), "weight_range": (2, 3)},   # Zone 1: Low weight
        {"x_range": (5, 9), "y_range": (0, 4), "weight_range": (4, 5)},   # Zone 2: High weight
        {"x_range": (0, 4), "y_range": (5, 9), "weight_range": (3, 4)},   # Zone 3: Medium weight
        {"x_range": (5, 9), "y_range": (5, 9), "weight_range": (1, 2)},   # Zone 4: Very low weight
    ]

    # Assign random weights in each zone
    for zone in weight_zones:
        for x in range(zone["x_range"][0], zone["x_range"][1] + 1):
            for y in range(zone["y_range"][0], zone["y_range"][1] + 1):
                if (x, y) not in grid.walls and (x, y) != (0, 0) and (x, y) != (grid.width - 1, grid.height - 1):
                    grid.weights[(x, y)] = random.randint(zone["weight_range"][0], zone["weight_range"][1])

    return grid

# Create the grid with random obstacles and weights
grid = create_map()
grid.display()

# Example path (change based on your algorithms' output)
path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)]
grid.display(path)
