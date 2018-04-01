"""
The CommandConnection allows clients to send commands between processes.
"""
from __future__ import absolute_import

import zmq

HOST = "localhost"
PORT = 5555

TIMEOUT = 1

class CommandConnection(object):

    def connect(self, host, port, as_receiver=False):
        """ Open a connection to pass commands.
        host: the hostname to connect to. If this is a receiver, use "*"
        port: port number to connect to
        as_receiver: True if receiving messages, False if sending messages
        """

        self.as_receiver = as_receiver
        self.addr = "tcp://%s:%s" % (host, port)

        self.context = zmq.Context()

        if as_receiver:
            self.socket = self.context.socket(zmq.PULL)
            self.socket.bind(self.addr)
        else:
            self.socket = self.context.socket(zmq.PUSH)
            self.socket.connect(self.addr)

    def receive(self):
        """ Receive a command from the server """

        assert self.as_receiver

        cmd = None

        events = self.socket.poll(timeout=TIMEOUT)

        if events:
            cmd = self.socket.recv()

        return cmd


    def send(self, cmd):
        """ Send a command to the server """

        assert not self.as_receiver

        try:
            self.socket.send(cmd)
        except zmq.ZMQError:
            print "Unable to send message on %s" % self.addr

    def send_enter(self):
        self.send("KEY_ENTER")

    def send_mode(self):
        self.send("KEY_MODE")

    def send_up(self):
        self.send("KEY_UP")

    def send_down(self):
        self.send("KEY_DOWN")

    def send_left(self):
        self.send("KEY_LEFT")

    def send_right(self):
        self.send("KEY_RIGHT")

    def send_playpause(self):
        self.send("KEY_PLAYPAUSE")

def main():

    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="CommandConnection")
    parser.add_argument("-s", 
                        choices=["up", "down", "left", "right", "enter", "mode", "playpause"],
                        help="Send a command")
    parser.add_argument("-r", action="store_true", help="Receive commands and print them to the screen")
    args = parser.parse_args()

    conn = CommandConnection()

    if args.r:
        conn.connect("*", PORT, as_receiver = True)

        while True:
            cmd = conn.receive()

            if cmd is not None:
                print cmd

            time.sleep(1)

    else:

        conn.connect(HOST, PORT, as_receiver=False)

        if args.s == "up":
            conn.send_up()
        elif args.s == "down":
            conn.send_down()
        elif args.s == "right":
            conn.send_right()
        elif args.s == "left":
            conn.send_left()
        elif args.s == "enter":
            conn.send_enter()
        elif args.s == "mode":
            conn.send_mode()
        elif args.s == "playpause":
            conn.send_playpause()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass

    

