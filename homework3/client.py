import socket
import threading
import json

# URL for the server, will be initialized later
url = None

def send_requests(sock):
    """Handles sending requests from the client to the server in a dedicated thread."""
    try:
        while True:
            request_type = input("Enter request type (JOIN, BID, or QUIT to exit): ")
            request = None
            if request_type.upper() == "QUIT":
                break  # Exit loop if user wants to quit
            if request_type.upper() == "BID":
                bid_amount = float(input("Enter your bid amount: "))
                # Prepare request data for a bid
                request = pack_data(request_type, bid_amount)
            else:
                # Prepare request data for joining
                request = pack_data(request_type)
            # Send the prepared request to the server
            sock.sendall(request.encode())
    except Exception as e:
        print(f"Error sending requests: {e}")

def pack_data(request_type, bid_amount=None):
    """Constructs the data payload for the HTTP request."""
    data = f'{{"request_type": "{request_type}"'
    if bid_amount is not None:
        data += f', "bid_amount": {bid_amount}'
    data += '}'

    # Calculate the content length for inclusion in the HTTP header
    content_length = len(data)
    
    # Build the complete HTTP POST request with headers
    request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {url}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {content_length}\r\n"
        "\r\n"
        f"{data}"
    )
    return request

def receive_responses(sock):
    """Responsible for receiving responses from the server in a separate thread."""
    try:
        while True:
            response = sock.recv(4096)
            if not response:
                break
            # Decode response from bytes to string
            response_str = response.decode('utf-8')
            # Split response into headers and body
            headers, body = response_str.split('\r\n\r\n', 1)
            # Parse JSON from response body
            response_json = json.loads(body)
            print("Received:", response_json)
    except Exception as e:
        print(f"Error receiving responses: {e}")
    finally:
        sock.close()
        return   

def start_client(server_host, server_port):
    """Initializes the client and connects to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, server_port))
        # Start thread to receive responses from the server
        threading.Thread(target=receive_responses, args=(sock,), daemon=True).start()
        # Handle sending requests in the main thread
        send_requests(sock)

if __name__ == '__main__':
    server_host = '0.0.0.0'
    server_port = 8000
    url = f"{server_host}:{server_port}"
    start_client(server_host, server_port)
