from __future__ import absolute_import

import StringIO
import time
from flask import Flask, send_file

from messaging.image_connection import ImageConnection

IMG_HOST = "localhost"
IMG_PORT = 5556

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32
IMG_ZOOM = 16

app = Flask(__name__)

def serve_pil_image(pil_img):
    # https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/')
def display_img():

    image_conn = ImageConnection()
    image_conn.connect(IMG_HOST, IMG_PORT, as_receiver=True)

    im = image_conn.receive()

    while im is None:
        im = image_conn.receive()
        print "."
        time.sleep(0.25)

    # Resize
    w = MATRIX_WIDTH * IMG_ZOOM
    h = MATRIX_HEIGHT * IMG_ZOOM
    im = im.resize((w, h))    
    
    if im is not None:
        return serve_pil_image(im)
    else:
        return 'No image found'