from types import SimpleNamespace
consts = SimpleNamespace()
consts.SEND_SCREENSHOT = "<SEND SCREENSHOT>"
consts.PLAY = "<PLAY>"
consts.ACK = "<ACK>"
consts.END = "<END>"
consts.TERMINATE = "<TERMINATE>"


import socket;
import threading
import time
from ollama import chat




MESSAGE_SIZE = 4096
MAX_CLIENTS = 4

class Server:
    def __init__(self):        
        self.clients = dict()

        SERVER = socket.gethostbyname(socket.gethostname())
        PORT = 8080

        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.bind((SERVER, PORT))

        print("[SERVER] Starting...")

        self.SOCKET.listen()

        while True:
            if len(self.clients) <= MAX_CLIENTS:
                conn, addr = self.SOCKET.accept()
                thread = threading.Thread(target = self.connect_Client, args=(conn, addr))
                thread.start()        
                print(f"[SERVER] Clients: {threading.active_count() - 1}")

    def __del__(self):
        print(f"[SERVER] Closed")
        self.SOCKET.close()


    def connect_Client(self, conn, addr):
        self.clients[addr] = 0

        print(f"[SERVER] New client from {addr}")
        conn.send(consts.PLAY.encode())

        req_action = conn.recv(MESSAGE_SIZE).decode()

        while True:
            self.handle(req_action, conn, addr)
            req_action = conn.recv(MESSAGE_SIZE).decode()
            try:
                if req_action == consts.TERMINATE:
                    break;
            except Exception as e:
                print("[ERROR] Cannot connect to client.", e)
                break;

        print(f"[SERVER] Client from {addr} disconnected")
        
        del self.clients[addr]


    def handle(self, action, conn, addr):
        print(f'[ACTION] {action}')

        match(action):
            case consts.SEND_SCREENSHOT:
                conn.send("Send image size".encode())
                print(f'[Size] {conn.recv(MESSAGE_SIZE).decode()}')
                conn.send("Send data bytes".encode())
                
                with open('Client_submission.jpg', 'wb') as file:
                    data = b'';
                    while True:
                        receivedData = conn.recv(MESSAGE_SIZE)
                        data += receivedData

                        if data[-5:] == consts.END.encode():
                            print("[SERVER] Received client submission.")
                            conn.send("Received image.".encode())
                            file.write(data[:-5])
                            break;     
                    file.close()

                # if not self.check_Image():
                self.clients[addr] += 1

                print(self.clients)
            
            case _:
                raise Exception(f'[Error] Unknown handle command: {action}')


    def check_Image(self):
        res = chat(
            model='llava:7b',
            messages=[{
                'role' : 'user',
                'content' : 'Is there a dog in the image',
                'images' : ['./Client_submission.jpg']
            }]
        )

        msg = res['message']['content']
        print(f'[AI] {msg}')

        return "Yes" in msg[:10]
    
    def check_Scores(self):
        i = 0;
        for key, score in self.clients.items:
            print(f'Client {i}: {self.clients[key]} points')
            i += 1;


newServer = Server()