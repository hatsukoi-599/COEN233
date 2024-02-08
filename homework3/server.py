import math
import socket
import json
import sys
import threading
import time
import logging
from auction_state import AuctionState
auction_state = AuctionState()

logging.basicConfig(filename='server.log',   
                    level=logging.INFO,      
                    filemode='w',            
                    format='%(asctime)s - %(levelname)s - %(message)s') 

MESSAGE = {
    200: 'OK',
    400: 'Bad Request'
}

def handle_request(client_address, client_socket, request):
    global auction_state
    logging.info(f"Handling request from {client_address}")
    request_json = json.loads(request.split('\r\n\r\n')[-1])
    data = None
    status_code = 200

    if request_json["request_type"] == "JOIN":
        auction_state.add_client(client_address, client_socket)
        data = auction_state.build_status_message();
        logging.info(f"Client {client_address} joined. Total clients: {len(auction_state.clients)}")
    
    elif request_json["request_type"] == "BID":
        new_bid = request_json.get("bid_amount") 
        if new_bid is not None:  
            if new_bid > auction_state.highest_bid and auction_state.client_joined(client_address):
                auction_state.update_bid(client_address, new_bid)
                data = {"request_type":"BID_ACK","bid_status":"ACCEPTED"}
                logging.info(f"New bid accepted from {client_address}: {new_bid}")
            else:
                data = {"request_type":"BID_ACK","bid_status":"REJECTED"}
                status_code = 400
                logging.info(f"Bid rejected from {client_address}: {new_bid}")
        else:
            status_code = 400
            data = {"error": "Missing bid amount"}
            logging.warning(f"Malformed bid request from {client_address}")

    
    return build_http_response(status_code, data);

def build_http_response(status_code, data):
    body = json.dumps(data)
    
    return (
        f"HTTP/1.1 {status_code} {MESSAGE[status_code]}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

def broadcast_status():
    global auction_state
    logging.info("Broadcasting status")
    while not stop_server:
        time.sleep(0.01)
        response = None
        last_bid_time = auction_state.last_bid_time
        if last_bid_time is None or math.floor((time.time() - last_bid_time) / 10) <= auction_state.chant:
            continue
        if auction_state.chant <= 3:
            auction_state.chant += 1
           
        if auction_state.chant > 3:
            msg = {"request_type":"CLOSE", "highest_bid": auction_state.highest_bid, "highest_bidder":auction_state.highest_bidder}
            response = build_http_response(200, msg)
            logging.info(f"Auction end - Winner: {auction_state.highest_bidder} with a bid of {auction_state.highest_bid}")
            print('Auction ended, starting a new one.')

        else:
            response = build_http_response(200, auction_state.build_status_message())

        clients_copy = auction_state.clients.copy()    
        for client_address, client_socket in clients_copy.items():
            try:
                # check socket is closed or not before send the response
                if client_socket.fileno() == -1:
                    logging.info(f"Socket for {client_address} already closed, removing client.")
                    auction_state.remove_client(client_address)
                    continue

                client_socket.sendall(response.encode('utf-8'))
                logging.info(f"Status broadcasted to {client_address}")
            except BrokenPipeError:
                print(f"Broken pipe error broadcasting to {client_address}")
                client_socket.close()  # Close the socket
                auction_state.remove_client(client_address)    
            except Exception as e:
                print(f"Error broadcasting to {client_address}: {e}")
                auction_state.remove_client(client_address) 
        
        if auction_state.chant > 3:
            auction_state.reset()    

def handle_client_connection(client_socket, client_address):
    global auction_state
    logging.info(f"New connection from {client_address}")
    print(f"New connection from {client_address}")
    try:
        while not stop_server:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            response = handle_request(client_address, client_socket, data)
            client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        logging.info(f"Disconnected from {client_address}")
        print(f"Disconnected from {client_address}")
    finally:
        logging.info(f"Connection closed and cleaned up for {client_address}")
        client_socket.close()  # Close the socket
        auction_state.remove_client(client_address)  

stop_server = False

def start_server(host='0.0.0.0', port=0):
    global stop_server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    port = server_socket.getsockname()[1]
    server_socket.listen()
    print(f"Listening on {socket.gethostbyname(socket.gethostname())}:{port}")
    logging.info(f"Server started on {host}:{port}")

    broadcast_thread = threading.Thread(target=broadcast_status)
    broadcast_thread.start()

    try:
        while not stop_server:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        logging.info("Server shutdown initiated by KeyboardInterrupt")
    finally:
        stop_server = True
        server_socket.close()
        logging.info("Server shutdown completed")

if __name__ == '__main__':
    start_server()
