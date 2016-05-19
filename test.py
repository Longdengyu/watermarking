# -*- coding:utf-8 -*-
from util import *
def to_bin(num, level):
    return 0 if num < 256*level else 255

from PIL import Image
im = Image.open('watermark1.png')
im = im.convert('L')
datas = im.getdata()
level = 0
processed_datas = [(to_bin(data, level) for data in datas)]
im.putdata(processed_datas)
im = im.convert('RGB')
im.save('watermark.bmp')
