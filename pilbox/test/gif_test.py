from __future__ import absolute_import, division, with_statement

import itertools
import os
import os.path
import re
from sys import platform as _platform
from io import BytesIO

from PIL import Image, ImageChops, ImageSequence
from PIL.GifImagePlugin import getheader, getdata

import pilbox.image
from tornado.test.util import unittest

DATADIR = os.path.join(os.path.dirname(__file__), "data")
ANIMATED_GIF = os.path.join(DATADIR, "animated.gif")
EXPECTED_GIF = os.path.join(DATADIR, "expected", "animated.gif")

# stolen from https://github.com/python-pillow/Pillow/blob/master/Scripts/gifmaker.py
def write_gif(fp, sequence):
    previous = None
    for im in sequence:
        print(im.info)
        duration = im.info['duration']
        loop = im.info['loop']
        transparency = im.info['transparency']
        im = im.copy()
        if not previous:
            for s in getheader(im)[0] + getdata(im, duration=duration, loop=loop, transparency=transparency):
                fp.write(s)
        else:
            for s in getdata(im, duration=duration, loop=loop, transparency=transparency):
                fp.write(s)
        previous = im.copy()
    fp.write(";".encode('utf-8'))

class GifTest(unittest.TestCase):

    def test_resize(self):
        with open(EXPECTED_GIF, "wb") as fp:
            image = Image.open(ANIMATED_GIF)
            frames = ImageSequence.Iterator(image)
            write_gif(fp, frames)

        print(Image.open(EXPECTED_GIF).info)
