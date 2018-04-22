import time
from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer

class ClockScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = True
        self.device = device

    def enter(self):
        pass

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        pass

    def render(self):
        bg = Image.new("RGBA", self.device.size)

        txt = TextLayer(time.strftime(
            "%I:%M", time.localtime()).lstrip("0"))
        im = txt.render()
        bg.paste(im, box=(0,0), mask=im)
        return bg

    def handle_input(self):
        pass
    
