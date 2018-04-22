import pygame, pygame.font

class FontFactory(object):

    def from_file(self, filename, size):

        font = pygame.font.Font(filename, size)

        return font

    def by_size(self, size):

        if size == "SMALL":
            font = self.from_file("fonts/visitor1.ttf", 10)

        elif size == "MEDIUM":
            font = self.from_file("fonts/small_pixel.ttf", 8)

        elif size == "HUGE":
            font = self.from_file("fonts/m12.ttf", 32)

        else:
            font = None

        return font



