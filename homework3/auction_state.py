# auction_state.py
import threading
import time

class AuctionState:
    def __init__(self):
        self.highest_bid = 0
        self.highest_bidder = None
        self.last_bid_time = None
        self.clients = {}
        self.chant = 1
        self.lock = threading.Lock()

    def add_client(self, client_address, client_socket):
        with self.lock:
            ip_address = client_address[0] 
            self.clients[ip_address] = client_socket

    def remove_client(self, client_address):
        with self.lock:
            if self.client_joined:
                del self.clients[client_address[0]]

    def client_joined(self, client_address):
        with self.lock:
            ip_address = client_address[0]
            return ip_address in self.clients
        
    def update_bid(self, bidder, bid):
        with self.lock:
            if bid > self.highest_bid:
                self.highest_bid = bid
                self.highest_bidder = bidder
                self.last_bid_time = time.time()
                self.chant = 1
                return True
            return False

    def build_status_message(self):
        with self.lock:
            return {
                "request_type": "STATUS",
                "status": "OPEN" if self.chant > 0 else "CLOSE",
                "highest_bid": self.highest_bid,
                "highest_bidder": self.highest_bidder,
                "chant": self.chant,
                "n_clients": len(self.clients),
                "next_auction": None
            }

    def reset(self):
        with self.lock:
            self.highest_bid = 0
            self.highest_bidder = None
            self.last_bid_time = None
            self.chant = 1
