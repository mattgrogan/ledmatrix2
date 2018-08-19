from PIL import Image
import pygame, pygame.font

from util.font_factory import FontFactory
from server.components.layers.screen_layer import ScreenLayer

class TextLayer(ScreenLayer):

    def __init__(self, text, size="MEDIUM", color="#FFFFFF"):
        self.text = text
        self.size = size
        self.color = color

        pygame.font.init()

        self.font = FontFactory().by_size(size)

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

        text = self.font.render(self.text, False, pygame.Color(self.color))

        # Convert to PIL image for display
        img_str = pygame.image.tostring(text, "RGBA")
        im = Image.frombytes("RGBA", text.get_size(), img_str)

        return im