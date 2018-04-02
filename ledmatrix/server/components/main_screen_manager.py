from server.screen_manager import ScreenManager

from server.components.gif import GifScreenFactory

class MainScreenManager(ScreenManager):

    def __init__(self):

        gif_screen = GifScreenFactory().from_folder("./icons/gifs/")

        self.screens = [gif_screen]
        self.current_item = 0

    def enter(self):
        self.current_item = 0
        self.screens[self.current_item].enter()

    def next(self):

        self.screens[self.current_item].exit()

        self.current_item += 1
        if self.current_item >= len(self.screens):
            self.current_item = 0

        self.screens[self.current_item].enter()

    def handle_input(self, cmd):
        if cmd == "KEY_MODE":
            self.next()
        else:
            self.screens[self.current_item].handle_input(cmd)

    def step(self):
        self.screens[self.current_item].step()

    def render(self):
        return self.screens[self.current_item].render()