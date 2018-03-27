"""
The ZMQ relay acts as an interface for any user interface to 
send commands to the server process.
"""

import zmq

class ZmqRelay(object):

    def __init__(self, host="localhost", port=5555):

        self.addr = "tcp://%s:%s" % (host, port)

        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.PUSH)
        self.socket.connect(self.addr)

    def send(self, msg):
        """ Send a message to the ZMQ process """

        try:
            print "Connecting"
            self.socket.connect(self.addr)
            print "sending"
            self.socket.send(msg)
            print "sent"
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


    

