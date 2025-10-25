from socket import *
import threading
import pathlib as Path
import struct

SERVER_HOST = '10.0.0.196' # local Ip address
SERVER_PORT = 5050         # random port number
BACKLOG = 100              # max queued connections

save_dir = Path.Path("uploads")
save_dir.mkdir(exist_ok=True)


def setup_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(BACKLOG)
    print(f"Server is ready: [TCP] Listening on {SERVER_HOST} : {SERVER_PORT}")

    return server_socket


def handle_client(connection, client_address):
    print(f"[TCP] Connected by {client_address}")
    try:
        while True:
            header = connection.recv(12)
            name_len, file_size = struct.unpack("!IQ", header)
            file_name = connection.recv(name_len).decode("utf-8")
            if not file_name:
                break
            
            with open(save_dir / file_name, "wb") as f:
                remaining = file_size
                while remaining:
                    chunk = connection.recv(min(4096, remaining))
                    if not chunk:
                        raise ConnectionError("Unexpected EOF")
                    f.write(chunk)
                    remaining -= len(chunk)

            print(f"[TCP] File saved: {save_dir / file_name}")
            connection.sendall(b"File received successfully")

    except Exception as e:
        print(f"[TCP] Handler error for: {client_address} : {e}")
    finally:
        connection.close()
        print(f"[TCP] Connection closed: {client_address}")

def main():
    server_socket = setup_server()

    try:
        while True:
            connection, client_address = server_socket.accept()
            # start new thread per client
            thread = threading.Thread(target=handle_client, args=(connection, client_address), daemon=True)
            thread.start()
            
    except KeyboardInterrupt:
        print("\n [TCP] Shutting down..")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()