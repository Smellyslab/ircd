import socket
import sys
import signal
import threading
import rsa 
import rsa
from base64 import b64encode, b64decode
import json




class Client():
    def __init__(self, rhost, rport):
        self.keysize = 1024
        (self.public, self.private) = rsa.newkeys(self.keysize)
        self.rhost = rhost
        self.rport = int(rport)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def receive():
        
        while True:
            try:
                data = self.s.recv(1024)
                print(data.decode("utf-8"))
            except:
                print('An error ocurred!')
                s.close()
                break

    def run(self):
        try:
            self.s.connect((self.rhost, self.rport))
        except Exception as e:
            print(e)
        thread = threading.Thread(target=self.receive)
        try:
            while True:
                inp = input('>>')
                if inp:
                    try:
                        message = {"message": inp, "public_key": str(self.public).encode(), "signature": b64encode(rsa.sign(inp.encode('utf-8'), self.private, "SHA-512"))}
                        self.s.send(bytes(str(message), 'utf-8'))
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        