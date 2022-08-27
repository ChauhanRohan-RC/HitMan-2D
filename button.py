import pygame


class Button:
    def __init__(self, x, y, width, height, color1, color2=None, text="", font=None, tcolor=None, outc=None, outw=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        self.text = text
        self.font =font
        self.tcolor = tcolor
        self.outc = outc
        self.outw = outw

    def draw(self, win):
        if self.outc:
            pygame.draw.rect(win, self.outc, (
            self.x - self.outw, self.y - self.outw, self.width + (self.outw * 2), self.height + (self.outw * 2)),
                             self.outw)
        pygame.draw.rect(win, self.color1, (self.x, self.y, self.width, self.height))
        if self.text != "":
            fon = pygame.font.SysFont(*self.font)
            text = fon.render(self.text, True, self.tcolor)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isover(self, *pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
