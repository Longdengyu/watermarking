# -*- coding:utf-8 -*-
from util import gen_pattern, cdma, get_msg
import random
from PIL import Image
from math import ceil
# TODO: 修改times那里的代码，使得能够嵌入任意长度的message。
def embeding(cover_object, message, seed):
    # message means b_seq the message length should be 32*32
    # every time we process 8 pixels on Image and 8 pixel will embed to the image
    # so the size of RP should be as 8*8, embed 8 to image 32*32/8 = 128 times
    raw, colum = (8, 8)
    # get gray_scale
    # gray_scale =  cover_object.convert("L").getdata()
    im= cover_object.convert('YCbCr')
    source = im.split()
    Y,Cb,Cr = 0, 1, 2
    gray_scale = [i for i in source[Y].getdata()]

    watered_gray_scale = []
    random.seed(seed)
    # times = 128 # 32*32/8
    len_msg = len(message)
    times = int(ceil((len_msg + 0.0)/ 8))
    left = (len_msg + 0.0) % 8
    if left > 0:
        message += [0] * (8 - left)

    msg_point = 0
    gray_point = 0
    # embed the msg on gray scale
    for i in range(times):
        RP = gen_pattern(raw, colum)
        b_seq = message[msg_point:msg_point + 8]
        I = gray_scale[gray_point:gray_point + 8]
        Iw = cdma(RP, b_seq, I)
        for num in Iw:
            watered_gray_scale.append(num)
        msg_point += 8
        gray_point += 8
    watered_size = len(watered_gray_scale)
    gray_scale[:watered_size] = watered_gray_scale
    source[Y].putdata(gray_scale)
    image = Image.merge(im.mode, source)
    image = image.convert('RGB')
    return image



