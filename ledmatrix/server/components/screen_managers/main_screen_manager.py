import collections
from PIL import Image

from server.components.screen_managers.screen_manager import ScreenManager

from server.components.screens.gif_screen_factory import GifScreenFactory
from server.components.screens.info_screen import InfoScreen
from server.components.screens.clock_screen import ClockScreen

class MainScreenManager(ScreenManager):

    def __init__(self, device):

        self.device = device
        self.screens = collections.deque()

        #self.add_screen(InfoScreen(device=device))
        self.add_screen(ClockScreen(device=device))
        #self.add_screen(GifScreenFactory().from_folder("icons/gifs/"))

    def add_screen(self, screen):
        self.screens.append(screen)

    @property
    def current_screen(self):
        return self.screens[0]

    def enter(self):
        for screen in self.screens:
            screen.enter()

    def next(self):

        # Pop the top item
        screen = self.screens.popleft()

        # Append it to the end
        self.screens.append(screen)

    def handle_input(self, cmd):
        if cmd == "KEY_MODE":
            self.next()
        elif cmd is not None:
            for screen in self.screens:
                screen.handle_input(cmd)

    def step(self):
        """ Allow each screen to run logic """

        for screen in self.screens:
            screen.step()

    def render(self):

        # Create new background and paste other images on top
        bg = Image.new("RGBA", self.device.size)

        for screen in reversed(self.screens):
            if not screen.is_popup:
                # If this isn't a popup, it will cover all previous screens
                bg = Image.new("RGBA", self.device.size)
            
            # Paste the screen on the background
            im = screen.render()
            bg.paste(im, mask=im)

        return bg