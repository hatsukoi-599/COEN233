# @Author
# xiaoxiao jiang > xjiang3@scu.edu

import sys
from netemulate import netEmulator
import heapq
from logger_helper import setup_logger

logger = setup_logger('csen233hw7JiangXiaoxiao_dijkstra.log')


class Dijkstra(netEmulator):
	def __init__(self):
		super().__init__()

	def dijkstra(self, r1, r2):
		logger.info(f"Starting Dijkstra algorithm from {r1} to {r2}")
		path = []
		pair = [r for r in self.routers if r.name == r1 or r.name == r2]
		if len(pair) != 2:
			return None

		# Homework code	
		# Initialization
		distances = {router.name: float('infinity') for router in self.routers}
		previous = {router.name: None for router in self.routers}
		distances[r1] = 0
		visited = {r1}  # This set will hold all the router name with known shortest distance
		# Priority queue: Use a heap queue to get the minimum distance router name
		pq = []
		source = next((r for r in pair if r.name == r1), None)
		for neighbor, cost in source.links.items():
			distances[neighbor] = cost
			previous[neighbor] = r1
			heapq.heappush(pq, (cost, neighbor))
			 
		# Loop
		while pq:
			logger.info(f"The visited set: {visited}")
			logger.info(f"The pq: {pq}")
			# Find the router w not in visted such that D(w) is a minimum
			_, w = heapq.heappop(pq)
			if w in visited:
				continue
			
			# Add w to visted
			visited.add(w)
			logger.info(f"Router {w} is added to visited set.")
			
			if w == r2:
				break  # Found the shortest path to the target router

			# For each neighbor v of w not in visted
			w_router = next((router for router in self.routers if router.name == w), None)
			for v, cost in w_router.links.items():
				if v not in visited:
					# Update D(v) for each neighbor v of w and not in visted
					if distances[w] + cost < distances[v]:
						distances[v] = distances[w] + cost
						previous[v] = w
						heapq.heappush(pq, (distances[v], v))


		# Backtrace to reconstruct the shortest path from r1 to r2
		current_vertex = r2
		while current_vertex is not None:
			path.insert(0, current_vertex)
			current_vertex = previous[current_vertex]
		
		return path


	# This function calculates the shortest path cost from router r1 to router r2
	# It is designed to verify the correctness of dijkstra function above in test.py
	def calculate_path_cost(self, r1, r2):
		total_cost = 0
		path = self.dijkstra(r1, r2)
		if len(path) < 2:
			return total_cost 

		for i in range(len(path) - 1):
			current_router_name = path[i]
			next_router_name = path[i + 1]

			current_router = next((router for router in self.routers if router.name == current_router_name), None)

			if current_router and next_router_name in current_router.links:
				total_cost += current_router.links[next_router_name]
			else:
				return float('infinity')
			
		return total_cost


if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('need topology file')
	if len(sys.argv) <= 3:
		print('need node names')

	net=Dijkstra()
	print('loading {}'.format(sys.argv[1]))
	net.rtInit(sys.argv[1])
	print('net has {} routers'.format(len(net.routers)))

	# this is where you test your homework
	# assign two routers and find their shortest path
	# than print out the path
	shortest = net.dijkstra(sys.argv[2], sys.argv[3])
	shortest_cost = net.calculate_path_cost(sys.argv[2], sys.argv[3])
	logger.info(f"Shortest path from {sys.argv[2]} to {sys.argv[3]}: {shortest}. The cost is: {shortest_cost}")