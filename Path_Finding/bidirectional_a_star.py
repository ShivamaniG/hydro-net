from queue import PriorityQueue

def manhattan_heuristic(a, b):
    """Calculate the Manhattan distance between two points a and b."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, start, current):
    """Reconstruct the path from start to current node."""
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()  # Reverse the path to make it from start to current
    return path

def join_paths(path_1, path_2):
    """Join two paths from start to goal and goal to start."""
    path_2.reverse()  # Reverse the path from the goal
    return path_1 + path_2

def bidirectional_a_star(graph, start, goal):
    # Priority queues to hold the progression of nodes 
    frontier_1 = PriorityQueue()
    frontier_1.put((0, start))
    frontier_2 = PriorityQueue()
    frontier_2.put((0, goal))

    # Dictionaries to hold the cost of travel and origin of nodes 
    came_from_1 = {}
    cost_so_far_1 = {}
    came_from_1[start] = None 
    cost_so_far_1[start] = 0 

    came_from_2 = {}
    cost_so_far_2 = {}
    came_from_2[goal] = None
    cost_so_far_2[goal] = 0 

    while not frontier_1.empty() and not frontier_2.empty():
        # Process nodes from the start side
        _, current_1 = frontier_1.get()
        if current_1 in cost_so_far_2:
            path_1 = reconstruct_path(came_from_1, start, current_1)
            path_2 = reconstruct_path(came_from_2, goal, current_1)
            combined_path = path_1[:-1] + path_2  # Avoid double-counting the meeting point
            return combined_path, cost_so_far_1[current_1] + cost_so_far_2[current_1]
        
        # Process nodes from the goal side
        _, current_2 = frontier_2.get()
        if current_2 in cost_so_far_1:
            path_1 = reconstruct_path(came_from_1, start, current_2)
            path_2 = reconstruct_path(came_from_2, goal, current_2)
            combined_path = path_1[:-1] + path_2  # Avoid double-counting the meeting point
            return combined_path, cost_so_far_1[current_2] + cost_so_far_2[current_2]
        
        # Explore neighbors from the start side
        for next in graph.neighbors(current_1): 
            new_cost = cost_so_far_1[current_1] + graph.cost(current_1, next)
            if next not in cost_so_far_1 or new_cost < cost_so_far_1[next]:
                cost_so_far_1[next] = new_cost
                priority = new_cost + manhattan_heuristic(goal, next)
                frontier_1.put((priority, next))
                came_from_1[next] = current_1

        # Explore neighbors from the goal side
        for next in graph.neighbors(current_2): 
            new_cost = cost_so_far_2[current_2] + graph.cost(current_2, next)
            if next not in cost_so_far_2 or new_cost < cost_so_far_2[next]:
                cost_so_far_2[next] = new_cost
                priority = new_cost + manhattan_heuristic(start, next)
                frontier_2.put((priority, next))
                came_from_2[next] = current_2

    return "No route possible", None
