
import socket
import threading
import os
import tqdm
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
HEADER_SIZE = 128


def receive_file(conn, addr):
    while True:
        msg = conn.recv(HEADER_SIZE).decode(FORMAT)
        if msg:
            file_name, file_size = msg.split("@")
            print("file_name: ", file_name)
            print("file_size: ", file_size)

            progress = tqdm.tqdm(
                # range(int(file_size)),
                f"Receiving {file_name}",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                total=int(file_size)
            )

            data = b''
            t1 = time.perf_counter()

            while len(data) < int(file_size):
                received = conn.recv(512)
                data += received
                progress.update(512)

            t2 = time.perf_counter()

            print("time receive file >>> ", (t2 - t1))
            print("len(data) >>> ", len(data))
            try:
                t3 = time.perf_counter()
                with open(f"uploads/received_{file_name}", 'wb') as f:
                    f.write(data)

                if (os.path.exists(f"uploads/received_{file_name}") and
                        os.path.getsize(f"uploads/received_{file_name}") > 0):
                    t4 = time.perf_counter()

                    print("time to write file >>> ", (t4 - t3))
                    print("File Successfuly Saved!")
                else:
                    print("Could no save file")
            except FileNotFoundError:
                print("Something went wrong")
                conn.close()
            # print(f"[DISCONNECTED] {addr} disconnected")
            # conn.close()
        else:
            break


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    receive_file(conn, addr)

    # print(f"[DISCONNECTED] {addr} disconnected")
    # conn.close()


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
        thread.join()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
