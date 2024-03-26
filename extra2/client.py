

# @Author: Xiaoxiao Jiang > xjiang3@scu.edu
# @Partner: WeiHao Liu > wliu4@scu.edu

import socket
import sys
import pickle
from logger_helper import setup_logger

logger = setup_logger('csen233extra2JiangXiaoxiao_client.log')

def tcp_client(host, port):

    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            
            server_address = (host, port)
            client_socket.connect(server_address) 
            logger.info(f"Attempting to connect to {host}:{port}")

            data = client_socket.recv(1024)
            logger.info(f"Receive raw data from server: {data}")
            
            public_key = pickle.loads(data)
            logger.info(f"Loads public key from raw data: {public_key}")

            msg = input('please input msg:')
            logger.info(f"The original message: {msg}")

            encrypted_msg = knapsack_encrypt(msg, public_key)
            logger.info(f"Encrypted msg: {encrypted_msg}")

            encrypted_msg_bytes = pickle.dumps(encrypted_msg)
            logger.info(f"Encrypted message transfered to bytes stream: {encrypted_msg_bytes}")
            client_socket.sendall(encrypted_msg_bytes)
    
    except Exception as e:
        logger.error("Failed to establish connection or key exchange", exc_info=True)


def knapsack_encrypt(msg, public_key):
    binary_msg = ''.join(format(ord(c), '08b') for c in msg)
    encrypted_msg = []

    for i in range(0, len(binary_msg), len(public_key)):
        block = binary_msg[i:i + len(public_key)]
        if len(block) < len(public_key):
            block += '0' * (len(public_key) - len(block))  

        encrypted_block = sum([int(bit) * key for bit, key in zip(block, public_key)])
        encrypted_msg.append(encrypted_block)

    return encrypted_msg


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py server_host server_port")
    else:
        tcp_client(sys.argv[1], int(sys.argv[2]))