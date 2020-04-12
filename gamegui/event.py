from gamegui import *
import threading

def mainevent(event):
    index = -1
    mouse = pygame.mouse.get_pos()
    if event.type == QUIT:
        funcs.exit()
    if pygame.mouse.get_pressed()[0]:
        for i in [x for x in ALL if isinstance(x, Button)]:
            if i.rect.collidepoint(mouse) and not funcs.pressing():
                i.set_focus()
                i()
        for i in [x for x in ALL if isinstance(x, Listbox)]:
            if i.allrect.collidepoint(mouse) and not funcs.pressing():
                i.set_focus()
                index = (mouse[1]-i.rect.y)//i.rect.height
                i.states[index] = 1 if i.states[index]==0 else 0
        funcs.pressing(True)
    else:
        funcs.pressing(False)