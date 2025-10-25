from socket import *
import pathlib as Path
import struct

SERVER_HOST = '10.0.0.196' # local Ip address
SERVER_PORT = 5050         # random port number

test_file = Path.Path("test_files/my_resume.pdf")

def setup_client():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Client connected: [TCP] {SERVER_HOST} : {SERVER_PORT}")

    return client_socket

def send_file(client_socket, file_path=test_file):

    try:
        filename_bytes = file_path.name.encode("utf-8")
        header = struct.pack("!IQ", len(filename_bytes), file_path.stat().st_size)
        client_socket.sendall(header)
        client_socket.sendall(filename_bytes)
        print(f"[TCP] → Sending file")

        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                client_socket.sendall(chunk)

        print("[TCP] → File successfully sent")

    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
    except Exception as e:
        print(f"[Error] Failed to send file: {e}")
    finally:
        client_socket.close()
        print("[TCP] Connection closed.")

def main():
    client_socket = setup_client()
    send_file(client_socket)

if __name__ == "__main__":
    main()