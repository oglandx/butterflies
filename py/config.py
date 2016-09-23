from os import getcwd
from PIL import Image
from prepare import get_colors
import numpy as np

try:
    from cv2 import cv2
except ImportError:
    import cv2

from util import cv2tk, make_background

__author__ = 'oglandx'


class Config:
    # root directory of the project with all files
    root = '%s/..' % getcwd()

    # file that describes classes and their relations to images
    classes = '%s/labels.txt' % root

    # file that describes paths to images
    paths = '%s/imagelist.txt' % root

    min_items_in_class = 17

    limit_items_for_class = 9

    size = (70, 70)

    border = (5, 5)

    @property
    def __size(self):
        return self.size[0] - 2*self.border[0], self.size[1] - 2*self.border[1]

    crop = (0, 0)

    def __crop(self, img):
        return img[self.crop[0]:len(img[0]) - self.crop[0], self.crop[1]:len(img[1]) - self.crop[1]]

    conversion = "RGB"

    exclude_classes = (
        155,
        194,
        62,
        223,
        162,
        277,
        179,
        157,
        89,
        120
    )

    min_points_in_contour = 90

    def prepare(self, path, **kwargs):
        img = cv2.imread(path)
        thumb = self.__crop(cv2.resize(img, self.__size, interpolation=cv2.INTER_AREA))

        background = make_background(self.size, (255, 255, 255))
        background[self.border[0]:self.size[0] - self.border[0], self.border[1]:self.size[1] - self.border[1]] = thumb
        thumb = background

        img_gray = cv2.cvtColor(thumb, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(img_gray, 170, 255, 0)
        im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        prepared_contours = sorted(contours, key=lambda k: cv2.contourArea(k), reverse=True)
        main_contour = prepared_contours[1]
        cv2.drawContours(thumb, [main_contour], -1, (0, 255, 0), 2)
        return cv2tk(thumb) if len(main_contour) > self.min_points_in_contour else None


config = Config()