from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.layers.scrolling_layer import ScrollingLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

class InfoScreen(Screen):

    def __init__(self, device):

        self.init()
        self.is_popup = False

        self.device = device
        self.is_paused = False

        self.layers = []
        self.positions = []

        txt = TextLayer("Welcome to my world again")
        scrolling_txt = ScrollingLayer(self.device, txt, xspeed=10)

        self.add_layer(scrolling_txt, (0, 10))

        icon_file = "icons/gif_icons/1624_icon_thumb.gif"
        icon = GifScreenFactory().from_icon(icon_file)

        self.add_layer(icon, (0, 0))

    def add_layer(self, layer, pos):
        self.layers.append(layer)
        self.positions.append(pos)

    def enter(self):
        for layer in self.layers:
            layer.enter()

    def exit(self):
        pass
        
    def suspend(self):
        for layer in self.layers:
            layer.suspend()

    def resume(self):
        for layer in self.layers:
            layer.resume()

    def step(self):
        for layer in self.layers:
            layer.step()

    def render(self):
        bg = Image.new("RGBA", self.device.size)
        for i, layer in enumerate(self.layers):
            im = layer.render()
            bg.paste(im, box=self.positions[i], mask=im)

        return bg


    def handle_input(self, cmd):
        if cmd == "KEY_PLAYPAUSE":
            self.is_paused = not self.is_paused

            if self.is_paused:
                self.suspend()
            else:
                self.resume()