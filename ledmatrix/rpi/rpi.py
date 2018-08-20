from __future__ import absolute_import

import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from messaging.command_connection import CommandConnection
from messaging.image_connection import ImageConnection

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32

CMD_HOST = "localhost"
CMD_PORT = 5555

IMG_HOST = "localhost"
IMG_PORT = 5556

TICK_MS = 10.0

class Rpi(object):

    def __init__(self):
        
        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = MATRIX_HEIGHT
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat' 

        self.matrix = RGBMatrix(options = options)

        # Connect to receive images
        self.image_conn = ImageConnection()
        self.image_conn.connect(IMG_HOST, IMG_PORT, as_receiver=True)

    def mainloop(self):

        while True:
            im = self.image_conn.receive()
            if im is not None:
                self.display(im)
                time.sleep(TICK_MS)

    def display(self, im):
        
        self.matrix.SetImage(im)
            

            
        


