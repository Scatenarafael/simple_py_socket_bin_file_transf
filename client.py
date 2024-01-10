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
   
    # client.send(file_name.encode(FORMAT))

    file_size = os.path.getsize(file_name_path)
    # print("filesize >>> ", file_size)

    # client.send(str(file_size).encode(FORMAT))

    with open(file_name_path, 'rb') as f:
        data = f.read(file_size)
    client.send(data)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # for file in os.listdir("files"):
    #     handle_send_file("files", file, client)
    
    handle_send_file("files", "3d_person_vectors.jpg", client)

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
