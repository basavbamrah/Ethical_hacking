
import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
# print(HEX_FILTER)
# print(bool(0))


def hexdump(src, length=16, show=True):
    # print(len(src))
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        # susbstitue the string repr of each character for the corresponding character in raw string
        printtable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        # :02X converts the number into two digit hex representation
        # print('hexa = ', hexa)
        hexwidth = length*3
        # print(i)
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printtable}')
    # print(results)
    if show:
        for line in results:
            print(line)
        else:
            return results

# hexdump('python rocks\n and proxies roll\n')


def receive_from(connection):
    buffer = b""
    # connection.recv(4096)
    print(connection)
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer


def request_handler(buffer):
    # perform packet modification
    return buffer


def response_handler(buffer):
    # perform packet modification
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    # remote_socket.settimeout(5)
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[===>] Sending  %d bytes from localhost. " % len(remote_buffer))
        client_socket.send(remote_buffer)
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print('[===>] Received %d bytes from localhost. ' %
                  len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_buffer)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote " % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost. ")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more Data, connection closed ")
            break

# server loop creates a socket and then binds to the local host and listens
# does all the sending and receiving of bits


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('Problem on bind: %r' % e)
        print(e)
        print("[!!] Failed to listern on %s:%d" % (local_host, local_port))
        print("Check for other listerning sockets or change permissions")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # print the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # start a thread to talk to the remote server

        proxy_thread = threading.Thread(target=proxy_handler, args=(
            client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("usage: ./proxy.py [local host] [local port]", end="")
        print("[remotehost] [remoteport] [receive_first]")
        print("Example ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True

    else:
        receive_first = False
    print('Yes')
    server_loop(local_host, local_port, remote_host,
                remote_port, receive_first)


if __name__ == '__main__':
    main()
