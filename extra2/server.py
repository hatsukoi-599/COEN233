

# @Author: Xiaoxiao Jiang > xjiang3@scu.edu
# @Partner: WeiHao Liu > wliu4@scu.edu

import random
import math
import socket
import pickle
from logger_helper import setup_logger

logger = setup_logger('csen233extra2JiangXiaoxiao_server.log')

# Constants
PORT = 8008

def tcp_server():
	private_key = generate_private_key()
	logger.info(f"Private key: {private_key}")

	public_key, q, r = generate_public_key(private_key)
	logger.info(f"Public key: {public_key}")

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	bind_to_local(server_socket)
	
	server_socket.listen(1)

	try:
		client_socket, addr = server_socket.accept()
		logger.info(f"Connection from {addr}")

		public_key_bytes = pickle.dumps(public_key)
		logger.info(f"Public key transfered to bytes stream: {public_key_bytes}")
		
		# Send public key to client
		client_socket.sendall(public_key_bytes)
		
		logger.info(f"Waiting for client's encrypted message ... ")

		ciphertext = client_socket.recv(1024)
		logger.info(f"Raw ciphertext in bytes stream received: {ciphertext}")

		encrypted = pickle.loads(ciphertext)
		logger.info(f"Load ciphertext from raw bytes stream: {encrypted}")
		
		decrypted = knapsack_decrypt(encrypted, private_key, q, r)
		logger.info(f"Decrypted message: {decrypted}")

		client_socket.close()

	except Exception as e:
		logger.error("Server failed to start or accept connections", exc_info=True)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def knapsack_decrypt(encrypted_msg, private_key, q, r):
    r_inv = mod_inverse(r, q)
    decrypted_msg = ''

    for block in encrypted_msg:
        total = (block * r_inv) % q

        decrypted_block = []
        for weight in reversed(private_key):
            if total >= weight:
                total -= weight
                decrypted_block.append('1')
            else:
                decrypted_block.append('0')

        decrypted_block.reverse()
        decrypted_msg += chr(int(''.join(decrypted_block), 2))

    return decrypted_msg

def generate_private_key(n = 8):

	sequence = [random.randint(1, 10)]
	for _ in range(1, n):
		sequence.append(random.randint(sum(sequence) + 1, 2 * sum(sequence)))
	return sequence


def generate_public_key(private_key):
	sum_sequence = sum(private_key)
	q = random.randint(sum_sequence + 1, 2 * sum_sequence + 1)
	
	r = -1
	while True:
		r = random.randint(1, q)
		if math.gcd(r, q) == 1:
			break
	
	pub_key = [r * w % q for w in private_key]

	return pub_key, q, r

def bind_to_local(server_socket):
	try:
		local_ip = socket.gethostbyname(socket.gethostname())
	except socket.gaierror:
		local_ip = "127.0.0.1"

	server_socket.bind((local_ip, PORT))
	logger.info(f"Server running on {local_ip}:{PORT}")


if __name__ == "__main__":
	tcp_server()
