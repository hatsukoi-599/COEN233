import math
import socket
import json
import threading
import time
from auction_state import AuctionState
auction_state = AuctionState()

MESSAGE = {
    200: 'OK',
    400: 'Bad Request',
    503: 'Service Unavailable'
}

def handle_request(client_address, client_socket, request):
    global auction_state
    request_json = json.loads(request.split('\r\n\r\n')[-1])
    data = None
    status_code = 200

    if request_json["request_type"] == "JOIN":
        auction_state.add_client(client_address, client_socket)
        data = auction_state.build_status_message();
    
    elif request_json["request_type"] == "BID":
        new_bid = request_json.get("bid_amount") 
        if new_bid is not None:  
            if new_bid > auction_state.highest_bid and client_address in auction_state.clients:
                auction_state.update_bid(client_address, new_bid)
                data = {"request_type":"BID_ACK","bid_status":"ACCEPTED"}
            else:
                data = {"request_type":"BID_ACK","bid_status":"REJECTED"}
                status_code = 400
        else:
            status_code = 400
            data = {"error": "Missing bid amount"}

    
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
    while True:
        time.sleep(0.01)
        response = None
        last_bid_time = auction_state.last_bid_time
        if last_bid_time is None or math.floor((time.time() - last_bid_time) / 10) <= auction_state.chant:
            continue
        if auction_state.chant < 3:
            auction_state.chant += 1
           
        if auction_state.chant == 3:
            msg = {"request_type":"CLOSE", "highest_bid": auction_state.highest_bid, "highest_bidder":auction_state.highest_bidder}
            response = build_http_response(503, msg)
            auction_state.reset()
            print('Aunction End')

        else:
            response = build_http_response(200, auction_state.build_status_message())

        clients_copy = auction_state.clients.copy()    
        for client_address, client_socket in clients_copy.items():
            try:
                client_socket.sendall(response.encode('utf-8'))
                if auction_state.chant == 3:
                    client_socket.close()
                    print(f"Connection closed for {client_socket}")
                
            except Exception as e:
                print(f"Error broadcasting to {client_address}: {e}")
                auction_state.remove_client(client_address)
            

def handle_client_connection(client_socket, client_address):
    global auction_state
    print(f"New connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            response = handle_request(client_address, client_socket, data)
            client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling connection from {client_address}: {e}")
   

def start_server(host='0.0.0.0', port=8000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Listening on {host}:{port}")

    broadcast_thread = threading.Thread(target=broadcast_status)
    broadcast_thread.start()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()