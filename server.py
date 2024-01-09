
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    data = b''
    while True:
        received = conn.recv(1024)
        if not received:
            break
        else:
            data += received

    print("len(data) >>> ", len(data))
    try:
        with open("uploads/received_img.jpg", 'wb') as f:
            f.write(data)

        print("File Successfuly Saved!")
    except FileNotFoundError:
        print("Something went wrong")
        conn.close()

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
