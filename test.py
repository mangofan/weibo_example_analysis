#!/usr/bin/python
# -*- coding: utf-8 -*-

import time_standard
import codecs
import jieba.posseg as pseg
import jieba
jieba.load_userdict('shanghai_diming_library.txt')
list_weather = [u'雨', u'下雨', u'暴雨', u'雪', u'下雪', u'雾', u'下雾', u'冰雹', u'下冰雹', u'霾', u'台风', u'气旋', u'厄尔尼诺', u'风力', u'天气', u'温度', u'凉', u'热', u'暑', u'寒']
list_congestion = [u'堵', u'堵车', u'堵住', u'塞车', u'塞住', u'拥堵', u'排积', u'缓慢']
list_accident = [u'碰', u'碰倒', u'撞', u'相撞', u'碰撞', u'交通事故', u'刮', u'剐', u'蹭', u'追尾', u'塌方', u'超速', u'超载', u'闯红灯', u'变道', u'车祸', u'逆行']  #  , u'事故'
list_subway = [u'号线', u'地铁']


def list_location_build(path):
    f = codecs.open(path)
    list = []
    for line in f:
        line = line.strip('\r\n').split(' ')
        list.append(line[0].decode('utf-8'))
    return list


def compare(text):     # 返回每一条微博是否包含需要的信息，分为三个参数：是否天气，是否交通状况，是否含有地理位置
    words = pseg.cut(text)   # 分词,分词结果含有词性
    label_e = '0'
    for w in words:
        if w.word in list_location:   # 是否是某个地名
            if w.word == u'热带风暴':
                label_e = '1'
    return label_e

def build_state_dict(file_path):
    f = codecs.open(file_path)
    e = codecs.open('redaifengbao.txt', 'w')
    i = 0
    for line in f:
        i += 1
        text = line.strip('\r\n').split(',')[7]  # 微博正文
        label_e = compare(text)   # 调用分词库函数，同时判断该微博所含信息是否
        if label_e == '1':
            print text
            print i
            e.write(text)
            e.write('\n')
    f.close()
    e.close()

if __name__ == '__main__':
    list_location = list_location_build('shanghai_diming_library.txt')
    global list_location
    build_state_dict('weibo1.txt')

