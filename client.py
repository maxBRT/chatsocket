import socket 
import sys
import threading

def receive_messages(client_socket):
    """Thread function to continuously receive messages"""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Server disconnected")
                break
            print(f"\n{data.decode('utf-8')}")
            print("Enter a message: ", end='', flush=True)
    except Exception as e:
        print(f"\nError receiving: {e}")

def start_client():
    # Get server IP from command line argument or prompt user
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = input("Enter server IP address (or press Enter for localhost): ").strip()
        if not host:
            host = '127.0.0.1'
    
    port = 12345
    
    print(f"Attempting to connect to {host}:{port}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")
            print("Type your messages (type 'quit' to exit):")
            
            # Start receive thread
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            # Main loop for sending messages
            while True:
                message = input("Enter a message: ")
                if message.lower() == 'quit':
                    break
                client_socket.send(message.encode('utf-8'))
                
        except ConnectionRefusedError:
            print(f"Connection refused. Make sure the server is running on {host}:{port}")
        except Exception as e:
            print(f"Error connecting: {e}")
            
if __name__ == "__main__":
    start_client()