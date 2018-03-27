"""
The ZMQ relay acts as an interface for any user interface to 
send commands to the server process.
"""

import zmq
import argparse

class ZmqRelay(object):

    def __init__(self, host="localhost", port=5555):

        self.addr = "tcp://%s:%s" % (host, port)

        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.PUSH)
        self.socket.connect(self.addr)

    def send(self, msg):
        """ Send a message to the ZMQ process """

        try:
            self.socket.connect(self.addr)
            self.socket.send(msg)
        except zmq.ZMQError:
            print "Unable to connect to %s" % self.addr

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
    
    parser = argparse.ArgumentParser(description="ZMQ Controller")
    parser.add_argument("-m", 
                        choices=["up", "down", "left", "right", "enter", "mode", "playpause"],
                        required=False)
    args = parser.parse_args()

    relay = ZmqRelay()

    if args.m == "up":
        relay.send_up()
    elif args.m == "down":
        relay.send_down()
    elif args.m == "right":
        relay.send_right()
    elif args.m == "left":
        relay.send_left()
    elif args.m == "enter":
        relay.send_enter()
    elif args.m == "mode":
        relay.send_mode()
    elif args.m == "playpause":
        relay.send_playpause()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass

    

