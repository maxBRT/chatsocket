import socket 
import threading

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception:
                    pass  # Ignore send errors

def handle_client(client_socket, client_address):
    """Handle individual client connection in a separate thread"""
    print(f"Connection established with {client_address}")
    with clients_lock:
        clients.append(client_socket)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received from {client_address}: {message}")
            broadcast(f"{client_address}: {message}".encode('utf-8'), client_socket)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()
        print(f"Connection closed with {client_address}")

def start_server():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")
        print("Server can now handle multiple clients simultaneously!")
        
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Create a new thread for each client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address)
            )
            client_thread.daemon = True  # Thread will exit when main program exits
            client_thread.start()
            
            print(f"Active connections: {threading.active_count() - 1}")  # -1 for main thread

if __name__ == "__main__":
    start_server()