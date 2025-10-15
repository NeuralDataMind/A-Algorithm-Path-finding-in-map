from flask import Flask, request, jsonify, render_template
import osmnx as ox
import networkx as nx

# Initialize the Flask application
app = Flask(__name__)

# --- Pre-load the graph data ---
# This is a time-consuming step, so we do it once when the server starts.
print("Loading graph for Telangana... This may take a few minutes.")
# For faster testing, you can use a smaller area like 'Hyderabad'
# G = ox.graph_from_place("Hyderabad, Telangana, India", network_type='drive')
G = ox.load_graphml(r"D:\AI project\project\telangana.graphml")
print("Graph for Telangana loaded successfully!")

# Define the main route for the web page
@app.route('/')
def index():
    # This will serve your main HTML file
    return render_template('index.html')

# Define the API endpoint for calculating the route
@app.route('/get_route', methods=['POST'])
def get_route():
    # Get start and end points from the JSON data sent by the frontend
    data = request.get_json()
    start_point_name = data.get('start')
    end_point_name = data.get('end')

    if not start_point_name or not end_point_name:
        return jsonify({'error': 'Start and end points are required.'}), 400

    try:
        # Geocode the start and end points to get coordinates
        start_coords = ox.geocode(start_point_name + ", Telangana")
        end_coords = ox.geocode(end_point_name + ", Telangana")

        # Find the nearest network nodes to the coordinates
        start_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
        end_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])

        # Calculate the shortest path using A*
        shortest_route_nodes = nx.astar_path(G, start_node, end_node, weight='length')

        # Get the coordinates for each node in the route
        route_latlons = []
        for node in shortest_route_nodes:
            point = G.nodes[node]
            route_latlons.append([point['y'], point['x']])

        # Return the route and start/end coordinates as JSON
        return jsonify({
            'route': route_latlons,
            'start_coords': [start_coords[0], start_coords[1]],
            'end_coords': [end_coords[0], end_coords[1]]
        })

    except Exception as e:
        # Handle errors, e.g., location not found
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Could not find a route. Please check the location names.'}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)