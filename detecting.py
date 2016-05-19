# -*- coding:utf-8 -*-
from util import *
import random
# 修改函数，使得能够提取任意长度的message

def detect_msg(watermarked_image, seed, msg_length):
    random.seed(seed)
    times = 128 # 32*32/8
    im = watermarked_image.convert('YCbCr')
    source = im.split()
    Y, Cb, Cr = 0, 1, 2
    gray_scale = [i for i in source[Y].getdata()]
    point = 0
    watermark_msg = []
    for i in range(times):
        # get Iw
        Iw = gray_scale[point: point + 8]
        point += 8
        # get RP
        raw, colum = 8, 8
        RP = gen_pattern(raw,colum)
        msg = d_cdma(RP, Iw)
        watermark_msg += msg
    # watermark_obj = msg2img(watermark_msg)
    # return watermark_obj
    return watermark_msg

def detecting(watermarked_image,seed):
    MSG_LENGTH = 1024 # 32*32 the watermark img size
    msg = detect_msg(watermarked_image, seed,MSG_LENGTH)
    watermark_obj = msg2img(msg)
    return watermark_obj

