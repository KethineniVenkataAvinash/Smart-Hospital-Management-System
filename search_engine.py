import networkx as nx
import time

def create_city_graph(size=10):
    G = nx.grid_2d_graph(size, size)

    obstacles = [
        (2, 2), (2, 3), (3, 3),
        (5, 5), (6, 5), (7, 5),
        (8, 2), (8, 3)
    ]

    G.remove_nodes_from(obstacles)

    return G

def run_bfs(graph, start, goal):
    start_time = time.time()

    try:
        path = nx.shortest_path(graph, start, goal)
    except nx.NetworkXNoPath:
        return None

    end_time = time.time()

    return {
        "algorithm": "BFS",
        "path": path,
        "path_length": len(path),
        "time": round(end_time - start_time, 6),
        "nodes_explored": len(graph.nodes)
    }


def manhattan_heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def run_astar(graph, start, goal):
    start_time = time.time()

    try:
        path = nx.astar_path(graph, start, goal, heuristic=manhattan_heuristic)
    except nx.NetworkXNoPath:
        return None

    end_time = time.time()

    return {
        "algorithm": "A*",
        "path": path,
        "path_length": len(path),
        "time": round(end_time - start_time, 6),
        "nodes_explored": len(path)
    }


def run_routing(start=(0, 0), goal=(9, 9)):
    graph = create_city_graph()

    bfs_result = run_bfs(graph, start, goal)
    astar_result = run_astar(graph, start, goal)

    if bfs_result and astar_result:
        best = "A*" if astar_result["time"] < bfs_result["time"] else "BFS"
    else:
        best = "No Path Found"

    return {
        "BFS": bfs_result,
        "ASTAR": astar_result,
        "best_algorithm": best
    }

def estimate_real_distance(path_length):
    """
    Convert grid path → kilometers
    (Assume 1 step ≈ 0.5 km)
    """
    return round(path_length * 0.5, 2)


def estimate_travel_time(distance_km):
    """
    Estimate ambulance time (avg speed = 40 km/h)
    """
    if distance_km == 0:
        return 0

    return round((distance_km / 40) * 60, 2) 

if __name__ == "__main__":
    print("=== SEARCH ENGINE TEST ===")

    result = run_routing()

    print("\nBFS RESULT:")
    print(result["BFS"])

    print("\nA* RESULT:")
    print(result["ASTAR"])

    print("\nBEST ALGORITHM:", result["best_algorithm"])

    if result["ASTAR"]:
        dist = estimate_real_distance(result["ASTAR"]["path_length"])
        time_min = estimate_travel_time(dist)

        print(f"\nEstimated Distance: {dist} km")
        print(f"Estimated Time: {time_min} minutes")