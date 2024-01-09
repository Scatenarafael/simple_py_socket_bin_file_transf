import socket
import os


IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    file_size = os.path.getsize("img.jpg")
    print('file_size >>> ', file_size)
    f = open('img.jpg', 'rb')

    data = f.read(file_size)
    print('len(data) >> ', len(data))
    # with open('img.jpg', 'rb') as f:
    #     data = f.read(6500_000)
    # remaining = file_size
    # data = b''
    # while remaining > 0:
    #     if remaining > 0 and remaining < 1024:
    #         print("if remaining >> ", remaining)
    #         data += f.read(remaining)
    #     else:
    #         print("else remaining >> ", remaining)
    #         data += f.read(1024)
    #     remaining -= 1024
    client.send(data)

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
