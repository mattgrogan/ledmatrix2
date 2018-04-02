from PIL import Image
import pygame

class PygameBox(object):

    def enter(self):
        self.camera = pygame.Rect(0, 0, 32, 32)

        self.xspeed = 0
        self.yspeed = 0

        self.has_rendered = False

    def step(self):

        if self.has_rendered:
            render_needed = False
        else:
            self.has_rendered = True
            render_needed = False

        return True
    
    def render(self):

        s = pygame.Surface(self.camera.size, pygame.SRCALPHA, 32)
        s.set_alpha(128)

        # Add a box
        s.fill(pygame.Color("#FF0000"), rect=pygame.Rect(20, 20, 25, 25))

        # Use the camera to extract a view
        view = s.subsurface(self.camera)

        # Convert to PIL image for display
        img_str = pygame.image.tostring(view, "RGBA")
        im = Image.fromstring("RGBA", view.get_size(), img_str)

        return im

    