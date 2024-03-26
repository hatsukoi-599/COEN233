# @Author：Xiaoxiao Jiang > xjiang3@scu.edu

# @Usage
# To execute this program, simply run the following command in your terminal or command prompt:
# python dijkstra.py <topology_file> <source_router_name> <dest_router_name>
# Example: python dijkstra.py R01 R20

# Note: The implementation of the Dijkstra algorithm is based on the provided code, which assumes unique router names for each node. 
# Consequently, the algorithm does not account for scenarios involving duplicate router names, such as (R01, R01). 
# Please ensure that each router has a distinct name for testing purposes

# @Description:
# This script takes the second and third command-line arguments as the source and destination router names, respectively.
# Before simulating packet forwarding, it invokes the Dijkstra algorithm from HW7 to compute the shortest path between the two routers for reference.
# The negative tests primarily focus on attempting to sendData to a destination that does not exist in the FIB. 
# For this purpose, a router name is generated randomly, and sendData is called with this generated name as the destination.
# You should expect to see the packet being dropped in both the stdout and the logfile.


import sys
from logger_helper import setup_logger
import random
import string
from dijkstra import Dijkstra



logger = setup_logger('csen233hw8JiangXiaoxiao.log')
if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print('need topology file')
	if len(sys.argv) <= 3:
		print('need node names')

	filename = sys.argv[1]
	net = Dijkstra()
	net.rtInit(filename)

	net.calculate_and_distribute_fib()

	source_router_name = sys.argv[2]
	dest_router_name = sys.argv[3]
	logger.info(f'source router: {source_router_name}, dest router: {dest_router_name}')
	logger.info(f'Positive test: Trying to send data from {source_router_name} to {dest_router_name}')

	# Positive test
	path = net.dijkstra(source_router_name, dest_router_name)
	short_path_cost = net.calculate_path_cost(source_router_name, dest_router_name)

	logger.info(f'Shortest path from {source_router_name} to {dest_router_name} shall be {path}')

	router = next((r for r in net.routers if r.name == source_router_name), None)
	
	if router is None:
		logger.error(f'Router Not Found')
			
	router.sendData(dest_router_name, "hello world");

	# Negative test
	# Case #1 -> Try to send data to non-existent destination
	random_router_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
	logger.info(f'Negative test case #1 -> Try to send data to non-existent destination: Send data from {source_router_name} to {random_router_name}')
	router.sendData(random_router_name,'You shall not see this sentence')