from PIL import Image
import pygame

from util.timedelta import TimeDelta

class PygameBox(object):

    def enter(self):
        self.camera = pygame.Rect(0, 0, 32, 32)

        self.xspeed = 0
        self.yspeed = 0

        self.timedelta = TimeDelta().reset()
        self.color = "#FF0000"

    def step(self):

        if self.timedelta.delta() >= 1:
            self.color = "#00FF00"
        if self.timedelta.delta() >= 4:
            self.color = "#0000FF"
            self.timedelta.reset()

        return True
    
    def render(self):

        s = pygame.Surface(self.camera.size, pygame.SRCALPHA, 32)
        s.set_alpha(0)

        # Add a box
        s.fill(pygame.Color(self.color), rect=pygame.Rect(20, 20, 25, 25))

        # Use the camera to extract a view
        view = s.subsurface(self.camera)

        # Convert to PIL image for display
        img_str = pygame.image.tostring(view, "RGBA")
        im = Image.fromstring("RGBA", view.get_size(), img_str)

        return im

    