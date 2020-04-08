from gamegui import *
from math import pi
PI = pi
import pygame.gfxdraw

class Canvas(Control):
    def __init__(self, root, size, bg=(255, 255, 255), xscrollbar=False, yscrollbar=True):
        self.screen = pygame.Surface(size)
        self.screen.fill(bg)
        self.bg, self.xscrollbar, self.yscrollbar = bg, xscrollbar, yscrollbar
        self.w, self.h = size
        Control.__init__(self, root)
    def clear(self, fill=None):
        self.screen.fill(fill if fill else self.bg)
        Control.update(self)
    def pixel(self, pos, color=(0, 0, 0)):
        pygame.gfxdraw.pixel(self.screen, *pos, color)
        Control.update(self)
    def line(self, pos1, pos2, width=1, color=(0, 0, 0)):
        pygame.draw.line(self.screen, color, pos1, pos2, width)
        Control.update(self)
    def hline(self, y, x1=0, x2=None, color=(0, 0, 0)):
        pygame.gfxdraw.hline(self.screen, x1, x2 if x2 else self.w, y, color)
        Control.update(self)
    def vline(self, x, y1=0, y2=None, color=(0, 0, 0)):
        pygame.gfx.draw.vline(self.screen, x, y1, y2 if y2 else self.h, color)
        Control.update(self)
    def aaline(self, pos1, pos2, blend=True, color=(0, 0, 0)):
        pygame.draw.aaline(self.screen, color, pos1, pos2, blend)
        Control.update(self)
    def drawrect(self, rect, width=0, color=(0, 0, 0)):
        pygame.draw.rect(self.screen, color, rect, width)
        Control.update(self)
    def polygon(self, pointlist, width=0, color=(0, 0, 0)):
        pygame.draw.polygon(self.screen, color, pointlist, width)
        Control.update(self)
    def aapolygon(self, pointlist, fill=True, color=(0, 0, 0)):
        pygame.gfxdraw.aapolygon(self.screen, pointlist, color)
        if fill:
            pygame.gfxdraw.filled_polygon(self.screen, pointslist, color)
        Control.update(self)
    def circle(self, pos, raduis, width=0, color=(0, 0, 0)):
        pygame.draw.circle(self.screen, color, pos, raduis, width)
        Control.update(self)
    def aacirle(self, pos, raduis, fill=True, color=(0, 0, 0)):
        pygame.gfxdraw.aacicle(self.screen, *pos, raduis, color)
        if fill:
            pygame.gfxdraw.filled_circle(self.screen, *pos, raduis, color)
        Control.update(self)
    def ellipse(self, rect, width=0, color=(0, 0, 0)):
        pygame.draw.ellipse(self.screen, color, rect, width)
        Control.update(self)
    def aaellipse(self, rect, fill=True, color=(0, 0, 0)):
        rx, ry = rect.center[0]-rect.x, rect.center[1]-rect.y
        pygame.gfxdraw.aaellipse(self, *rect.center, rx, ry, color)
        if fill:
            pygame.gfxdraw.filled_ellipse(self, *rect.center, rx, ry, color)
        Control.update(self)
    def arc(self, rect, start, stop, color=(0, 0, 0)):
        pygame.draw.arc(self.screen, color, rect, start, stop)
        Control.update(self)
    def pie(self, pos, raduis, start, stop, color=(0, 0, 0)):
        pygame.gfxdraw.pie(self.screen, *pos, raduis, start, stop, color)
        Control.update(self)
    def image(self, image, rect):
        self.screen.blit(image, rect)
        Control.update(self)