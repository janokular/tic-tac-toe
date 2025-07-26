#!/bin/env python3


import socket
from threading import Thread
import sys


class Client:
    def __init__(self, HOST, PORT):
        ''''''
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input('Enter your name: ')

        self.talk_to_server()


    def talk_to_server(self):
        ''''''
        self.socket.send(self.name.encode())
        Thread(target = self.received_message).start()
        self.send_message()


    def send_message(self):
        ''''''
        while True:
            player_input = input('')
            player_message = self.name + ": " + player_input
            self.socket.send(player_message.encode())


    def received_message(self):
        ''''''
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                sys.exit()

            print(server_message)


def main():
    client = Client('127.0.0.1', 8000)

if __name__ == '__main__':
    main()
