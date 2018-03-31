from __future__ import division
import time
import PIL.Image as Image

from messaging.image_connection import ImageConnection

c = ImageConnection()
c.connect("localhost", 5556, as_receiver=False)

im = Image.open("ufo.gif")

frame = 0

while True:

    

    # Get the frame duration
    try:
        dur = im.info["duration"] / 1000
    except KeyError:
        dur = 25 / 1000

    try:
        im.seek(frame)
    except EOFError:
        frame = 0
        im.seek(frame)

    im_copy = im.copy()
    im_copy = im_copy.convert("RGB")

    c.send(im_copy)

    time.sleep(dur)

    frame += 1