#!/usr/bin/python
# -*- coding: utf-8 -*-
import time_standard


def three_dimension_dict(start_date, end_date, hours, state):
    hough = {}             # 建立三维数组
    dates = time_standard.dateRange(start_date, end_date)  # 获取时间的标准表示格式
    for x in dates:   # 每天
        yhough = {}
        for y in xrange(hours):  # 每小时
            rhough = {}
            for r in xrange(state):  # abcdef 6个状态变量 a仍然为天气状态变量
                rhough[r] = 0
            yhough[y] = rhough
        hough[x] = yhough
    return hough