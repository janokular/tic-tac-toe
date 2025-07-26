#!/bin/env python3


import socket
from threading import Thread


class Server:
    Players = []

    def __init__(self, HOST, PORT):
        '''Create a TCP socket over IPv4. Accept 2 players'''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(2)
        print(f'Server is listening for players on port {PORT}')


    def listen(self):
        ''''''
        while True:
            player_socket, address = self.socket.accept()
            print('Connection from: ' + str(address))

            player_name = player_socket.recv(1024).decode()
            player = {'player_name': player_name, 'player_socket': player_socket}

            self.broadcast_message(player_name, player_name + ' has joined the game!')
            Server.Players.append(player)
            Thread(target = self.handle_new_player, args = (player,)).start()


    def handle_new_player(self, player):
        ''''''
        player_name = player['player_name']
        player_socket = player['player_socket']
        while True:
            player_message = player_socket.recv(1024).decode()

            if player_message.strip() == player_name + ': exit' or not player_message.strip():
                self.broadcast_message(player_name, player_name + ' has left the game!')
                Server.Players.remove(player)
                player_socket.close()
                break
            else:
                self.broadcast_message(player_name, player_message)


    def broadcast_message(self, sender_name, message):
        ''''''
        for player in self.Players:
            player_socket = player['player_socket']
            player_name = player['player_name']
            if player_name != sender_name:
                player_socket.send(message.encode())


def main():
    server = Server('127.0.0.1', 8000)
    server.listen()

if __name__ == '__main__':
    main()