from __future__ import division
from __future__ import absolute_import

import time
import copy
from PIL import Image, ImageFont, ImageDraw

from messaging.command_connection import CommandConnection
from messaging.image_connection import ImageConnection

from server.pygame_text import PygameText

FPS = 60

CMD_HOST = "*"
CMD_PORT = 5555

IMG_HOST = "*"
IMG_PORT = 5556

SECS_PER_FRAME = 1.0 / FPS

def main():
    
    done = False

    # Set up the command connection
    cmd_connection = CommandConnection()
    cmd_connection.connect(CMD_HOST, CMD_PORT, as_receiver=True)

    # Set up the image connection
    img_connection = ImageConnection()
    img_connection.connect(IMG_HOST, IMG_PORT, as_receiver=False)

    gif = PygameText()
    gif.enter()

    while(not done):

        # Save time
        start_time = time.time()

        # Check for input
        cmd = cmd_connection.receive()

        # Update state
        render = gif.step()

        # Render
        if cmd is not None:
            print cmd

        if render:
            img_connection.send(gif.render()) 

        # Elapse time
        sleep_time = max(start_time + SECS_PER_FRAME - time.time(), 0)
        time.sleep(sleep_time)

class Vector(object):

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Vector(%.2f, %.2f)" % (self.x, self.y)

class Animation(object):

    def enter(self):

        self.last_update = time.time()
        self.pos = Vector(0, 0)
        self.velocity = Vector(-10, 0)


    def step(self):

        self.last_pos = copy.copy(self.pos)
        
        delta = time.time() - self.last_update

        self.pos += self.velocity * delta

        self.last_update = time.time()

        return int(self.pos.x) != int(self.last_pos.x) or int(self.pos.y) != int(self.last_pos.y)

    def render(self):

        text = "HELLO WORLD"
        self.font = ImageFont.truetype("fonts/small_pixel.ttf", 8)

        w, h = self.font.getsize(text)

        self.im = Image.new("RGB", (w*2, h*2))
        self.draw = ImageDraw.Draw(self.im)

        pos = (int(self.pos.x), int(self.pos.y))
        print pos

        self.draw.text(pos, 
                "HELLO WORLD", 
                font=self.font,
                fill="#FFFFFF")

        #print "Drawing at %s" % self.pos

        return self.im.crop(box=(0, 0, 32, 32))

class GifState(object):

    def __init__(self):
        self.im = None
        self.frame = None
        self.last_step = None
        self.dur = None

    def enter(self):
        self.frame = 0
        self.im = Image.open("ufo.gif")

        self.last_step = time.time()
        self.dur = 0

        self.step()

    def exit(self):
        self.frame = None
        self.im = None
        self.last_step = None
        self.dur = None

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        """ Advance the frame if duration has passed. Return True if 
            rendering is required.
        """

        is_updated = False

        if time.time() >= self.last_step + self.dur:
            
            # Advance frame
            try:
                self.dur = self.im.info["duration"] / 1000.0
            except KeyError:
                self.dur = 25 / 1000.0

            try:
                self.im.seek(self.frame)
                self.frame += 1
            except EOFError:
                self.frame = 0
                self.im.seek(self.frame)

            self.last_step = time.time()

            is_updated = True

        return is_updated

    def render(self):

        im_copy = self.im.copy()
        im_copy = im_copy.convert("RGB")

        return im_copy


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass