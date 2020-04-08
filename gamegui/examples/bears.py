from gamegui import *

n = 1
def f():
    global n
    text.set(str(n)+' bears')
    n += 1

root = Window((300, 200), 0)
root.title('Demo - Bears')
Button(root, 'click me', command=f).place(pygame.Rect((100, 50), (100, 50)))
text = Text(root)
#text = Text(root, bg=(0, 255, 0))
text.place(pygame.Rect((110, 105), (80, 20)))

mainloop()
