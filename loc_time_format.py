#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
source_file = 'result_push_all.csv'
result_file1 = 'result_all_format_change.csv'
result_file2 = 'result_loc_event.csv'
hours = 24


def change_format(source, result1, result2):
    dict1 = {}
    dict2 = {}
    f = codecs.open(source)
    for line in f:     # line：日期，小时，地址
        line = line.strip('\r\n').split(',')
        hour = int(line[1])
        if line[2] not in dict1:
            dict1[line[2]] = {}
            dict2[line[2]] = {'w':0, 'c':0, 'a':0, 's':0}
            for x in xrange(hours):  # 建立新的多维数组
                lo = {'w':0, 'c':0, 'a':0, 's':0}
                dict1[line[2]][x] = lo
            dict1[line[2]][hour]['w'] = int(line[3])
            dict1[line[2]][hour]['c'] = int(line[4])
            dict1[line[2]][hour]['a'] = int(line[5])
            dict1[line[2]][hour]['s'] = int(line[6])
        else:
            dict1[line[2]][hour]['w'] += int(line[3])
            dict1[line[2]][hour]['c'] += int(line[4])
            dict1[line[2]][hour]['a'] += int(line[5])
            dict1[line[2]][hour]['s'] += int(line[6])
    f.close()

    w = codecs.open(result1, 'w')
    for loc in dict1.keys():
        for hour in dict1[loc].keys():
            dict2[loc]['w'] += int(dict1[loc][hour]['w'])
            dict2[loc]['c'] += int(dict1[loc][hour]['c'])
            dict2[loc]['a'] += int(dict1[loc][hour]['a'])
            dict2[loc]['s'] += int(dict1[loc][hour]['s'])
            need1 = loc + ',' + str(hour) + ',' + str(dict1[loc][hour]['w']) + ',' + str(dict1[loc][hour]['c']) + ',' + str(dict1[loc][hour]['a']) + ',' + str(dict1[loc][hour]['s']) + '\n'
            w.write(need1)
    w.close()
    w1 = codecs.open(result2, 'w')
    for loc in dict1.keys():
        need2 = loc + ',' + str(dict2[loc]['w']) + ',' + str(dict2[loc]['c']) + ',' + str(dict2[loc]['a']) + ',' + str(dict2[loc]['s']) + '\n'
        w1.write(need2)
    w1.close()

if __name__ == '__main__':
    change_format(source_file, result_file1, result_file2)

        





