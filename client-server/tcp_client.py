from http import client
from pydoc import cli
import socket
from urllib import response
target_host = '127.0.0.1'
target_port = 9998

#  create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))
# SEND DATA
client.send(b'Hi there!!')
# receive some data
response = client.recv(4096).decode()

print(response)

client.close()
