# @Author
# xiaoxiao jiang > xjiang3@scu.edu

# @Description
# This script validates a custom implementation of Dijkstra's algorithm against the NetworkX library.
# NetworkX is used for calculating shortest paths in Python, and it must be installed to run this script.
# The script enumerates all pairs of routers and compares the path costs calculated by the custom implementation
# and NetworkX. As Dijkstra's algorithm calculates the shortest path based on total cost, the validation
# is performed by comparing the costs of paths, not the paths themselves.
# Note: For those pair (r1, r2) which r1 == r2, the path will be None 

# @Requirements
# The script requires the installation of the NetworkX module. Install it using pip:
# pip install networkx

import json

import networkx as nx

from dijkstra import Dijkstra

# Load network data from a JSON file
def load_network_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data["Network"]

# Create a graph from the network data
def create_graph_from_network(network_data):
    G = nx.DiGraph()
    for router in network_data:
        router_name = router["Router"]
        for link, weight in router["Links"].items():
            G.add_edge(router_name, link, weight=weight)
    return G

# Find the shortest path length using NetworkX
def find_shortest_path_length(graph, source, target):
    length = nx.shortest_path_length(graph, source=source, target=target, weight='weight')
    return length

if __name__ == "__main__":
    filename = 'net.json'
    # Load the network data from a JSON file
    network_data = load_network_from_json(filename)

    # Create a graph from the network data
    G = create_graph_from_network(network_data)

    # Generate a list of router names
    routers = ["R{:02d}".format(i) for i in range(1, 21)]

    # Initialize the custom Dijkstra algorithm implementation
    net = Dijkstra()
    net.rtInit(filename)

    match = True
    # Enumerate all pairs of routers to validate the shortest path
    for source in routers:
        for target in routers:

            # Skip if source and target are the same
            if source == target:
                continue

            # Calculate path cost using the custom Dijkstra implementation
            my_solution_length = net.calculate_path_cost(source, target)
            # Calculate path cost using NetworkX
            module_solution_length = find_shortest_path_length(G, source, target)

            # Compare the results and print a message if they differ
            if my_solution_length != module_solution_length:
               match = False
               print(f"Something wrong when calculating {source} to {target}...")
               print(f"my_solution_length: {my_solution_length}, while mudule_solution_length: {module_solution_length}")
    
    # Print a success message if all path costs match
    if match:
        print('pass!')
