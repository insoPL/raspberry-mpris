class Line(object):
    DEAD_SPACES = 4
    def __init__(self, text, width):
        self.text = ""
        self.animated = False
        self.width = width
        self.i = 0
        self.set_text(text)

    def set_text(self, text):
        if len(text)>self.width:
            self.animated = True
            new_text = text+" "*self.DEAD_SPACES
        else:
            self.animated = False
            new_text = text
        if new_text == self.text:
            return
        self.i = 0
        self.text = new_text

    def __str__(self):
        if not self.animated:
            return self.text

        framebuffer = self.text[self.i:self.width+self.i]
        self.i+=1
        if self.i>len(self.text)-self.width:
            self.i=0
        return framebuffer