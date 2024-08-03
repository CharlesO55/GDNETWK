from types import SimpleNamespace
consts = SimpleNamespace()
consts.SEND_SCREENSHOT = "<SEND SCREENSHOT>"
consts.PLAY = "<PLAY>"
consts.ACK = "<ACK>"
consts.END = "<END>"
consts.TERMINATE = "<TERMINATE>"

from time import sleep
from selenium import webdriver
from pyautogui import screenshot
from pynput.keyboard import Listener as keyboard_Controls

import socket

SCREENSHOT_PATH = 'Client/screenshot.jpg'
MESSAGE_SIZE = 4096


class GameClient:
    def __init__(self):
        SERVER = socket.gethostbyname(socket.gethostname())
        PORT = 8080

        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.connect((SERVER, PORT))
        print("[CLIENT] Connected to server.")

        self.loop()

    def __del__(self):
        self.SOCKET.send(consts.TERMINATE.encode())
        self.SOCKET.close()
        print("[CLIENT] Connection and Client closed")
        

    def loop(self):
        while True:
            print('Loop start')
            msg = self.SOCKET.recv(MESSAGE_SIZE).decode()

            print(msg)
            if msg == consts.PLAY:
                self.start_round()



    def start_round(self, round_duration = 5):
        print('[GAME] Round start')
        key_blocker = keyboard_Controls(suppress=True)
        key_blocker.start()

        # Open the page
        dr = webdriver.Chrome()
        dr.get("https://en.wikipedia.org/wiki/Special:Random")
        
        # Timer
        sleep(round_duration)

        # Screenshot result
        screenshot(SCREENSHOT_PATH)

        # Close
        key_blocker.stop()
        dr.close()
        print('[GAME] Round end')

        self.send_Image()

    def send_Image(self):
        with open(SCREENSHOT_PATH, "rb") as file:
            data = file.read()

            self.SOCKET.send(consts.SEND_SCREENSHOT.encode())
            print(f"[Server Response] {self.SOCKET.recv(MESSAGE_SIZE).decode()}")
            
            self.SOCKET.send(str(len(data)).encode())
            print(f"[Server Response] {self.SOCKET.recv(MESSAGE_SIZE).decode()}")

            self.SOCKET.sendall(data)

            print(f"[Client] Sending image data...")
            self.SOCKET.send(consts.END.encode())
            msg = self.SOCKET.recv(MESSAGE_SIZE).decode()
            print(f"[Server Response] {msg}")

            file.close()


newClient = GameClient()