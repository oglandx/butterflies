from functools import reduce

from PIL import Image, ImageFilter, ImageDraw
from os import getcwd

__author__ = 'oglandx'


def get_lines(path):
    with open(path) as file:
        return {
            line: content.strip()
            for line, content in enumerate(file)
        }


def get_class_paths(classes_file, paths_file):
    classes = get_lines(classes_file)
    paths = get_lines(paths_file)
    if len(classes) != len(paths):
        raise AssertionError("Lengths of files must be the same")
    return {
        int(cls): [
            paths.get(_line) for _line, _cls in classes.items()
            if _cls == cls
        ] for cls in set(classes.values())
    }


def get_class_paths_limited(classes_file, paths_file, min_items_in_class=15, limit=None, **kwargs):
    return {
        cls: values[:limit] for cls, values in get_class_paths(classes_file, paths_file).items()
        if len(values) > min_items_in_class
    }


def get_colors(image, colors_num=10, swatch_size=10):
    '''
    https://gist.github.com/zollinger/1722663
    '''

    resize = min(image.width, image.height)
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=colors_num)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)

    pal = Image.new('RGB', (swatch_size*colors_num, swatch_size))

    draw = ImageDraw.Draw(pal)
    posx = 0
    for count, col in colors:
        draw.rectangle([posx, 0, posx + swatch_size, swatch_size], fill=col)
        posx += swatch_size
    del draw

    return pal


def img_prepare_func_pillow(path, **kwargs):
    raise NotImplemented()


def img_prepare_func_cv(path, **kwargs):
    raise NotImplemented()


def get_images_with_limit_class_items_im(classes_file, paths_file, root=None,
                                         img_prepare_func=None, exclude=None, **kwargs):
    if not root:
        root = getcwd()
    if not img_prepare_func:
        img_prepare_func = img_prepare_func_pillow
    if not exclude:
        exclude = []
    return {
        cls: [img_prepare_func('%s/%s' % (root, path), **kwargs) for path in paths]
        for cls, paths in get_class_paths_limited(classes_file, paths_file, **kwargs).items()
        if cls not in exclude
    }


def prepare(config):
    return get_images_with_limit_class_items_im(
        config.classes,
        config.paths,
        config.root,
        img_prepare_func=config.prepare,
        size=config.size,
        conversion_mode=config.conversion,
        min_items_in_class=config.min_items_in_class,
        limit=config.limit_items_for_class,
        exclude=config.exclude_classes,
    )
