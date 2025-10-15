# download_graph.py
import osmnx as ox

print("Downloading graph data for Telangana. This will take a long time but only needs to be run once.")

# Download the graph data from OpenStreetMap
G = ox.graph_from_place("Telangana, India", network_type='drive')

print("Graph download complete. Saving to file...")

# Save the graph to a file named 'telangana.graphml'
ox.save_graphml(G, filepath="telangana.graphml")

print("Graph has been saved to telangana.graphml successfully!")