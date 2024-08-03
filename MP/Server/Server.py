# CUSTOM PROTOCOL CONSTANTS
from types import SimpleNamespace
consts = SimpleNamespace()
consts.SEND_SCREENSHOT = "<SEND SCREENSHOT>"
consts.PLAY = "<PLAY>"
consts.ACK = "<ACK>"
consts.SCORE = "<SCORE>"
consts.END = "<END>"
consts.TERMINATE = "<TERMINATE>"

# MAIN PROGRAM
import socket;
import threading
import json

# IMAGE RECOGNITION MODEL
from ollama import chat

# TOPIC SELECTION
from random import choice

# FOR BACKOFF TIME
from time import sleep
from random import randint

# CONSTANTS
TOPICS = ['Color white','Car', 'House', 'Tree', 'Animal', 'Ball']
PATHS = {
    'Submission_Folder' : './Submissions/'
    # 'Submission_Folder' : 'Server/Submissions/'
}
MESSAGE_SIZE = 4096
MAX_CLIENTS = 4



class Server:
    def __init__(self):        
        '''
            Initializes the server socket and loops it to accept new client connections.
        '''
        # VARIABLES
        self.client_scores = dict()
        self.active_connections = []
        # FLAG
        self.IS_SCORING = False

        # CREATE THE SERVER SOCKET
        SERVER = socket.gethostbyname(socket.gethostname())
        PORT = 8080

        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.bind((SERVER, PORT))

        print("[SERVER] Active")
        self.SOCKET.listen()

        # SERVER SOCKET ACCEPT LOOP
        while True:
            if len(self.active_connections) <= MAX_CLIENTS:
                conn, addr = self.SOCKET.accept()
                thread = threading.Thread(target = self.connect_Client, args=(conn, addr))
                thread.start()        
                print(f"[SERVER] Clients: {threading.active_count() - 1}")

    # CLEAN UP
    def __del__(self):
        '''
            Close the server socket.
        '''
        print(f"[SERVER] Closed")
        self.SOCKET.close()



    def connect_Client(self, conn, addr):
        '''
            Handle new connections.
            Clean up on connection lost (except the scores dictionary).
        '''

        # GET THE USER'S USERNAME (1st msg)
        username = conn.recv(MESSAGE_SIZE).decode()
        
        # ADD AS NEW SCORE ENTRY IF NOT YET IN LIST
        if str(username) not in self.client_scores.keys():
            print(f'New user: {username}')
            self.client_scores[username] = 0
        
        # NOT ACTUALLY UTILIZED BCUZ THREADING DOES THIS BETTER
        self.active_connections.append(conn)

        print(f"[SERVER] New client ({username}) from {addr}")
        

        '''
            Client handle loop.
            1. Send PLAY protocol
            2. Wait for ACK
            3. Send random TOPIC
            4. Wait for IMAGE
            5. Stop receiving when END protocol encountered
            6. Save image.
            7. Pass to scoring.
            8. Repeat
        '''
        while True:
            try:
                # Send PLAY
                print(f'[SERVER] Starting new round for {username}...')
                conn.send(consts.PLAY.encode())
                
                print(f'[SERVER] Sent play command to {username}')
                ack_msg = conn.recv(MESSAGE_SIZE).decode()
                
                # SEND random TOPIC to player
                search_item = choice(TOPICS)
                print(f'[TOPIC] Find a {search_item}')
                conn.send(search_item.encode())
                
                # GAME Client plays...
                
                # Receive image sent
                data = b''
                while data[-5:] != consts.END.encode():
                    data += conn.recv(MESSAGE_SIZE)
                
                # Save the player submission
                SAVED_FILE_PATH = PATHS['Submission_Folder'] +username+'.jpg'
                with open(SAVED_FILE_PATH, 'wb') as file:
                    file.write(data[:-5])
                    file.close()
                

                # Score the player submission
                if self.check_Image(SAVED_FILE_PATH, search_item):
                    self.client_scores[username] += 1
                print(self.client_scores)

                # Send scores to player
                conn.send(consts.SCORE.encode())
                b_scores = json.dumps(self.client_scores).encode()

                ack_msg = conn.recv(MESSAGE_SIZE).decode()
                if ack_msg == consts.ACK:
                    print("[SERVER] Sending scores...")
                    conn.send(b_scores)
                else:
                    raise Exception("[ERROR] Can't send scores")

            except Exception as e:
                print(e)
                break;


        # END OF CLIENT HANDLE LOOP
        print(f"[SERVER] Client {username} from {addr} disconnected")
        
        # CLEAN UP CLIENT SOCKET
        self.active_connections.remove(conn)
        conn.close()
        print(f'[SERVER] Clients remaining {len(self.active_connections)}')


    def check_Image(self, SAVED_FILE_PATH, search_item):
        '''
            Score the image using llava image recognition.
        '''
        # INCREMENTING BACKOFF PERIOD.
        # ONLY 1 INSTANCE OF THE AI CAN BE RAN AT A TIME
        wait_time = 0
        while self.IS_SCORING:
            wait_time += randint(5, 10)
            print(f'[SCORING] Wait for {wait_time} before processing {SAVED_FILE_PATH}')
            sleep(wait_time)
        
        # ACTIVATE FLAG TO BLOCK 2ND AI RUNNING
        self.IS_SCORING = True
        
        # START SCORING...
        print(f'[SERVER] Processing {SAVED_FILE_PATH}')
        
        # ASK THE MODEL IF THE IMAGE CONTAINS THE TOPIC SEARCHED
        res = chat(
            model='llava:7b',
            messages=[{
                'role' : 'user',
                'content' : 'Is there a ' + search_item + ' in the image',
                'images' : [SAVED_FILE_PATH]
            }]
        )

        # CHECK RESULTS 
        msg = res['message']['content']
        print(f'[AI] {msg}')
        
        # DEACTIVATE FLAG
        self.IS_SCORING = False

        # SEND RESULTS
        return "yes" in msg[:10].lower()



# Create server instance
Server()