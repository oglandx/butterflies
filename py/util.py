try:
    from cv2 import cv2
except ImportError:
    import cv2
from PIL import Image, ImageTk
import numpy as np


def cv2tk(img):
    b, g, r = cv2.split(img)
    array = cv2.merge((r, g, b))
    image = Image.fromarray(array)
    return ImageTk.PhotoImage(image=image)


def make_background(size, color):
    image = np.zeros((size[0], size[1], 3), np.uint8)
    image[:, :] = color
    return image
