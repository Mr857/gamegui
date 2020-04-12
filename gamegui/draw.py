from gamegui import *
from math import pi
PI = pi
import pygame.gfxdraw

SUNK = 0
RAISED = 1
SMOOTH = 2
class Canvas(Control):
    def __init__(self, root, size, bg=(255, 255, 255), style=0, xscrollbar=False, yscrollbar=True):
        self.screen = pygame.Surface(size)
        self.screen.fill(bg)
        self.size, self.style, self.bg, self.xscrollbar, self.yscrollbar = size, style, bg, xscrollbar, yscrollbar
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
            pygame.gfxdraw.filled_polygon(self.screen, pointlist, color)
        Control.update(self)
    def circle(self, pos, raduis, width=0, color=(0, 0, 0)):
        pygame.draw.circle(self.screen, color, pos, raduis, width)
        Control.update(self)
    def aacircle(self, pos, raduis, fill=True, color=(0, 0, 0)):
        pygame.gfxdraw.aacircle(self.screen, *pos, raduis, color)
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
        self.screen.blit(image.surface(), rect)
        Control.update(self)
    def aalock(self):
        self.line = self.aaline
        self.polygon = self.aapolygon
        self.circle = self.aacircle
        self.ellipse = self.aaellipse
    def place(self, topleft):
        self.rect = pygame.Rect(topleft, self.size)
        ALL.append(self)
        self.update()

class Image(Control):
    def __init__(self, root, path, alpha=255):
        if not isinstance(path, str):
            if isinstance(path, draw.Canvas):
                self.image = path.screen
            else:
                raise ValueError
        else:
            self.image = pygame.image.load(path)
        self.image.set_alpha(alpha)
        self.style = ''
        Control.__init__(self, root)
    def __len__(self):
        return self.iamge.get_size()
    def __getitem__(self, index):
        return tuple(self.image.get_at(index))
    def __setitem__(self, key, value):
        self.image.set_at(key, value)
    def surface(self):
        return self.image
    def set_style(self, style=''):
        self.style = style
    def get_style(self):
        return self.style

def maindraw(window, widgets):
    screen = window.screen
    window.clear()
    for widget in widgets:
        wrect = widget.rect
        if isinstance(widget, Image):
            screen.blit(widget.surface(), wrect)
        elif isinstance(widget, Canvas):
            screen.blit(widget.screen, wrect)
            if widget.style == 0:
                window.aaline((wrect.x, wrect.y), (wrect.x, wrect.y+wrect.height), color=(5, 5, 5))
                window.aaline((wrect.x, wrect.y), (wrect.x+wrect.width, wrect.y), color=(5, 5, 5))
                window.aaline((wrect.x, wrect.y+wrect.height), (wrect.x+wrect.width, wrect.y+wrect.height), color=(255, 255, 255))
                window.aaline((wrect.x+wrect.width, wrect.y), (wrect.x+wrect.width, wrect.y+wrect.height), color=(255, 255, 255))
            elif widget.style == 1:
                window.aaline((wrect.x, wrect.y), (wrect.x, wrect.y+wrect.height), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y), (wrect.x+wrect.width, wrect.y), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y+wrect.height), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
                window.aaline((wrect.x+wrect.width, wrect.y), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
        elif isinstance(widget, Text):
            if widget.bg:
                window.drawrect(wrect, color=widget.bg)
            screen.blit(widget.image, wrect)
        elif isinstance(widget, textbox.Textbox):
            pass
        elif isinstance(widget, Button):
            if widget.style != 3:
                window.drawrect(wrect, color=widget.bg)
            if (widget.style == 0 and not funcs.pressing()) or (widget.style == 1 and funcs.pressing()):
                window.aaline((wrect.x, wrect.y), (wrect.x, wrect.y+wrect.height), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y), (wrect.x+wrect.width, wrect.y), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y+wrect.height), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
                window.aaline((wrect.x+wrect.width, wrect.y), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
            elif (widget.style == 1 and not funcs.pressing()) or (widget.style == 0 and funcs.pressing()):
                window.aaline((wrect.x, wrect.y), (wrect.x, wrect.y+wrect.height), color=(5, 5, 5))
                window.aaline((wrect.x, wrect.y), (wrect.x+wrect.width, wrect.y), color=(5, 5, 5))
                window.aaline((wrect.x, wrect.y+wrect.height), (wrect.x+wrect.width, wrect.y+wrect.height), color=(255, 255, 255))
                window.aaline((wrect.x+wrect.width, wrect.y), (wrect.x+wrect.width, wrect.y+wrect.height), color=(255, 255, 255))
            buffer = widget.image.get_rect()
            buffer.center = wrect.center
            screen.blit(widget.image, buffer)
            del buffer
        elif isinstance(widget, Checkbutton):
            pass
        elif isinstance(widget, Radiobutton):
            pass
        elif isinstance(widget, Listbox):
            window.drawrect(widget.allrect, color=widget.bg)
            for i in range(len(widget.states)):
                if widget.states[i] == 1:
                    window.drawrect(pygame.Rect((wrect.x, wrect.y+i*wrect.height), (wrect.width, wrect.height)), color=widget.selectbg)
            window.aaline((widget.allrect.x, widget.allrect.y), (widget.allrect.x, widget.allrect.y+widget.allrect.height), color=(5, 5, 5))
            window.aaline((widget.allrect.x, widget.allrect.y), (widget.allrect.x+widget.allrect.width, widget.allrect.y), color=(5, 5, 5))
            window.aaline((widget.allrect.x, widget.allrect.y+widget.allrect.height), (widget.allrect.x+widget.allrect.width, widget.allrect.y+widget.allrect.height), color=(255, 255, 255))
            window.aaline((widget.allrect.x+widget.allrect.width, widget.allrect.y), (widget.allrect.x+widget.allrect.width, widget.allrect.y+widget.allrect.height), color=(255, 255, 255))
            for i in widget.images:
                buffer = i.get_rect()
                buffer.topleft = (wrect.x, wrect.y+wrect.height*widget.images.index(i))
                screen.blit(i, buffer)
                del buffer
            for i in range(1, len(widget.images)):
                window.aaline((wrect.x+3, wrect.y+i*wrect.height), (wrect.x+wrect.width-3, wrect.y+i*wrect.height), color=(5, 5, 5))
        elif isinstance(widget, Labelbutton):
            pass
        else:
            raise WidgetDrawError('Some troubles in Widgets')