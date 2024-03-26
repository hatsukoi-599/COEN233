import json
from logger_helper import setup_logger

logger = setup_logger('csen233finalJiangXiaoxiao.log')


class Router:
    def __init__(self, nm):
        self.name = nm  # name of the router
        self.links = {}  # a dictionary of directly connected neighbors with link costs
        self.__fib = {}  # Forwarding Information Base as a dictionary

    @property
    def fib(self):
        # Property to access the router's FIB. Returns the FIB of the router if it exists.
        return self.__fib[self.name] if self.name in self.__fib else {}


    def addLink(self, l, c):
        self.links[l] = c

    def initFib(self):
        # logger.info(f"Router {self.name} is initing .. ")
        self.__fib.clear()
        self.__fib[self.name] = {}
        for dest in self.network.routers:
            if dest in self.links:
                self.__fib[self.name][dest] = (dest, self.links[dest])
            else:
                self.__fib[self.name][dest] = (None, float('inf'))
        
        
        for neighbor in self.links:
            self.__fib[neighbor] = {}
            for dest in self.network.routers:
                self.__fib[neighbor][dest] = (None, float('inf'))
        
        # logger.info(f"Router {self.name} has inited, ready to broadcast, the current state: {self}")
    

    def markLinkDown(self, link_name):
        # Set the link cost to a very high value to simulate "down"
        self.links[link_name] = float('inf')
        for y in self.__fib[self.name]:
            curr_next_hop, curr_cost = self.__fib[self.name][y]
            if curr_next_hop == link_name:
                if y not in self.links:
                    self.__fib[self.name][y] = (None, float('inf'))
                else:
                    self.__fib[self.name][y] = (y, self.links[y])
        
        self.updateFib()
        self.broadcast()
        
    def pack(self, dest, is_routing, data):
        routing_packet = {
            "header": {
                "source": self.name,
                "destination": dest,
                "is_routing": is_routing
            },
            "data": data
        }
        return routing_packet

    def updateFib(self):
        updated = False
        for y in self.network.routers:
                next_hop_name, curr_cost = self.__fib[self.name][y]
                for v in self.__fib:
                    if v == self.name:
                        continue
                    new_cost = self.links[v] + self.__fib[v][y][1] 
                    
                    if curr_cost > new_cost:
                        curr_cost = new_cost
                        self.__fib[self.name][y] = (v, new_cost)
                        updated = True
        
        return updated


    def broadcast(self):
         for neighbor in self.links:
            data = self.pack(neighbor, True, self.__fib[self.name])
            self.sendData(neighbor, data)


    def sendData(self, dest, data):
        source, dest, is_routing = data["header"].values()
        # logger.info(f"Router {self.name} sending data to {dest}")
        # Check if there is an entry which has valid next_hop
        if is_routing:
            next_hop = self.network.routers[dest]
            return next_hop.recvData(data)
        
        if dest in self.__fib[self.name] and self.__fib[self.name][dest][0] is not None:
            next_hop_name, _ = self.__fib[self.name][dest]
            next_hop = self.network.routers[next_hop_name]
            # Simulate sending the packet to the next router
            return next_hop.recvData(data)
        else:
            # Log the packet drop event
            logger.info(f"Router {self.name}: No valid fib entry for destination {dest}. Dropping packet.")
        
        return False

    def recvData(self, packet):
        source, dest, is_routing = packet["header"].values()
        data = packet["data"]
        # logger.info(f"Router {self.name} receives data from {source} with {packet['data']}")
        # logger.info(f"Router {self.name} FIB: {self.fib}")
        if is_routing:
            self.__fib[source] = data
            if self.updateFib():
                self.broadcast()

            return True
        
        elif dest == self.name:
            # Packet is for this router, accept it.
            logger.info(f"Router {self.name}: Packet received. {packet}")
            return True
        
        else:
            # Packet is for another router, forward it using fib.
            logger.info(f"Router {self.name}: Forwarding packet. Data: {packet}")
            return self.sendData(dest, packet)


    def __str__(self):
        return self.__repr__()

    # Friendly output of router info in JSON syntax
    def __repr__(self):
        str_repr = '{{"Router": "{}", '.format(self.name)
        if self.links:
            str_repr += '"Links": ' + json.dumps(self.links)

        if self.__fib:
            fib_simple = {
                outer_dest: {
                    inner_dest: (next_hop if isinstance(next_hop, str) else (next_hop.name if next_hop is not None else None), cost) 
                    for inner_dest, (next_hop, cost) in outer_dict.items()
                }
                for outer_dest, outer_dict in self.__fib.items()
            }
            str_repr += ', "__fib": ' + json.dumps(fib_simple)

        str_repr += '}'
        return str_repr





