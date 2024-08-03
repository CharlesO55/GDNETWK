import socket
import time


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 8080

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.connect((SERVER, PORT))
SOCKET.send(b'Hi world. Id')


time.sleep(5)
SOCKET.send('<END>'.encode('utf-8'))



SOCKET.close()