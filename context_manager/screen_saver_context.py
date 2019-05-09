class ScreenSaverContext:
    def __init__(self):
        self.foo = "foo"
        self.bar = "    bar"

    def get_lines(self):
        return self.foo, self.bar
