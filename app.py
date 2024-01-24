from flask import Flask, request, jsonify, send_from_directory
import os
from A_star_code import *
app = Flask(__name__, static_folder='static')

# Serve your index page
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'visualization.html')

# Endpoint to handle the pathfinding
@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    start_coord = data['start']
    goal_coord = data['end']
    
    # For demonstration, let's just send back the start and end coordinates
    # Replace this with a call to your A* function and handle the response
    path = [start_coord, goal_coord]
    cost = 0  # Replace with actual cost from your A* function
    # Assuming you have a function to load your data
    adjacencies, coord_to_index, index_to_coord = load_data()
    road_nodes = create_road_nodes_set(adjacencies)
    start_node = index_to_coord[find_nearest_node(start_coord, index_to_coord,road_nodes)]
    goal_node = index_to_coord[find_nearest_node(goal_coord, index_to_coord,road_nodes)]

    path, cost, a,b = a_star(start_node, goal_node, adjacencies, coord_to_index, index_to_coord)
    print(path)
    return jsonify({'path': path, 'cost': cost})

# Necessary for local development to avoid CORS issues
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(debug=True)
