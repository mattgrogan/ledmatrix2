import time
from PIL import Image
import pygame, pygame.freetype

from util.timedelta import TimeDelta

class PygameText(object):

    def enter(self):
        pygame.freetype.init()
        self.font = pygame.freetype.Font("fonts/small_pixel.ttf", 8)
        self.camera = pygame.Rect(32, 32, 32, 32)
        self.timedelta = TimeDelta().reset()

        self.xspeed = 20
        self.yspeed = 0

    def step(self):

        render_needed = False

        # Does the camera need to move?
        delta = self.timedelta.delta()

        xdist = int(self.xspeed * delta)
        ydist = int(self.yspeed * delta)

        if xdist != 0 or ydist != 0:
            self.camera.move_ip(xdist, ydist)
            self.timedelta.reset()
            render_needed = True

        return render_needed
    
    def render(self):

        text, text_box = self.font.render("Hello World", pygame.Color("#FFFFFF"))

        # Drawing area with 32x32 margins
        w, h = text.get_size()
        w += 2 * 32
        h += 2 * 32
        s = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        s.set_alpha(0)

        # Add the text
        #s.fill(pygame.Color("#333333"))
        s.blit(text, (32, 32))

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
        im = Image.fromstring("RGBA", view.get_size(), img_str)

        return im

    