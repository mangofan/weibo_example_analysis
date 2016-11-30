#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import json
import urllib2
u1 = 'http://api.map.baidu.com/geocoder/v2/?'
u3 = '&output=json&ak=sKPAHLGGycEXip219Wn15v0QWydjyBlv&callback=showLocation'


def choose(source):
    f = codecs.open(source)
    list = []
    w = codecs.open(result_file2, 'w')
    for line in f:  # line格式：地址, 天气，拥堵，事故，地铁
        line = line.strip('\r\n').split(',')
        loc = str(line[0])
        radius = int(line[1])+int(line[2])
        need2 = loc + str(radius) + '\n'
        w.write(need2)  # 输出  地址 数据  格式的文件
        address = '&address=' + loc + '&city=' + u'上海市'
        url = u1 + address + u3
        # 请求经纬度
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()  # 将传回的内容解析出来
        res = res.lstrip('showLocation&&showLocation(').rstrip(')')  # 去掉头尾的部分，形成json
        res = json.loads(res)  # 将json转为字典
        if res['status'] == 0:
            lat = res['result']['location']['lat']
            lng = res['result']['location']['lng']
        else:
            continue
        list.append({"loc": loc, "lat": lat, "lng": lng, "radius": radius, "level": res['result']['level']})
    need1 = json.dumps(list)
    w = codecs.open(result_file1, 'w')
    w.write(need1)


if __name__ == '__main__':
    source_file = 'result_loc_event.csv'
    result_file1 = 'lat_lng_radius1.json'
    result_file2 = 'lat_lng_radius1.txt'
    choose(source_file)