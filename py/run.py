import tkinter
from PIL import ImageTk
from config import config as configuration, Config
from prepare import prepare

import numpy as np

__author__ = 'oglandx'


tk_root = tkinter.Tk()

imgs = prepare(configuration)
print(imgs)

canvas = tkinter.Canvas(tk_root, width=1300, height=700)
canvas.pack()

# tk_imgs = [[ImageTk.PhotoImage(img) for img in cls] for cls in imgs.values()]
#
# for i, cls in enumerate(tk_imgs):
#     for j, img in enumerate(cls):
#         canvas.create_image((50 + 220*i, 100*(j+1)), image=img)

# for i, cls in enumerate(imgs):
#     for j, img in enumerate(cls):
#         photo = ImageTk.PhotoImage(img)
#         canvas.create_image((100 + 200*i, 100*(j+1)), image=photo)

# labels = ttk.Label(root, image=tuple(element for pck in tk_imgs for element in pck))
# labels.pack(padx=100, pady=100)

for k in imgs.keys():
    print(k)

for i, cls in enumerate(imgs.values()):
    for j, img in enumerate(cls):
        canvas.create_image((Config.size[0]*(0.5 + 1.2*i), Config.size[1]*(j+1)), image=img)

tk_root.mainloop()