from __future__ import absolute_import

import StringIO
import time
import zmq
from flask import Flask, send_file, request, render_template

from messaging.image_connection import ImageConnection
from messaging.command_connection import CommandConnection

IMG_HOST = "localhost"
IMG_PORT = 5556

CMD_HOST = "localhost"
CMD_PORT = 5555

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32
IMG_ZOOM = 16

app = Flask(__name__)

image_conn = ImageConnection()
image_conn.connect(IMG_HOST, IMG_PORT, as_receiver=True)


cmd_conn = CommandConnection()
cmd_conn.connect(CMD_HOST, CMD_PORT, as_receiver=False)

def serve_pil_image(pil_img):
    # https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', cache_timeout=0)

@app.route("/")
def display_index():
    return render_template("index.html")


@app.route('/api/v1/current_image.png')
def display_img():

    try:
        im = image_conn.receive()
    except zmq.ZMQError:
        print "COULD NOT FIND IMAGE"
        return ""

    # while im is None:
    #      im = image_conn.receive()
    #      print "."
    #      time.sleep(0.25)

    # Resize
    w = MATRIX_WIDTH * IMG_ZOOM
    h = MATRIX_HEIGHT * IMG_ZOOM
    im = im.resize((w, h))    
    
    if im is not None:
        return serve_pil_image(im)
    else:
        return 'No image found'

@app.route('/api/v1/command', methods=["GET", "POST"])
def command():
    if request.method == "POST":

        cmd = request.headers["CMD"]

        print "COMMAND IS: %s" % cmd

        if cmd == "KEY_MODE":
            cmd_conn.send_mode()
        elif cmd == "KEY_ENTER":
            cmd_conn.send_enter()
        elif cmd == "KEY_UP":
            cmd_conn.send_up()
        elif cmd == "KEY_DOWN":
            cmd_conn.send_down()
        elif cmd == "KEY_LEFT":
            cmd_conn.send_left
        elif cmd == "KEY_RIGHT":
            cmd_conn.send_right()
        elif cmd == "KEY_PLAYPAUSE":
            cmd_conn.send_playpause()
        else:
            return "Bad Input"

        return cmd
    else:
        return "please post"
