from PIL import Image

from server.screen import Screen
from server.components.scrolling_text import ScrollingText
from server.components.gif import GifScreenFactory

SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

class InfoScreen(Screen):

    def __init__(self):

        self.layers = []
        self.positions = []

        txt = ScrollingText("Welcome to my world!", xspeed=20)

        self.add_layer(txt, (9, 2))

        icon_file = "icons/gif_icons/1624_icon_thumb.gif"
        icon = GifScreenFactory().from_icon(icon_file)


        self.add_layer(icon, (0, 0))

        #self.add_layer(ScrollingText(), (10, 20))

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
        bg = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT))
        for i, layer in enumerate(self.layers):
            im = layer.render()
            bg.paste(im, box=self.positions[i], mask=im)

        return bg


    def handle_input(self, cmd):
        pass