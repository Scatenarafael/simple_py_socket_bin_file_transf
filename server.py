
import socket
import threading
import os
import tqdm

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    msg = conn.recv(SIZE).decode(FORMAT)

    file_name, file_size = msg.split("@")
    print("file_name: ", file_name)
    print("file_size: ", file_size)

    progress = tqdm.tqdm(
                    range(int(file_size)),
                    "Receiving img.jpg",
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024
                    )

    data = b''
    while True:
        received = conn.recv(1024)
        if not received:
            break
        else:
            data += received
        progress.update(1024)

    print("len(data) >>> ", len(data))
    try:
        with open(f"uploads/received_{file_name}", 'wb') as f:
            f.write(data)

        if (os.path.exists(f"uploads/received_{file_name}") and
                os.path.getsize(f"uploads/received_{file_name}") > 0):
            conn.send("next".encode(FORMAT))
            print("File Successfuly Saved!")
        else:
            conn.send("finished".encode(FORMAT))
            print("Could no save file")
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
