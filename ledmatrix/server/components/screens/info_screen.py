from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer
from server.components.screens.gif_screen_factory import GifScreenFactory

class InfoScreen(Screen):

    def __init__(self, device):

        self.device = device

        self.layers = []
        self.positions = []

        txt = TextLayer("Welcome to my world again")

        self.add_layer(txt, (0, 10))

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
        pass

    def resume(self):
        pass

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
        pass