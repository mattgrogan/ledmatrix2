class ScreenManager(object):

    def __init__(self):
        pass

    def enter(self):
        raise NotImplementedError

    def handle_input(self, cmd):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError