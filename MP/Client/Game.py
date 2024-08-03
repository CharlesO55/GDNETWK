# GUI
from tkinter import *
import customtkinter
from PIL import Image

# SOCKETS
import socket
from threading import Thread

# OS FILES
import os.path
import json

# WEB PLAY
from selenium import webdriver
from pyautogui import screenshot
from pynput.keyboard import Listener as keyboard_Controls

from time import sleep

# CUSTOM PROTOCOL CONSTANTS
from types import SimpleNamespace
consts = SimpleNamespace()
consts.SEND_SCREENSHOT = "<SEND SCREENSHOT>"
consts.PLAY = "<PLAY>"
consts.ACK = "<ACK>"
consts.SCORE = "<SCORE>"
consts.END = "<END>"
consts.TERMINATE = "<TERMINATE>"
PATHS = {
    # 'wiki' : 'Client/Wikipedia.png',
    # 'submission' : 'Client/screenshot.jpg'
    'wiki' : './Wikipedia.png',
    'submission' : './screenshot.jpg'
}


MESSAGE_SIZE = 4096
# SCREENSHOT_PATH = 'Client/screenshot.jpg'
SCREENSHOT_PATH = './screenshot.jpg'


class GameClient:
    def __init__(self):
        '''
            Create the app GUI and game loop.
        '''
        # FLAGS for resuming threads
        self.START_ROUND = False
        self.LISTEN_CMD = False

        # GAME THREAD for opening and screenshoting web results. 
        self.game_loop = Thread(target=self.start_round)
        self.game_loop.start()

        # APP gui with ctkinter 
        self.create_GUI()
        

    def __del__(self):
        # CLEAN UP
        if self.SOCKET:
            self.SOCKET.send(consts.TERMINATE.encode())
            self.SOCKET.close()
        print("[CLIENT] Connection and Client closed")
        
        # CLOSE APP gui
        self.root.quit()


    def create_GUI(self):
        '''
            Create the GUI elements.
            Bind the start function to btn_start.
            Activate default GUI loop.
        '''
        customtkinter.set_appearance_mode("light") 
        customtkinter.set_default_color_theme("dark-blue") 

        self.root = customtkinter.CTk()
        self.root.geometry('500x500')

        self.frame = customtkinter.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=60, fill='both', expand=True)

        self.image = customtkinter.CTkImage(light_image=Image.open(PATHS['wiki']),
            dark_image=Image.open(PATHS['wiki']),
            size=(250,250))
        self.image_holder = customtkinter.CTkLabel(self.root, text="", image=self.image)


        self.label = customtkinter.CTkLabel(master=self.frame, text='Wiki Links', font=('Arial', 32))
        self.entry = customtkinter.CTkEntry(master=self.frame, placeholder_text='Username')
        self.btn_start = customtkinter.CTkButton(master=self.frame, text='Play', command=self.start)
        self.score_label = customtkinter.CTkLabel(master=self.frame, text='Scores', font=('Arial', 12))

        self.image_holder.pack()
        self.label.pack(pady=12, padx=10)
        self.entry.pack(pady=12, padx=10)
        self.btn_start.pack(pady=12, padx=10)
        self.score_label.pack()

        # GUI display loop
        self.root.mainloop()


    def update_score_display(self, scores):
        '''
            Update the score label.
        '''
        self.score_label.destroy()

        text = ''
        for name in scores:
            text += str(name) + ' : ' + str(scores[name])
            text += '\n'
        
        self.score_label = customtkinter.CTkLabel(master=self.frame, text=text, font=('Arial', 12))
        self.score_label.pack()
        print('[GUI] Updated scores')

    
    def start(self):
        '''
            Start function called on button press.
            Begins the connection.
            Also remove the button.
        '''
        if self.entry.get() != '':
            self.btn_start.destroy()
            self.connect(self.entry.get())

    def connect(self, username):
        '''
            Creates the socket connections.
            Starts socket loop thread.
        '''
        SERVER = socket.gethostbyname(socket.gethostname())
        PORT = 8080

        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # CONNECT
            self.SOCKET.connect((SERVER, PORT))
            print("[CLIENT] Connected to server.")
            self.SOCKET.send(username.encode())

            # BEGIN SOCKET LOOP
            # self.listen_to_server()
            self.listener_loop = Thread(target=self.listen_to_server)
            self.listener_loop.start()
            self.LISTEN_CMD = True

        except Exception as e:
            print(e)
            self.root.quit()

    def listen_to_server(self):
        '''
            Socket loop. 
            1. Listens for server PLAY protocol.
            2. Sends ACK response.
            3. Listens for server chosen topic.
            4. Updates GUI
            5. Disable socket loop flag and activate mark game loop flag. 
        '''
        while True:
            if self.LISTEN_CMD:
                # STOP LOOPING LISTENING WHILE GAME IS ACTIVE
                self.LISTEN_CMD = False

                # RECEIVE PLAY PROTOCOL
                print(f'[CLIENT] Waiting for server command...')
                msg = self.SOCKET.recv(MESSAGE_SIZE).decode()
                print(f'[SERVER COMMAND] {msg}')

                match(msg):
                    case consts.PLAY:
                        # SEND ACK RESPONSE
                        self.SOCKET.send(consts.ACK.encode())
                        
                        # RECEIVE TOPIC AND UPDATE GUI
                        msg = self.SOCKET.recv(MESSAGE_SIZE).decode()
                        print(f"[SERVER] Find a {msg}")
                        self.label.configure(text=msg)
                                            
                        # ACTIVATE GAME LOOP
                        self.START_ROUND = True
                        # self.start_round()
                    case _:
                        print('[ERROR] Unknown server message.')
                        raise Exception('[ERROR] Unknown server message.')
            else: 
                sleep(1)
        print('[WARNING] Server listening loop broken')


    def start_round(self, round_duration = 30):
        '''
            Open the webbrowser on a random wiki article for a specified round_duration.
            Disable keyboard typing to prevent cheating.
            Screenshot and Close at end of time.
            Update GUI with screenshot taken.
            
            Call send_image() to send screenshot image.
            Call get_score() also called to listen for score and update GUI.
            
            Reenable socket loop flag.
        '''
        while True:
            if self.START_ROUND:
                self.START_ROUND = False
                # DELAY TO SEE PROMPT
                sleep(1)

                print('[GAME] Round start')
                key_blocker = keyboard_Controls(suppress=True)
                key_blocker.start()

                # OPEN A RANDOM WIKI PAGE
                dr = webdriver.Chrome()
                dr.get("https://en.wikipedia.org/wiki/Special:Random")
                
                # Game Timer
                sleep(round_duration)

                # Screenshot result
                screenshot(SCREENSHOT_PATH)
                self.update_GUI_image()

                # Close web browser and restore keyboard controls.
                key_blocker.stop()
                dr.close()
                print('[GAME] Round end')

                # SEND SCREENSHOT IMAGE TO SERVER
                self.send_Image()

                # LISTEN FOR SERVER SCORING
                self.get_score()

                # REACTIVATE SOCKET LISTEN LOOP FOR NEXT PLAY PROTOCOL 
                self.LISTEN_CMD = True
            else:
                sleep(2)

    
    def send_Image(self):
        '''
            Send the screeenshot image.
            Append END protocol to mark end of image bytes/
        '''
        with open(SCREENSHOT_PATH, "rb") as file:
            data = file.read()

            # SEND IMAGE BYTES
            self.SOCKET.sendall(data)

            # SEND END PROTOCOL
            self.SOCKET.send(consts.END.encode())
            
            file.close()


    def get_score(self):
        '''
            Receive the players' scores and update the GUI.
        '''
        # LISTEN FOR SCORE
        print('[CLIENT] Waiting for score...')
        msg = self.SOCKET.recv(MESSAGE_SIZE).decode()
        print(f"[SERVER Msg] {msg}")

        # SEND ACK RESPONSE
        self.SOCKET.send(consts.ACK.encode())
        scores = self.SOCKET.recv(MESSAGE_SIZE)
        
        # DISPLAY SCORES ON CLIENT
        scores = json.loads(scores)
        print(scores)
        self.update_score_display(scores)
        


    def update_GUI_image(self):
        '''
            Update the GUI image with that of the screenshot.
        '''
        if os.path.isfile(PATHS['submission']):
            self.image_holder.destroy()
            self.image = customtkinter.CTkImage(light_image=Image.open(PATHS['submission']), dark_image=Image.open(PATHS['submission']), size=(250,250))
            self.image_holder = customtkinter.CTkLabel(self.root, text="", image=self.image)
            self.image_holder.pack()


# Client Instance
GameClient()