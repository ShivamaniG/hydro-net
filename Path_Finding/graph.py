import time
import random
import psutil  # For memory usage tracking
import statistics  # For standard deviation
import matplotlib.pyplot as plt  # For graph plotting
from map_graph import create_map
from a_star import a_star_search
from dijkstra import dijkstra_search
from bidirectional_a_star import bidirectional_a_star 

# Function to measure the performance of the algorithms
def measure_performance(algorithm, grid, start_node, goal_node):
    start_time = time.time()
    path = algorithm(grid, start_node, goal_node)
    end_time = time.time()

    time_taken = end_time - start_time
    path_length = len(path)

    # Memory usage for the entire process
    memory_usage = psutil.Process().memory_info().rss  
    return time_taken, path_length, memory_usage

# Function to calculate statistics (average, standard deviation, and path length)
def calculate_stats(times, lengths):
    avg_time = sum(times) / len(times)
    std_dev_time = statistics.stdev(times) if len(times) > 1 else 0
    avg_length = sum(lengths) / len(lengths)
    return avg_time, std_dev_time, avg_length

# Function to run the comparison for one map
def run_comparison_for_map(grid, iterations=100):
    start_node = (0, 0)
    goal_node = (grid.width - 1, grid.height - 1)

    a_star_times = []
    dijkstra_times = []
    bidirectional_a_star_times = []

    a_star_lengths = []
    dijkstra_lengths = []
    bidirectional_a_star_lengths = []

    for _ in range(iterations):
        # A* Search
        time_taken, path_length, _ = measure_performance(a_star_search, grid, start_node, goal_node)
        a_star_times.append(time_taken)
        a_star_lengths.append(path_length)

        # Dijkstra's Algorithm
        time_taken, path_length, _ = measure_performance(dijkstra_search, grid, start_node, goal_node)
        dijkstra_times.append(time_taken)
        dijkstra_lengths.append(path_length)

        # Bidirectional A* Search
        time_taken, path_length, _ = measure_performance(bidirectional_a_star, grid, start_node, goal_node)
        bidirectional_a_star_times.append(time_taken)
        bidirectional_a_star_lengths.append(path_length)

    # Calculate statistics for the current map
    a_star_stats = calculate_stats(a_star_times, a_star_lengths)
    dijkstra_stats = calculate_stats(dijkstra_times, dijkstra_lengths)
    bidirectional_a_star_stats = calculate_stats(bidirectional_a_star_times, bidirectional_a_star_lengths)

    return a_star_stats, dijkstra_stats, bidirectional_a_star_stats

# Run comparison for 100 maps and collect stats
def run_comparison_for_multiple_maps(num_maps=100, iterations=200):
    a_star_avg_times = []
    dijkstra_avg_times = []
    bidirectional_a_star_avg_times = []

    for _ in range(num_maps):
        grid = create_map()  # Generate a random map
        a_star_stats, dijkstra_stats, bidirectional_a_star_stats = run_comparison_for_map(grid, iterations)

        a_star_avg_times.append(a_star_stats[0])  # Average time for A*
        dijkstra_avg_times.append(dijkstra_stats[0])  # Average time for Dijkstra
        bidirectional_a_star_avg_times.append(bidirectional_a_star_stats[0])  # Average time for Bidirectional A*

    return a_star_avg_times, dijkstra_avg_times, bidirectional_a_star_avg_times

# Plotting the graph
def plot_graph(a_star_avg_times, dijkstra_avg_times, bidirectional_a_star_avg_times):
    maps = list(range(1, len(a_star_avg_times) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(maps, a_star_avg_times, label="A* Search", color='r')
    plt.plot(maps, dijkstra_avg_times, label="Dijkstra", color='g')
    plt.plot(maps, bidirectional_a_star_avg_times, label="Bidirectional A*", color='b')

    plt.xlabel('Map Index')
    plt.ylabel('Average Time (seconds)')
    plt.title('Algorithm Performance for Multiple Maps')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the comparison for 100 maps and plot the graph
a_star_avg_times, dijkstra_avg_times, bidirectional_a_star_avg_times = run_comparison_for_multiple_maps(100, 100)
plot_graph(a_star_avg_times, dijkstra_avg_times, bidirectional_a_star_avg_times)
