from http import client
from multiprocessing.reduction import ACKNOWLEDGE
import socket
import threading
from urllib import request

ip = '0.0.0.0'
port = 9998


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # pass the ip and port on which we want the server to listern
    server.bind((ip, port))

    # tell the server to listern
    # the argument to listen tells the socket library that we want it to queue up as many as 5 connect requests (the normal max) before refusing outside connections
    server.listen(5)
    print(f'[*] Listerning on {ip}:{port}')

    while True:
        # client socket details is stored in client and the remote connection details is stored in address variable
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        #  Now create thread that points to handle client function
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):  # performs recv() and send ACKNOWLEDGEMENT

    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')


if __name__ == '__main__':
    main()
