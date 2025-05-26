from a_star import a_star_search
from dijkstra import dijkstra_search
from bidirectional_a_star import bidirectional_a_star  # Importing Bidirectional A* search
from map_graph import create_map

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

if __name__ == "__main__":
    grid = create_map()
    start, goal = (0, 0), (9, 9)

    # A* Search
    print("Running A* Search:")
    came_from_a_star, cost_a_star = a_star_search(grid, start, goal)
    path_a_star = reconstruct_path(came_from_a_star, start, goal)
    print("Path (A*):", path_a_star)
    print("Cost (A*):", cost_a_star[goal])
    grid.display(path_a_star)

    print("\n" + "=" * 40 + "\n")

    # Dijkstra's Search
    print("Running Dijkstra's Search:")
    came_from_dijkstra, cost_dijkstra = dijkstra_search(grid, start, goal)
    path_dijkstra = reconstruct_path(came_from_dijkstra, start, goal)
    print("Path (Dijkstra):", path_dijkstra)
    print("Cost (Dijkstra):", cost_dijkstra[goal])
    grid.display(path_dijkstra)

    print("\n" + "=" * 40 + "\n")

    # Bidirectional A* Search
    print("Running Bidirectional A* Search:")
    path_bidirectional, cost_bidirectional = bidirectional_a_star(grid, start, goal)
    if path_bidirectional == "No route possible":
            print(path_bidirectional)
    else:
            print("Path (Bidirectional A*):", path_bidirectional)
            print("Cost (Bidirectional A*):", cost_bidirectional)
            grid.display(path_bidirectional)  # Pass only the path, not the tuple