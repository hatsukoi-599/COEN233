from netemulate import netEmulator
import random

class DistanceVector(netEmulator):
	def __init__(self):
		super().__init__()
		
	def distance_vector(self):
		for _, w in self.routers.items():
			w.initFib()
		
		# Randomly choose a router to begin the broadcast wave in the whole network
		seed_router_name = random.choice(list(self.routers.keys()))
		seed_router = self.routers[seed_router_name]
		seed_router.broadcast()
