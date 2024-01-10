import socket
import os


IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def handle_send_file(
        files_folder, file_name, client):

    file_name_path = os.path.join(files_folder, file_name)

    file_size = os.path.getsize(file_name_path)
    
    client.send(f"{file_name}@{str(file_size)}".encode(FORMAT))

    with open(file_name_path, 'rb') as f:
        data = f.read(file_size)
    client.send(data)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    files = os.listdir("files")

    # for file in os.listdir("files"):
    #     handle_send_file("files", file, client)
    i = 0

    handle_send_file("files", files[i], client)

    while True:
        msg = client.recv(SIZE).decode(FORMAT)
        print("while >> msg:", msg)
        if msg == "next" and i+1 < len(files):
            i += 1
            handle_send_file("files", files[i], client)
        else:
            break
    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
