from server.screen import Screen

class GifScreen(Screen):

    def __init__(self, layers):
        self.items = layers
        self.current_item = 0
        self.is_paused = False

    def next(self):
        self.items[self.current_item].exit()

        self.current_item += 1

        if self.current_item >= len(self.items):
            self.current_item = 0

        self.items[self.current_item].enter()

    def prev(self):
        self.items[self.current_item].exit()

        self.current_item -= 1

        if self.current_item < 0:
            self.current_item = len(self.items) - 1

        self.items[self.current_item].enter()

    def enter(self):
        self.current_item = 0
        self.items[self.current_item].enter()

    def exit(self):
        self.items[self.current_item].exit()

    def step(self):
        self.items[self.current_item].step()

    def render(self):
        return self.items[self.current_item].render()

    def handle_input(self, cmd):

        if cmd == "KEY_PLAYPAUSE":
            self.is_paused = not self.is_paused
            
            if self.is_paused:
                self.items[self.current_item].suspend()
            else:
                self.items[self.current_item].resume()

        if cmd == "KEY_RIGHT":
            self.next()

        if cmd == "KEY_LEFT":
            self.prev()




