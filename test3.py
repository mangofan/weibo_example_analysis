#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import codecs
import jieba.posseg as pseg
import jieba

jieba.load_userdict('shanghai_diming_library.txt')
library_path = 'shanghai_diming_library.txt'
file_path = 'result_push_all.csv'


def search_and_destory(file_path, library_path):
    words = pseg.cut('江桥收费站至中环路严重堵塞，大量外地车辆涌入上海')

    for word in words:
        print word.word, word.flag

if __name__ == '__main__':
    search_and_destory(file_path, library_path)