import json

import networkx as nx

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

if __name__ == "__main__":
    filename = 'net.json'
    # Load the network data from a JSON file
    network_data = load_network_from_json(filename)

    # Create a graph from the network data
    G = create_graph_from_network(network_data)

    mst = nx.minimum_spanning_arborescence(G)

    total_weight = mst.size(weight='weight')
    print("Total weight of the minimum spanning tree is:", total_weight)
