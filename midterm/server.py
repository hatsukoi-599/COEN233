#import socket module
from socket import *
import sys  # In order to terminate the program
import logging
import random

logging.basicConfig(filename='csen233midtermJiangXiaoxiao.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

try: 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverPort = 8100
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    local_ip = gethostbyname(gethostname())
    logging.info(f"Server started, listening on {local_ip}:{serverPort}")
    print(f"Use the URL to connect to server: http://{local_ip}:{serverPort}")

    while True:
        logging.info('Ready to serve...')
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            # Randomly choose whether to send a normal response or an error
            if random.choice([True, False]):
                # If chosen to respond normally, prepare and send an HTTP 200 OK response
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                response_content = "<html><body><h1>Hello, World!</h1></body></html>"
                connectionSocket.send(response_header.encode() + response_content.encode())
                logging.info(f"Sent normal response to {addr}")
            else:
                 # If chosen to respond with an error, prepare and send an HTTP 404 Not Found response
                error_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
                connectionSocket.send(error_response.encode())
                logging.error(f"Sent error response (404 Not Found) to {addr}")
        
        finally:
            connectionSocket.close()
            logging.info(f"Connection with {addr} closed")

except KeyboardInterrupt:
    logging.info("Server shutdown initiated")
    serverSocket.close()
    logging.info("Server shut down")
    sys.exit()
