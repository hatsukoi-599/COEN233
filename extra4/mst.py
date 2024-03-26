# @Author: Xiaoxiao Jiang > xjiang3@scu.edu

# @Description
# This code generates a Minimum Spanning Tree (MST) using Kruskal's algorithm. To better visualize the generated MST, 
# refer to 'mst.png' in the folder, which is created using matplotlib.pyplot. 
# The code for visualization can be found in the commented-out function 'visualize_mst' in mst.py.
# Additionally, 'test.py' is included to verify the correctness of the MST. This verification uses the NetworkX library in Python. 
# If interested, you can install NetworkX and run 'test.py' to compare the total weight of the MST.



import sys
from netemulate import netEmulator
from logger_helper import setup_logger

# import matplotlib.pyplot as plt
# import networkx as nx

logger = setup_logger('csen233extra4JiangXiaoxiao.log')

class DisjointSet():
    def __init__(self, vertices):
        self.vertices = vertices
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if item == self.parent[item]:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1


def kruskalMST(net):
    vertices = [router.name for router in net.routers]
    ds = DisjointSet(vertices)
    mst = []
    edges = sorted([(weight, u.name, v) for u in net.routers for v, weight in u.links.items()])

    for weight, u, v in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, weight))

    return mst


# def visualize_mst(mst, net):
#     G = nx.Graph()

#     for router in net.routers:
#         G.add_node(router.name)

#     for edge in mst:
#         G.add_edge(edge[0], edge[1], weight=edge[2])

#     # Set up the plot size
#     plt.figure(figsize=(12, 12))

#     # Try to optimize the layout
#     pos = nx.spring_layout(G, k=3.0, iterations=100)  # Increase k for more space, iterations for better layout

#     nx.draw_networkx_nodes(G, pos, node_size=500)
#     nx.draw_networkx_edges(G, pos, width=2)

#     # Adjust font size and font family
#     nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

#     edge_labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

#     plt.axis('off')
#     plt.show()


# Main execution
def main():
    if len(sys.argv) <= 1:
        logger.info('Usage: python mst.py <topology file>')
        sys.exit(1)

    net = netEmulator()
    net.rtInit(sys.argv[1])
    mst = kruskalMST(net)
    logger.info('Minimum Spanning Tree:')
    total_weight = 0
    for edge in mst:
        total_weight += edge[2]
        logger.info(f'{edge[0]} - {edge[1]} (Weight: {edge[2]})')

    logger.info(f"Total weight of MST is: {total_weight}")
    # visualize_mst(mst, net)

if __name__ == '__main__':
    main()
