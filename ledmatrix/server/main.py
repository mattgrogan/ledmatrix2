from __future__ import division
from __future__ import absolute_import

import time
import PIL.Image as Image

from messaging.command_connection import CommandConnection
from messaging.image_connection import ImageConnection

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

    gif = GifState()
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