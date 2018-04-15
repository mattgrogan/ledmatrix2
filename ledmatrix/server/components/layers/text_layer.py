from PIL import Image
import pygame

from server.components.layers.screen_layer import ScreenLayer
from util.font_factory import FontFactory

class TextLayer(ScreenLayer):

    def __init__(self, text, size="MEDIUM", color="#FFFFFF"):
        self.text = text
        self.size = size
        self.color = color

        pygame.freetype.init()
        self.font = FontFactory().by_size(self.size)

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

        text, text_box = self.font.render(self.text, pygame.Color(self.color))

        # Convert to PIL image for display
        img_str = pygame.image.tostring(text, "RGBA")
        im = Image.fromstring("RGBA", text.get_size(), img_str)

        return im