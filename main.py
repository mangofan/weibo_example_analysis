#!/usr/bin/python
# -*- coding: utf-8 -*-

# 一共接近457000条数据
import time_standard
import codecs
import jieba.posseg as pseg
import jieba
jieba.load_userdict('shanghai_diming_library.txt')

start_date = '20140521'
end_date = '20150430'
hours = 24

list_weather = [u'雨', u'下雨', u'暴雨', u'雪', u'下雪', u'雾', u'下雾', u'冰雹', u'下冰雹', u'霾', u'台风', u'气旋', u'厄尔尼诺', u'风力', u'天气', u'温度', u'凉', u'热', u'暑', u'寒', u'热带风暴']
list_congestion = [u'堵', u'堵车', u'堵住', u'塞车', u'塞住', u'拥堵', u'排积', u'缓慢']
list_accident = [u'碰', u'碰倒', u'撞', u'相撞', u'碰撞', u'交通事故', u'刮', u'剐', u'蹭', u'追尾', u'塌方', u'超速', u'超载', u'闯红灯', u'变道', u'车祸', u'逆行']  #  , u'事故'
list_subway = [u'号线', u'地铁']
list_ambiguity = [u'收费站', u'大桥', u'港口']
dates = time_standard.dateRange(start_date, end_date)  # 获取时间的标准表示格式


def compare(text):     # 返回每一条微博是否包含需要的信息，分为三个参数：是否天气，是否交通状况，是否含有地理位置
    words = pseg.cut(text)   # 分词,分词结果含有词性
    label_a = label_b = label_c = label_d = 0
    label_e = '0'
    rem_word = '0'
    for w in words:
        if w.word in list_weather:   # 是否与天气有关,是的话，设置为 1
            label_a = 1
        elif w.word in list_congestion:  # 是否与拥堵有关
            label_b = 1
        elif w.word in list_accident:  # 是否与事故有关
            label_c = 1
        elif w.word in list_subway:  # 是否与地铁有关
            label_d = 1
        elif w.word in list_location:   # 是否是某个地名
            label_e = w.word
        elif w.word in list_ambiguity :
            label_e = rem_word + w.word
            list_location.append(label_e)
            # 注意这个地方如果出现多个地名的话只能最后记住一个
        rem_word = w.word
    return label_a, label_b, label_c, label_d, label_e


def list_location_build(path):
    f = codecs.open(path)
    list = []
    for line in f:
        line = line.strip('\r\n').split(' ')
        list.append(line[0].decode('utf-8'))
    return list


def build_state_dict(file_path):
    f = codecs.open(file_path)
    count = 0
    list_location = list_location_build('shanghai_diming_library.txt')
    global list_location

    k = codecs.open('weibo_uncounted.txt', 'a+')
    lw = codecs.open('weibo_loc_weather.txt', 'a+')
    lc = codecs.open('weibo_loc_congestion.txt', 'a+')
    la = codecs.open('weibo_loc_accident.txt', 'a+')
    ls = codecs.open('weibo_loc_subway.txt', 'a+')
    nlw = codecs.open('weibo_noloc_weather.txt', 'a+')
    nlc = codecs.open('weibo_noloc_congestion.txt', 'a+')
    nla = codecs.open('weibo_noloc_accident.txt', 'a+')
    nls = codecs.open('weibo_noloc_subway.txt', 'a+')
    k_count = lw_count = lc_count = la_count = ls_count = nlw_count = nlc_count = nls_count = nla_count = 0

    hough = {}  # 建立三维词典，但是没有初始化
    for x in dates:  # 每天
        yhough = {}
        for y in xrange(hours):  # 每小时
            rhough = {}
            yhough[int(y)] = rhough
        hough[x] = yhough

    for line in f:
        line = line.strip('\r\n').split(',')
        text = line[7]  # 微博正文
        time = line[3].split(' ')    # time 是str型
        day = time[0]
        hour = int(time[1].split(':')[0])   # 分离出小时  hour是 int 型

        w, c, a, s, label_e = compare(text)   # 调用分词库函数，同时判断该微博所含信息是否可用
        print label_e
        # w-天气  c-拥堵  a-事故  s-地铁
        if w == c == a == s == 0:
            k.write(line[7])
            k.write('\n')
            k_count += 1
        elif c != 0 and label_e != '0':
            lc.write(line[7])
            lc.write('\n')
            lc_count += 1
        elif a != 0 and label_e != '0':
            la.write(line[7])
            la.write('\n')
            la_count += 1
        elif s != 0 and label_e != '0':
            ls.write(line[7])
            ls.write('\n')
            ls_count += 1
        elif w != 0 and label_e != '0':
            lw.write(line[7])
            lw.write('\n')
            lw_count += 1
        elif c != 0:
            nlc.write(line[7])
            nlc.write('\n')
            nlc_count += 1
        elif a != 0:
            nla.write(line[7])
            nla.write('\n')
            nla_count += 1
        elif s != 0:
            nls.write(line[7])
            nls.write('\n')
            nls_count += 1
        elif w != 0:
            nlw.write(line[7])
            nlw.write('\n')
            nlw_count += 1

        if label_e in hough[day][hour]:   # 此日此时第一次出现label_e(即新位置)的情况，新建字典
            hough[day][hour][label_e]['w'] += w  # 状态值均已变为float型
            hough[day][hour][label_e]['c'] += c
            hough[day][hour][label_e]['a'] += a
            hough[day][hour][label_e]['s'] += s
        else:
            hough[day][hour][label_e] = {}
            hough[day][hour][label_e]['w'] = w
            hough[day][hour][label_e]['c'] = c
            hough[day][hour][label_e]['a'] = a
            hough[day][hour][label_e]['s'] = s
        count += 1
        if not count % 1000:
            print count

    f.close()
    k.write(str(k_count))
    k.close()
    lw.write(str(lw_count))
    lw.close()
    lc.write(str(lc_count))
    lc.close()
    la.write(str(la_count))
    la.close()
    ls.write(str(ls_count))
    ls.close()
    nlw.write(str(nlw_count))
    nlw.close()
    nlc.write(str(nlc_count))
    nlc.close()
    nla.write(str(nla_count))
    nla.close()
    nls.write(str(nls_count))
    nls.close()

    print 'build_done'
    return hough


# 输出整个四维字典
def push_all(dict, result_path1):
    print 'push_all start'
    w = codecs.open(result_path1, 'a+')  # 要写的文件

    print 'list_location write done'
    for date in dates:  # 天
        if date not in dict.keys():
            continue
        else:
            for hour in dict[date].keys():   # 小时
                for location in dict[date][hour].keys():
                    need_to_write = date + ',' + str(hour) + ',' + location.encode('utf-8') + ',' + str(dict[date][hour][location]['w']) + ',' + str(dict[date][hour][location]['c']) + ',' + str(dict[date][hour][location]['a']) + ',' + str(dict[date][hour][location]['s']) + '\n'
                    w.write(need_to_write)
                    print date
    w.close()
    print 'push_all done'

if __name__ == '__main__':

    dict = build_state_dict('weibo1.txt')
    push_all(dict, 'result_push_all.csv')


