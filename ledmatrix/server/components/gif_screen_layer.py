from __future__ import division

from PIL import Image

from server.screen_layer import ScreenLayer
from util.timedelta import TimeDelta

DEFAULT_DURATION = 25.0 # milliseconds

class GifScreenLayer(object):

    def __init__(self, filename):
        self.filename = filename
        self.im = Image.open(filename)
        self.is_playing = False

    def _get_duration(self):
        """ Return the requested duration (in milliseconds) encoded 
            in the gif file."""
        try:
            dur = self.im.info["duration"] / 1000.0
        except KeyError:
            dur = DEFAULT_DURATION / 1000.0 

        return dur

    def _load_frame(self, i):
        """ Load the indicated frame. 
            If found return True, otherwise False """

        eof = False 
        try:
            self.im.seek(i)
        except EOFError:
            eof = True

        return eof       

    def enter(self):
        """ Reset the animation to the beginning """

        self.frame = 0
        self.timedelta = TimeDelta().reset()

        self._load_frame(self.frame)
        self.dur = self._get_duration()

        self.is_playing = True

    def exit(self):
        self.is_playing = False

    def suspend(self):
        self.is_playing = False

    def resume(self):
        self.is_playing = True

    def step(self):

        if not self.is_playing:
            return

        if self.timedelta.test(self.dur):

            self.frame += 1

            eof = self._load_frame(self.frame)

            if eof:
                self.frame = 0
                self._load_frame(self.frame)

            self.dur = self._get_duration()

            self.timedelta.reset()

    def render(self):

        im_copy = self.im.copy()
        im_copy = im_copy.convert("RGBA")

        return im_copy




