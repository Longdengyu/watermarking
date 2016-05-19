# -*- coding:utf-8 -*-

import os,sys
import random
import unittest
from PIL import Image

def gen_pattern(raw, colum):
    def gen_raw(colum_size):
        out_raw = []
        for i in range(colum_size):
            out_raw.append(float2bin(random.random(),0.5))
        return out_raw

    def float2bin(num,level):
        if num < level:
            return -1
        else:
            return 1
    pattern = []
    # random.seed(seed)
    for i in range(raw):
        pattern.append(gen_raw(colum))
    return pattern

def get_msg(img_object):
    def tobin(num):
        return 0 if num <= 0 else 1
    # img_object = Image.open('me.png') # TODO: remove it
    msg = img_object.convert('1').getdata()
    return [tobin(num) for num in msg]
def msg2img(msg):
    def topixl(num):
        return 0 if num == 0 else 255

    size = (32, 32)
    msg_img = Image.new('L', size)
    msg_img.putdata([topixl(num) for num in msg])
    return msg_img

def cdma(RP, b_seq, I):
    # get b_pattern
    b_pattern = []
    for b, rp in zip(b_seq, RP):
        tmp = []
        for num in rp:
           tmp.append((2*b -1) * num)
        b_pattern.append(tmp)
    # get W
    W = []
    raw_size = len(b_seq)
    colum_size = len(RP[0])
    for colum_index in range(colum_size):
        colum_sum = 0
        for raw_index in range(raw_size):
            colum_sum += b_pattern[raw_index][colum_index]
        W.append(colum_sum)
    # get Iw
    Iw = []
    for w,i in zip(W, I):
        Iw.append(w + i)
    return Iw

def d_cdma(RP, Iw):
    def everage(nums):
        return (sum(nums) + 0.0) / len(nums)
    def to_bin(num):
        return 1 if num > 0 else 0

    E_Iw = everage(Iw)
    size = len(RP)
    b_seq = []
    for i in range(size):
        seq = [(rp0 - everage(RP[i])) * (iw - E_Iw) for rp0, iw in zip(RP[i], Iw)]
        print 'b' + str(i) + '= ' + str(to_bin(everage(seq))) + '--> {0:.1f}'.format(sum(seq))
        # b_seq.append(to_bin(everage(seq)))
        b_seq.append(to_bin(sum(seq)))

    return b_seq


class Test_case(unittest.TestCase):

        def test_cdma(self):
            RP = [
                [-1, 1, 1, -1, -1, 1, -1, -1, 1, 1, -1],
                [1, 1, -1, -1, 1, -1, -1, 1, 1, -1, 1 ],
                [1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1],
                [-1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1],
                [-1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1],
                [1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1],
                [-1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1]

            ]
            b_seq = [1, 1, 0, 0, 1, 0, 1]
            I = [98, 98, 97, 98, 97, 96, 97, 96, 95, 94, 94]
            Iw = cdma(RP, b_seq,I)
            self.assertEqual(Iw,[95, 103, 98, 95, 98, 99, 90, 97, 98, 93, 97])

        def test_d_cdma(self):
            # TODO: d_cema 函数有问题。测试不能通过。
            RP = [
                [-1, 1, 1, -1, -1, 1, -1, -1, 1, 1, -1],
                [1, 1, -1, -1, 1, -1, -1, 1, 1, -1, 1],
                [1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1],
                [-1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1],
                [-1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1],
                [1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1],
                [-1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1]
            ]
            # Iw = [95, 103, 98, 95, 98, 99, 90, 97, 98, 93, 97]

            def gen_raw(colum_size):
                out_raw = []
                for i in range(colum_size):
                    out_raw.append(float2bin(random.random(), 0.5))
                return out_raw

            def float2bin(num, level):
                if num < level:
                    return 0
                else:
                    return 1


            # b_seq = [1, 1, 0, 0, 1, 0, 1]
            # self.assertEqual(d_cdma(RP, Iw), b_seq)
            I = [98, 98, 97, 98, 97, 96, 97, 96, 95, 94, 94]
            for i in range(10):
                b_seq = gen_raw(7)
                # b_seq = [1, 1, 0, 0, 1, 0, 1]
                Iw = cdma(RP,b_seq,I)
                self.assertEqual(d_cdma(RP, Iw), b_seq)
                break # todo: remove it
        def test_get_msg(self):
            msg_object = Image.open('watermark.png')
            msg = get_msg(msg_object)
            print msg
        def test_msg2img(self):
            msg_object = Image.open('watermark.png')
            msg = get_msg(msg_object)
            obj = msg2img(msg)
            msg2 = get_msg(obj)
            self.assertEqual(msg, msg2)

if __name__ == '__main__':
    def print_pattern(pattern):
        for raw in pattern:
            print raw
    print_pattern(gen_pattern(3,5))