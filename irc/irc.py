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
            json_data = message.decode()
            #print(json_data)
            json_data = json.dumps(json_data)
            print(type(json_data))
            #print(f'New message: {json_data}')
            #print(f'\033[01;36m{json_data["message"]}\033[00m')
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
                message = f'{hashlib.sha1(json_data["public_key"].encode("utf-8"))}: {json_data["message"]}'
                if rsa.verify(json_data["message"], b64decode(json_data["signature"]), json_data["public_key"]) == True:
                    self.brodcast(message.encode('utf-8'))
                else:
                    print("Wrong Verification.")


    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #rsa.verify(msg2, b64decode(signature), public)
        s.bind((self.host,self.port))
        s.listen()
        print(f'\033[01;32m[LOG]: STARTING SERVER ON {self.host}:{self.port}, IRC NAME: {self.name}\033[00m')
        #conn = s.accept()
        while True:
            conn = s.accept()[0]
            print(f'New Connection: {conn}')
            self.clients.append(conn)
            print(self.clients)
            thread = threading.Thread(target=self.recvclient, args=(conn,))
            thread.start()

                
                    

            


