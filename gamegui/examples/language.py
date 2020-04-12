from gamegui import *

root = Window((300, 200), 0)
root.title('Demo - Language')
listbox = Listbox(root, ['Python', 'C++', 'C', 'Html', 'JavaScript', 'CSS', 'Java', 'DOS', 'VBs'])
listbox.place(pygame.Rect((100, 10), (100, 15)))

mainloop()
