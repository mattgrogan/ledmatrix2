import time
from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

class ClockScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        icon_file = "icons/gif_icons/13533_icon_thumb.gif"
        self.icon = GifScreenFactory().from_icon(icon_file)

    def enter(self):
        self.icon.enter()

    def exit(self):
        pass

    def suspend(self):
        self.icon.suspend()

    def resume(self):
        self.icon.resume()

    def step(self):
        self.icon.step()

    def _time(self):
        # Return the formatted time
        return time.strftime("%I:%M", time.localtime()).lstrip("0")

    def render(self):

        # Create a blank background
        bg = Image.new("RGBA", self.device.size)

        # Render the text
        txt = TextLayer(self._time())
        im = txt.render()

        # Calculate position of text
        x = self.device.size[0] - im.size[0]
        y = 0

        # Paste the text on the background
        bg.paste(im, box=(x, y), mask=im)

        # Render the icon
        icon_im = self.icon.render()
        bg.paste(icon_im, box=(0,0), mask=icon_im)

        return bg

    def handle_input(self, cmd):
        pass
    
