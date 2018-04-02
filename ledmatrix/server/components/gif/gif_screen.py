from server.screen import Screen
from server.components.gif_screen_layer import GifScreenLayer

class GifScreen(Screen):

    def __init__(self):
        self.gifs = [GifScreenLayer("ufo.gif")]
        self.current_item = 0
        self.is_paused = False

    def enter(self):
        self.gifs[self.current_item].enter()

    def exit(self):
        self.gifs[self.current_item].exit()

    def step(self):
        self.gifs[self.current_item].step()

    def render(self):
        return self.gifs[self.current_item].render()

    def handle_input(self, cmd):

        if cmd == "KEY_PLAYPAUSE":
            self.is_paused = not self.is_paused
            
            if self.is_paused:
                self.gifs[self.current_item].suspend()
            else:
                self.gifs[self.current_item].resume()




