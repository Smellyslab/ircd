import socket
import sys
import os
import json
import time
import threading
import rsa
from base64 import b64encode, b64decode
import hashlib

class Irc():
    def __init__(self, name: str, host: None, port: int):
        if host == None:
            self.host = 'localhost'
        self.host = host
        self.port = port
        self.name = name
        self.clients = []
    
    def brodcast(self, message):
        for client in self.clients:
            client.send(message.encode('utf-8'))

    def recvclient(self, conn):

        while True:
            print(conn)
            message = conn.recv(1024)
            json_data = message.decode('utf-8')
            print(f'New message: {message.decode()}')
            if "message" not in json_data:
                print('Missing Message VAR')
                return 
            elif "signature" not in json_data:
                print("Missing SIG. VAR")
                return
            elif "public_key" not in json_data:
                print("Missing PUBLIC_KEY VAR")
                return 
            else:
                message = f'{hashlib.sha1(json_data["public_key"].decode("utf-8"))}: {json_data["message"]}'
                if rsa.verify(json_data["message"], b64decode(json_data["signature"]), json_data["public_key"]) == True:
                    self.brodcast(message.encode('utf-8'))
                else:
                    print("Wrong Verification.")


    def run(self):
        print(f'\033[01;32m[LOG]: STARTING SERVER ON {self.host}:{self.port}, IRC NAME: {self.name}\033[00m')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #rsa.verify(msg2, b64decode(signature), public)
        s.bind((self.host,self.port))
        s.listen()
        while True:
            conn, cli_addr = s.accept()
            #print(f'New Connection: {conn}')
            self.clients.append(conn)
            print(self.clients)
            thread = threading.Thread(target=self.recvclient, args=(conn,))
            thread.start()

                
                    

            


