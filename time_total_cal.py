#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
from itertools import islice
source_path = 'result_push_all.csv'
result_path = 'result_time_total_cal.csv'
hours = 24
list_location = []


def time_total_cal(source_path, result_path):
    dict1 = {}
    dict2 = {}
    for x in xrange(hours):  # 建立新的三维数组
        location = {}
        dict1[x] = location
        dict2[x] = {'w':0, 'c':0, 'a':0, 's':0}
    # 存入新字典

    f = codecs.open(source_path)
    for line in islice(f, 1, None):
        line = line.strip('\r\n').split(',')
        hour = int(line[1])
        location1 = line[2]
        if location1 in dict1[hour]:
            dict1[hour][location1]['w'] += int(line[3])
            dict1[hour][location1]['c'] += int(line[4])
            dict1[hour][location1]['a'] += int(line[5])
            dict1[hour][location1]['s'] += int(line[6])
        else:
            dict1[hour][location1] = {}
            dict1[hour][location1]['w'] = int(line[3])
            dict1[hour][location1]['c'] = int(line[4])
            dict1[hour][location1]['a'] = int(line[5])
            dict1[hour][location1]['s'] = int(line[6])
    f.close()

    w = codecs.open(result_path, 'w')
    for hour2 in xrange(hours):
        for loc in dict1[hour2].keys():
            dict2[hour2]['w'] += dict1[hour2][loc]['w']
            dict2[hour2]['c'] += dict1[hour2][loc]['c']
            dict2[hour2]['a'] += dict1[hour2][loc]['a']
            dict2[hour2]['s'] += dict1[hour2][loc]['s']
        need1 = str(hour2) + ',' + str(dict2[hour2]['w']) + ',' + str(dict2[hour2]['c']) + ',' + str(dict2[hour2]['a']) + ',' + str(dict2[hour2]['s']) + '\n'
        w.write(need1)

    w.close()
    print 'time done'

if __name__ == '__main__':
    time_total_cal(source_path, result_path)