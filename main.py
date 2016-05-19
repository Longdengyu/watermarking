# -*- coding:utf-8 -*-
from PIL import Image
from util import *
from embeding import *
from detecting import *

cover_file = 'me.png'
watermarked_file = 'watermarked.png'
watermark_file = 'watermark.bmp'
detected_file = 'detected_watermark.bmp'
# TODO: 水印嵌入前后不一样
cover_object = Image.open(cover_file)
msg_object = Image.open(watermark_file)
msg = get_msg(msg_object)
seed = 123

watered_img = embeding(cover_object, msg, seed)
watered_img.save(watermarked_file)
watermark = detecting(watered_img, seed)
watermark.save(detected_file)

# TODO: 添加图形界面， 水印信息手工输入，生成一个



