from PIL import Image

from server.components.layers.gif_screen_layer import GifScreenLayer

ICON_WIDTH = 8
ICON_HEIGHT = 8

X_OFFSET = 3
Y_OFFSET = 3

X_MULT = 5
Y_MULT = 5

class GifIconLayer(object):
    """ Act as a proxy to reformat the GIF Icons to the proper size """

    def __init__(self, filename):
        self.gif_icon = GifScreenLayer(filename)

    def enter(self):
        self.gif_icon.enter()

    def exit(self):
        self.gif_icon.exit()

    def suspend(self):
        self.gif_icon.suspend()

    def resume(self):
        self.gif_icon.resume()

    def step(self):
        self.gif_icon.step()

    def render(self):

        icon = self.gif_icon.render()
        icon_pix = icon.load()

        im = Image.new("RGBA", (ICON_WIDTH, ICON_HEIGHT))
        pix = im.load()

        for col in range(ICON_WIDTH):
            x = col * X_MULT + X_OFFSET
            for row in range(ICON_HEIGHT):
                y = row * Y_MULT + Y_OFFSET

                # If it's grey, make it transparent
                r, g, b, a = icon_pix[x, y]
                if r < 50 and g < 50 and b < 50:
                    a = 0

                pix[col, row] = (r, g, b, a)

        return im



