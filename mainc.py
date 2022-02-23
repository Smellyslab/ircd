from irc.client import Client
import sys

port = sys.argv[1]

def main():
    newclient = Client('127.0.0.1', int(port))
    newclient.run()

main()
