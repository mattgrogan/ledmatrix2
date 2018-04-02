class ScreenManager(object):

    def __init__(self):
        pass

    def handle_input(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

class MainScreenManager(ScreenManager):

    def __init__(self):
        pass
