class Screen(object):

    def __init__(self):
        pass

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

    def handle_input(self):
        raise NotImplementedError