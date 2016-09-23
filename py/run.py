import tkinter
from config import config as configuration, Config
from prepare import prepare

__author__ = 'oglandx'


tk_root = tkinter.Tk()

imgs = prepare(configuration)
print(imgs)

canvas = tkinter.Canvas(tk_root, width=1300, height=700)
canvas.pack()

for k in imgs.keys():
    print(k)

for i, cls in enumerate(imgs.values()):
    for j, img in enumerate(cls):
        canvas.create_image((Config.size[0]*(0.5 + 1.2*i), Config.size[1]*(j+1)), image=img)

tk_root.mainloop()