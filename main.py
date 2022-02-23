from irc.irc import Irc
import sys

port = sys.argv[1]


def main():
    newirc = Irc('SmellyIRC', '', int(port))
    newirc.run()

main()