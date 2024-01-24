import json
from queue import PriorityQueue
import numpy as np
def load_data():
    # Load adjacencies from a JSON file
    with open('adjacencies.json', 'r') as f:
        adjacencies_serializable = json.load(f)
    adjacencies = {k: set(v) for k, v in adjacencies_serializable.items()}

    # Load coord_to_index from a JSON file
    with open('coord_to_index.json', 'r') as f:
        coord_to_index_serializable = json.load(f)
    coord_to_index = {tuple(map(float, k.strip('()').split(', '))): v for k, v in coord_to_index_serializable.items()}

    # Load index_to_coord from a JSON file
    with open('index_to_coord.json', 'r') as f:
        index_to_coord_serializable = json.load(f)
    index_to_coord = {int(k): tuple(map(float, v.strip('()').split(', '))) for k, v in index_to_coord_serializable.items()}
    return adjacencies,coord_to_index,index_to_coord
def create_road_nodes_set(adjacencies):
    road_nodes = set()

    # Assuming adjacencies is a dictionary where each key is a node,
    # and the value is a set or list of connected nodes (road segments)
    for node, connected_nodes in adjacencies.items():
        if len(connected_nodes)>=2:
            for connect in connected_nodes:
                road_nodes.add(int(connect))

    return road_nodes



def haversine(coord1, coord2):
    # Calculate the Haversine distance between two coordinates in (lon, lat) format
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Radius of the Earth in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest_node(coord, all_nodes, road_nodes):
    closest_node = None
    min_distance = float('inf')

    for node_id in road_nodes:
            node_coord = all_nodes[node_id]  # Get the coordinates of the road node
            distance = haversine(coord, node_coord)
            if distance < min_distance:
                min_distance = distance
                closest_node = node_id

    return closest_node





def reconstruct_path(came_from, start, goal):
    # Reconstructs the path from start to goal
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
def a_star(start_coord, goal_coord, adjacencies, coord_to_index, index_to_coord):
    start = coord_to_index[start_coord]
    goal = coord_to_index[goal_coord]

    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    node_seen_count = {}
    explored_routes = []

    while not open_set.empty():
        current = open_set.get()[1]
        node_seen_count[current] = node_seen_count.get(current, 0) + 1
        
        if current == goal:
            break

        current_coord = index_to_coord[int(current)]

        # Access only neighbors of the current node
        for next_node in adjacencies.get(str(current), []):
            next_node = int(next_node)
            next_node_coord = index_to_coord[int(next_node)]

            # Calculate distance using Haversine formula
            distance = haversine(current_coord, next_node_coord)
            new_cost = cost_so_far[current] + distance

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + haversine(next_node_coord, goal_coord)
                open_set.put((priority, next_node))
                came_from[next_node] = current
                explored_routes.append((current, next_node))

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        if current not in came_from:
            break
        path.append(index_to_coord[current])
        current = came_from[current]
    path.append(index_to_coord[start])
    path.reverse()

    return path, cost_so_far.get(goal, float('inf')), node_seen_count, explored_routes
def a_star_2(start_coord, goal_coord, adjacencies, coord_to_index, index_to_coord):
    start = coord_to_index[start_coord]
    goal = coord_to_index[goal_coord]

    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}
    node_seen_count = {}
    states = []

    while not open_set.empty():
        current = open_set.get()[1]
        node_seen_count[current] = node_seen_count.get(current, 0) + 1

        if current == goal:
            break

        for next_node in adjacencies.get(str(current), []):
            next_node = int(next_node)
            new_cost = cost_so_far[current] + haversine(index_to_coord[current], index_to_coord[next_node])

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + haversine(index_to_coord[next_node], goal_coord)
                open_set.put((priority, next_node))
                came_from[next_node] = current

                # Record the state for visualization
                current_path = reconstruct_path(came_from, start, current)
                state = {
                    "current": index_to_coord[current],
                    "open_set": [index_to_coord[node] for _, node in open_set.queue],
                    "path": [index_to_coord[node] for node in current_path]
                }
                states.append(state)

    # Save states to a JSON file
    with open('a_star_states.json', 'w') as f:
        json.dump(states, f)

    final_path = reconstruct_path(came_from, start, goal)
    return [index_to_coord[node] for node in final_path], cost_so_far.get(goal, float('inf')), node_seen_count
if __name__ == '__main__':

    start_coord = (21.01590446, 105.836377608)
    goal_coord = (21.01061115892123, 105.83981623273218)
    
    # For demonstration, let's just send back the start and end coordinates

    # Assuming you have a function to load your data
    adjacencies, coord_to_index, index_to_coord = load_data()
    road_nodes = create_road_nodes_set(adjacencies)
    start_node = index_to_coord[find_nearest_node(start_coord, index_to_coord,road_nodes)]
    goal_node = index_to_coord[find_nearest_node(goal_coord, index_to_coord,road_nodes)]
    print(start_node)
    path, cost, a,b = a_star(start_node, goal_node, adjacencies, coord_to_index, index_to_coord)
    print(path)
    
