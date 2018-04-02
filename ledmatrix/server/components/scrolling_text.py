from PIL import Image
import pygame

from server.screen_layer import ScreenLayer
from util.timedelta import TimeDelta
from util.font_factory import FontFactory

MATRIX_WIDTH = 32
MATRIX_HEIGHT = 32

class ScrollingText(ScreenLayer):

    def enter(self):
        pygame.freetype.init()

        self.font = FontFactory().by_size("SMALL")
        self.camera = pygame.Rect(MATRIX_WIDTH, MATRIX_HEIGHT, MATRIX_WIDTH, MATRIX_HEIGHT)
        self.timedelta = TimeDelta().reset()

        self.xspeed = 32
        self.yspeed = 0

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):

        delta = self.timedelta.delta()

        xdist = int(self.xspeed * delta)
        ydist = int(self.yspeed * delta)

        if xdist != 0 or ydist != 0:
            self.camera.move_ip(xdist, ydist)
            self.timedelta.reset()

    def render(self):

        text, text_box = self.font.render("Hello World", pygame.Color("#FFFFFF"))

        # Add margins to drawing area
        w, h = text.get_size()
        w += 2 * MATRIX_WIDTH
        h += 2 * MATRIX_HEIGHT
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.set_alpha(0)

        # Add the text to the surface
        s.blit(text, (MATRIX_WIDTH, MATRIX_HEIGHT))

        # Check for overflow
        bounds = s.get_rect()

        if self.camera.right >= bounds.right:
            self.camera.left = 0
        if self.camera.left < 0:
            self.camera.right = bounds.right
        if self.camera.bottom >= bounds.bottom:
            self.camera.top = 0
        if self.camera.top < 0:
            self.camera.bottom = bounds.bottom

        # Use the camera to extract a view
        view = s.subsurface(self.camera)

        # Convert to PIL image for display
        img_str = pygame.image.tostring(view, "RGBA")
        self.im = Image.fromstring("RGBA", view.get_size(), img_str)

        return self.im