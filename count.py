#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import codecs
from itertools import islice

source_path = 'result_push_all.csv'


def count(source_path, result_path):
    f = codecs.open(source_path)
    dict ={'0':{'w':0, 'c':0, 'a':0, 's':0},'loc':{'w':0, 'c':0, 'a':0, 's':0}}
    for line in islice(f, 1, None):
        line = line.strip('\r\n').split(',')
        location = line[2]
        if line[2] != '0':
            dict['loc']['w'] += int(line[3])
            dict['loc']['c'] += int(line[4])
            dict['loc']['a'] += int(line[5])
            dict['loc']['s'] += int(line[6])
        else:
            dict['0']['w'] += int(line[3])
            dict['0']['c'] += int(line[4])
            dict['0']['a'] += int(line[5])
            dict['0']['s'] += int(line[6])
    f.close()
    w = codecs.open(result_path, 'a+')
    need = 'loc,%d,%d,%d,%d\n'%(dict['loc']['w'],dict['loc']['c'],dict['loc']['a'],dict['loc']['s'])
    w.write(need)
    need1 = '0,%d,%d,%d,%d\n' % (dict['0']['w'], dict['0']['c'], dict['0']['a'], dict['0']['s'])
    w.write(need1)

if __name__ == '__main__':
    result_path = 'result_count.csv'
    count(source_path, result_path)
