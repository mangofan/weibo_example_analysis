#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import jieba.posseg as pseg

import jieba
jieba.load_userdict('shanghai_diming_library.txt')

words = pseg.cut('我在延安高架堵车了')
for w in words:
    print w.word,w.flag