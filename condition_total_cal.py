#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import codecs
from itertools import islice
source_path = 'result_push_all.csv'
result_path = 'result_condition_total_cal.csv'


# 首先看四种情况（天气、拥堵、事故、地铁）的总数量
def condition_total_cal(source_path, result_path):
    f = codecs.open(source_path)
    dict1 = {}
    for line in f:
        line = line.strip('\r\n').split(',')
        location = line[2]
        if location in dict1:
            dict1[location]['w'] += int(line[3])
            dict1[location]['c'] += int(line[4])
            dict1[location]['a'] += int(line[5])
            dict1[location]['s'] += int(line[6])
        else:
            dict1[location] = {}
            dict1[location]['w'] = int(line[3])
            dict1[location]['c'] = int(line[4])
            dict1[location]['a'] = int(line[5])
            dict1[location]['s'] = int(line[6])

    w = codecs.open(result_path, 'w')  # 要写的文件
    for loc in dict1.keys():
        need = loc + ',' + str(dict1[loc]['w']) + ',' + str(dict1[loc]['c']) + ',' + str(dict1[loc]['a']) + ',' + str(dict1[loc]['s']) + '\n'
        w.write(need)
    w.close()
    print 'condition done'

if __name__ == '__main__':
    condition_total_cal(source_path, result_path)