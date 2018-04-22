class Screen(object):

    def init(self):
        self.is_popup = False

    def enter(self):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError

    def suspend(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def handle_input(self, cmd):
        raise NotImplementedError