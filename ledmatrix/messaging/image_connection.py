"""
The ImageConnection allows clients to send images between processes.
"""
from __future__ import absolute_import

import zmq
from PIL import Image

#import time

HOST = "localhost"
PORT = 5556

IMAGE_MODE = "RGB"
IMAGE_SIZE = (32, 32)

TIMEOUT = 1

class ImageConnection(object):

    def connect(self, host, port, as_receiver=False):
        """ Open a connection to pass images.
        host: the hostname to connect to. If this is a receiver, use "*"
        port: the port number to connect to
        as_receiver: True if receiving images, False if sending images
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

    def receive(self, mode=IMAGE_MODE, size=IMAGE_SIZE, timeout=TIMEOUT):
        """ Receive an image if one has been received, otherwise return None """

        assert self.as_receiver

        im = None

        while self.socket.poll(timeout=timeout):
            # Loop until the last image is received
            image = self.socket.recv()
            im = Image.fromstring(mode, size, image)

        return im

    def send(self, im):
        """ Send an image to a receiver """

        assert not self.as_receiver

        assert im.mode == IMAGE_MODE
        assert im.size == IMAGE_SIZE

        try:
            self.socket.send(im.tostring())
        except zmq.ZMQError:
            print "Unable to send image on %s" % self.addr

def main():

    import argparse
    import time

    parser = argparse.ArgumentParser(description="ImageConnection")
    parser.add_argument("-s", action="store", help="Send an image")
    parser.add_argument("-r", action="store_true", help="Receive an image")
    args = parser.parse_args()
    
    conn = ImageConnection()

    if args.r:
        conn.connect("*", PORT, as_receiver=True)

        print "Connected. Ready to receive image..."

        while True:
            im = conn.receive()

            if im is not None:
                im.show()

            time.sleep(1)

    elif args.s is not None:
        conn.connect(HOST, PORT, as_receiver=False)
        im = Image.open(args.s)
        im = im.convert(IMAGE_MODE)
        im.resize(IMAGE_SIZE)
        conn.send(im)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass