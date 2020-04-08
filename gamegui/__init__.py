from gamegui.error import *
try:
    import pygame
except ImportError:
    raise ReliantMuduleNotFound('Please install the mudule PYGAME')
import os, sys, threading
from pygame.locals import *
try:
    from PIL import Image as Pillow
except ImportError:
    raise ReliantMuduleNotFound('Please install the mudule PILLOW')

pygame.init()
fontname = os.path.split(__file__)[0]+'/fonts/mainfont.ttf'
_ALL = []
ALL = []
SELECT = 0

def fontpath(path):
    global fontname
    fontname = os.path.abspath(path)

class Control:
    def __init__(self, root):
        self.root = root
        _ALL.append(self)
    def update(self):
        i = _ALL.index(self)
        _ALL.remove(self)
        _ALL.insert(i, self)
        if self in ALL:
            i = ALL.index(self)
            ALL.remove(self)
            ALL.insert(i, self)
    def kill(self):
        _ALL.remove(self)
        if self in ALL:
            ALL.remove(self)
        del self
    def place(self, rect=None):
        self.rect = rect if isinstance(rect, (tuple, list)) else (rect if rect else self.root.rect.topleft)
        ALL.append(self)
        self.update()
    def unplace(self):
        del self.rect
        ALL.remove(self)
        self.update()
    def set_focus(self):
        SELECT = _ALL.index(self)
    def tip(self, string, size, bg=(255, 255, 255), fg=(0, 0, 0)):
        self.tip = pygame.Surface(size)
        self.tip.fill(bg)
        self.tip = self.tip.convert_alpha()
        self.tip.blit(self.font.render(string, True, fg), (0, 0))
    def tiplist(self, lst):
        pass

import gamegui.draw as draw

XSB = 'xscrollbar'
YSB = 'yscrollbar'
class Scrollbar(Control):
    def __init__(self, root, type):
        assert type=='xscrollbar' or type=='yscrollbar'
        self.type = type
        Control.__init__(self, root)
    def set_focus(self):
        raise VoidFuncError('Void define')

class Window(draw.Canvas):
    def __init__(self, size, mode, caption='Window', icon=None):
        draw.Canvas.__init__(self, None, size)
        _ALL.clear()
        _ALL.append(self)
        
        if icon:
            pygame.display.set_icon(icon.surface())
        self.screen = pygame.display.set_mode((size[0], size[1]), mode)
        self.size, self.caption, self.mode, self.fs, self.rs = \
                      size, caption, mode, True if mode==FULLSCREEN else False, True if mode==RESIZABLE else False
        pygame.display.set_caption(self.caption)
        global ROOTWD
        ROOTWD = self
        draw.Canvas.update(self)
    def __len__(self):
        return self.size
    def icon(self, image):
        pygame.display.set_icon(image.surface())
    def fullscreen(self):
        pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode\
                      ((self.size[0], self.size[1]), self.mode if self.fs else FULLSCREEN)
        self.fs = not self.fs
        draw.Canvas.update(self)
    def isfullscreen(self):
        return self.fs
    def resizable(self):
        pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode\
                      ((self.size[0], self.size[1]), self.mode if self.rs else RESIZABLE)
        self.rs = not self.fs
        draw.Canvas.update(self)
    def isresizable(self):
        return self.rs
    def title(self, caption):
        self.caption = caption
        pygame.display.set_caption(self.caption)
        draw.Canvas.update(self)
    def get_title(self):
        return self.caption
    def kill(self):
        pygame.display.quit()
        pygame.display.init()
        _ALL = []
        del self
    def resize(self, size):
        self.size = size
        pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode\
                      ((self.size[0], self.size[1]),\
                      FULLSCREEN if self.fs else (RESIZABLE if self.rs else self.mode))
        draw.Canvas.update(self)
    def place(self, rect):
        raise VoidFuncError('Void define')
    def unplace(self):
        raise VoidFuncError('Void define')

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
        self.pillow = Pillow.open(path)
        self.rgba = self.pillow.convert('RGBA')
        Control.__init__(self, root)
    def __len__(self):
        return self.pillow.size
    def __getitem__(self, index):
        return self.rgba.getpixel(index)
    def surface(self):
        return self.image

READONLY = 'readonly'
READWRITE = 'readwrite'
PASSWORD = '*'
class Text(Control):
    def __init__(self, root, text='', font=(None, 20), state='readonly', show=None, bg=None, fg=(0, 0, 0), xscrollbar=False, yscrollbar=False):
        self.imgs = []
        self.positions = []
        self.positions_ = []
        self.end = len(text)
        self.active = [self.end, -1]
        self.text, self.state, self.show, self.bg, self.fg, self.xscrollbar, self.yscrollbar = text, state, show, bg, fg, xscrollbar, yscrollbar
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.image = self.font.render(self.text, True, self.fg)
        Control.__init__(self, root)
    def __str__(self):
        return self.text
    def __len__(self):
        return self.end
    def __getitem__(self, key):
        return self.imgs[self.positions.index(key)] if key in self.positions else (self.imgs[self.positions_.index(key)] if key in self.positions_ else self.text[key])
    def set(self, value='', position=None):
        if isinstance(value, int):
            if value>self.end:
                raise ValueError
            self.active = [value, -1]
        elif isinstance(value, list):
            if value[0]>self.end or value[1]>self.end:
                raise ValueError
            self.active = value
        elif isinstance(value, Image):
            if position:
                self.imgs.append(value)
                self.positions.append(position)
                self.positions_.append(self.end-position)
                self.end += 1
                self.active = position+1
            else:
                self.imgs = [value]
                self.positions = [0]
                self.positions_ = [-1]
                self.text = ''
                self.end = 1
                self.active = self.end
        elif isinstance(value, str):
            self.text = self.text[:position]+value+self.text[position:] if position else value
            self.end = len(self.text)
            self.active = position+len(value) if position else self.end
        else:
            raise ValueError
        self.image = self.font.render(self.text, True, self.fg)
        Control.update(self)
    def get(self):
        return str(self)
    def append(self, value):
        self.set(value, self.end)
    def insert(self, value):
        if self.active[1] != -1:
            self.remove(self.active)
        self.set(value, self.active[0])
    def remove(self, key):
        if isinstance(key, int):
            if key in self.positions:
                self.imgs.pop(self.positions.index(key))
                self.positions.remove(key)
            elif key in self.positions_:
                self.imgs.pop(self.positions_.index(key))
                self.positions_.remove(key)
            else:
                self.text = self.text[:key]+self.text[key+1:]
        elif isinstance(key, str):
            if not key in self.text:
                raise ValueError
            self.text = self.text.replace(key, '')
        elif isinstance(key, (tuple, list)):
            if len(key) > 2:
                self.text = self.text.replace(*key)
            elif len(key) == 2:
                self.text = self.text[:key[0]]+self.text[key[1]+1:]
            else:
                raise ValueError
        self.image = self.font.render(self.text, True, self.fg)
        Control.update(self)

PUSH = 0
PULL = 1
SMOOTH = 2
IMAGE = HIDDEN = 3
class Button(Control):
    def __init__(self, root, text, font=(None, 20), style=0, bg=(240, 240, 240), fg=(0, 0, 0), command=None):
        self.text, self.style, self.bg, self.command = text, style, bg, command if command else lambda x=None:x
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.image = self.font.render(self.text, True, fg) if isinstance(self.text, str) else text.image
        Control.__init__(self, root)
    def __call__(self):
        return self.command()

# ------------------------------------------------------ #
COMMON = CMN = 0
SELECTED = SLC = 1
LOCKED = LOC = 2
LOCKED_AND_SELECTED = LAS = 3

class Checkbutton(Control):
    def __init__(self, root, texts, font=(None, 20), bg=(240, 240, 240), fg=(0, 0, 0), xscrollbar=False, yscrollbar=False):
        self.texts, self.bg, self.fg, self.xscrollbar, self.yscrollbar = texts, bg, fg, xscrollbar, yscrollbar
        self.states = [0]*len(self.texts)
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.images = [self.font.render(x, True, self.fg) for x in self.texts]
        Control.__init__(self, root)
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, key):
        if key[1] == True:
            return self.getbool()[key[0]]
        else:
            return self.get()[key[0]]
    def __setitem__(self, key, value):
        self.set(key, value)
        Control.update(self)
    def set(self, index, state):
        assert isinstance(state, int) and state<4
        self.states[index] = state
        if state <= 1:
            self.images[index] = self.font.render(self.texts[index], True, self.fg)
        elif state >= 2:
            self.images[index] = self.font.render(self.texts[index], True, (self.fg[0]+50, self.fg[1]+50, self.fg[2]+50))
        Control.update(self)
    def get(self):
        return self.states
    def getbool(self):
        bl = [False]*len(self.states)
        for i in self.states:
            if i==1 or i==3:
                bl[self.states.index(i)] = True
        return bl

class Radiobutton(Control):
    def __init__(self, root, texts, font=(None, 20), bg=(240, 240, 240), fg=(0, 0, 0), xscrollbar=False, yscrollbar=False):
        self.texts, self.bg, self.fg, self.xscrollbar, self.yscrollbar = texts, bg, fg, xscrollbar, yscrollbar
        self.states = [0]*len(self.texts)
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.images = [self.font.render(x, True, self.fg) for x in self.texts]
        Control.__init__(self, root)
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, key):
        if key[1] == True:
            return self.getbool()[key[0]]
        else:
            return self.get()[key[0]]
    def __setitem__(self, key, value):
        self.set(key, state)
        Control.update(self)
    def set(self, index, state):
        assert isinstance(state, int) and state<3
        if state == 1 and 1 in self.states:
            self.states[self.states.index(1)] = 0
        self.states[index] = state
        if state <= 1:
            self.images[index] = self.font.render(self.texts[index], True, self.fg)
        elif state == 2:
            self.images[index] = self.font.render(self.texts[index], True, (self.fg[0]+50, self.fg[1]+50, self.fg[2]+50))
        Control.update(self)
    def get(self):
        return self.states
    def getbool(self):
        bl = [False]*len(self.states)
        for i in self.states:
            if i==1:
                bl[self.states.index(i)] = True
        return bl

class Listbox(Control):
    def __init__(self, root, texts, font=(None, 20), style=0, bg=(240, 240, 240), fg=(0, 0, 0), commands=None, xscrollbar=False, yscrollbar=False):
        self.texts, self.style, self.bg, self.fg, self.xscrollbar, self.yscrollbar = texts, style, bg, fg, xscrollbar, yscrollbar
        if commands:
            assert len(commands)==len(texts)
        self.states = [0]*len(self.texts)
        self.commands = commands if commands else [lambda x=None:x]*len(self.texts)
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.images = [(self.font.render(x, True, fg) if isinstance(x, str) else x.image) for x in self.texts]
        Control.__init__(self, root)
    def __len__(self):
        return len(self.texts)
    def __call__(self, key):
        return self.commands[key]()
    def __getitem__(self, key):
        return self.texts[key]
        Control.update(self)
    def __setitem__(self, key, value):
        self.commands[key] = value
    def set(self, key, value):
        if isinstance(value, int):
            assert value < 2
            self.states[key] = value
        self.texts[key] = value
        self.images[key] = self.font.render(value, True, self.fg) if isinstance(value, str) else value.image
        Control.update(self)
    def get(self, type='text'):
        if type == 'text':
            return self.texts
        elif type == 'state':
            return self.states
        elif type == 'command':
            return self.commands
        else:
            raise ValueError
    def append(self, text, command=None):
        self.texts.append(text)
        self.commands.append(command if command else lambda x=None:x)
        self.images.append(self.font.render(text, True, self.fg) if isinstance(text, str) else text.image)
        Control.update(self)
    def pop(self, key):
        self.texts.pop(key)
        self.commands.pop(key)
        self.images.pop(key)
        Control.update(self)
    def remove(self, value):
        key = self.texts.index(value)
        self.pop(key)
        Control.update(self)

class Labelbutton(Control):
    def __init__(self, root, titles, values, icon=None, font=(None, 20), bg=(240, 240, 240), fg=(0, 0, 0)):
        self.titles, self.values, self.bg = titles, values, bg
        self.value = None
        self.font = pygame.font.Font(font[0] if font[0] else fontname, font[1])
        self.images = [self.font.render(x, True, fg) for x in self.titles]
        null = pygame.Surface((32, 32))
        null.fill(self.bg + ((0,) if isinstance(self.bg, tuple) else [0,]))
        null = null.convert_alpha()
        self.icon = icon.surface() if icon else null
        Control.__init__(self, root)
    def __abs__(self):
        return self.value
    def set(self, key):
        self.value = self.values[key]
        Control.update(self)
    def get(self):
        return abs(self)
    def icon(self, image):
        self.icon = image.surface()
        Control.update(self)
# ------------------------------------------------------ #

class Funcs:
    def exit(self, errorlevel=0):
        pygame.quit()
        sys.exit(errorlevel)
    def set_exit(self, define):
        self.exit = define
    def touched(self, rect, mouse):
        if rect.x<mouse[0] and mouse[0]<rect.x+rect.width and rect.y<mouse[1] and mouse[1]<rect.y+rect.height:
            return True
        else:
            return False
funcs = Funcs()

def maindraw(window):
    screen = window.screen
    window.clear()
    for widget in ALL:
        wrect = widget.rect
        if isinstance(widget, Image):
            screen.blit(widget.surface(), wrect)
        elif isinstance(widget, Text):
            if widget.bg:
                window.drawrect(wrect, color=widget.bg)
            screen.blit(widget.image, wrect)
        elif isinstance(widget, Button):
            if widget.style == 0:
                window.drawrect(widget.rect, color=widget.bg)
                window.aaline((wrect.x, wrect.y), (wrect.x, wrect.y+wrect.height), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y), (wrect.x+wrect.width, wrect.y), color=(255, 255, 255))
                window.aaline((wrect.x, wrect.y+wrect.height), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
                window.aaline((wrect.x+wrect.width, wrect.y), (wrect.x+wrect.width, wrect.y+wrect.height), color=(5, 5, 5))
            buffer = widget.image.get_rect()
            buffer.center = wrect.center
            screen.blit(widget.image, buffer)
            del buffer
        elif isinstance(widget, Checkbutton):
            pass
        elif isinstance(widget, Radiobutton):
            pass
        elif isinstance(widget, Listbox):
            pass
        elif isinstance(widget, Labelbutton):
            pass
        else:
            raise WidgetDrawError('Some troubles in ALL')

def mainloop(delay=20):
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                funcs.exit()
            elif pygame.mouse.get_pressed()[0]:
                for i in [x for x in ALL if isinstance(x, Button)]:
                    if funcs.touched(i.rect, mouse):
                        i()
        maindraw(ROOTWD)
        pygame.display.update()
        pygame.time.delay(delay)
