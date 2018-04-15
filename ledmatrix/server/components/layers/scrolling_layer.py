from PIL import Image
import pygame

from server.components.layers.screen_layer import ScreenLayer
from util.timedelta import TimeDelta

class ScrollingLayer(ScreenLayer):

    def __init__(self, device, layer, xspeed=0, yspeed=0):
        self.device = device
        self.layer = layer
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.is_paused = False

    def enter(self):
        w, h = self.device.size

        # Initialize the camera at w, h because
        # we will add margins to all sides
        self.camera = pygame.Rect(w, h, w, h)
        self.timedelta = TimeDelta().reset()

    def exit(self):
        self.layer.exit()

    def suspend(self):
        self.layer.suspend()
        self.is_paused = True

    def resume(self):
        self.layer.resume()
        self.timedelta.reset()
        self.is_paused = False

    def step(self):

        if self.is_paused:
            return

        # Update the layer
        self.layer.step()

        # Move the camera
        delta = self.timedelta.delta()

        xdist = int(self.xspeed * delta)
        ydist = int(self.yspeed * delta)

        if xdist != 0 or ydist != 0:
            self.camera.move_ip(xdist, ydist)
            self.timedelta.reset()        

    def render(self):
        im = self.layer.render()

        # Convert from PIL to pygame surface
        img_str = im.tostring()
        im = pygame.image.fromstring(img_str, im.size, "RGBA")
        
        # Create drawing area surrounded by margins on all sides
        w, h = im.get_size()
        dev_width, dev_height = self.device.size
        w += 2 * dev_width
        h += 2 * dev_height
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.set_alpha(0)

        # Add the layer to the surface
        s.blit(im, (dev_width, dev_height))

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

