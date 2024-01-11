import socket
import os
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
HEADER_SIZE = 256


def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate:
            return True
        time.sleep(period)
    return False


def handle_send_file(
        files_folder, file_name, client):
    file_name_path = os.path.join(files_folder, file_name)

    file_size = os.path.getsize(file_name_path)

    b_filename = bytes(file_name, FORMAT)

    b_filesize = bytes(str(file_size), FORMAT)

    # client.send(f"{file_name}@{str(file_size)}".encode(FORMAT))

    filename_length = len(b_filename)
    print("filename_length >> ", filename_length)

    filesize_length = len(b_filesize)
    print("filesize_length >> ", filesize_length)

    data = b_filename + b'@' + b_filesize + b' ' * \
        (HEADER_SIZE - (filename_length + filesize_length + len(b'@')))

    with open(file_name_path, 'rb') as f:
        data += f.read(file_size)
    client.send(data)
    # time.sleep(15)
    msg = client.recv(4).decode(FORMAT)
    wait_until(msg == "next", 15)
    print("msg >>> ", msg)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    files = os.listdir("files")
    print('files >> ', files)
    for file in os.listdir("files"):
        handle_send_file("files", file, client)
    # handle_send_file("files", files[0], client)
    # handle_send_file("files", files[1], client)
    # handle_send_file("files", files[2], client)

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
