# -*- coding: utf-8 -*-

import json
import os
import MySQLdb
import time
import datetime
from dateutil import parser as dp

config_path = "./config/"
datetime_format = '%Y-%m-%d %H:%M:%S'


def grab_area(lat_min, lat_max, lon_min, lon_max):
    '''
    根据输入的坐标范围生成抓取点阵
    :param lat_min:
    :param lat_max:
    :param lon_min:
    :param lon_max:
    :return:
    '''

    area = []
    for i in range(0, 2):
        if i == 1:
            lat_min = lat_min + 0.05
            lon_min = lon_min + 0.05

        lat = lat_min
        while lat < lat_max:
            lon = lon_min
            while lon < lon_max:
                coordinate = (lon, lat)
                area.append(coordinate)
                lon += 0.1
            lat += 0.1

    return area


def grab_area4over():
    '''
    根据输入的坐标范围生成抓取点阵
    :param lat_min:
    :param lat_max:
    :param lon_min:
    :param lon_max:
    :return: {"city_name": "cambridge", "date": "2015-02-12", "count": "-71.100900,42.400300"}
    '''
    dic_list = []
    exc_file = open(config_path + 'overflow.json')
    try:
        exc_list = exc_file.readlines()
        for exc_obj in exc_list:
            grab_dic = {'city_name': '', 'date': '', 'coordinates': ''}
            exc_dic = json.loads(exc_obj)
            lon_max = float(exc_dic["count"].split(',')[0]) + 0.05
            lat_max = float(exc_dic["count"].split(',')[1]) + 0.05
            lon_min = float(exc_dic["count"].split(',')[0]) - 0.05
            lat_min = float(exc_dic["count"].split(',')[1]) - 0.05
            city_name = exc_dic['city_name']
            date = exc_dic['date']
            area = []
            for i in range(0, 2):
                if i == 1:
                    lat_min = lat_min + 0.00625
                    lon_min = lon_min + 0.00625
                lat = lat_min
                while lat < lat_max:
                    lon = lon_min
                    while lon < lon_max:
                        coordinate = (lon, lat)
                        area.append(coordinate)
                        lon += 0.0125
                    lat += 0.0125
            grab_dic['city_name'] = city_name
            grab_dic['date'] = date
            grab_dic['coordinates'] = area
            dic_list.append(grab_dic)
    finally:
        exc_file.close()
    return dic_list


def load_city_area(city_name):
    '''
    加载指定城市的抓取范围
    :param city_name:
    :return:
    '''
    city_file = open(config_path+'city_list.txt')
    city_area = []
    try:
        city_obj_list = city_file.readlines()
        for city_obj in city_obj_list:
            if '\xef\xbb\xbf' in city_obj:
                city_obj = city_obj.replace('\xef\xbb\xbf', '').strip()

            # str_list = city_obj.split(' ')
            str_list = city_obj.strip('\n').split(' ')

            if city_name == str_list[0]:
                print 'str_list: ', str_list
                city_area = grab_area(float(str_list[1]), float(str_list[2]), float(str_list[3]), float(str_list[4]))
                break
    finally:
        city_file.close()

    return city_area


def get_grab_date():
    '''
    从日期配置文件中读取抓取日期
    :return:
    '''

    date_file = open(config_path + 'date_config.json')
    try:
        date_config = date_file.read()
        date_dic = json.loads(date_config)
        startdate = dp.parse(date_dic["start_time"])

        return startdate

    finally:
        date_file.close()






def convert_grab_date(start_time, format_c):
    '''
    将日期字符串转化为对应抓取unix（ISO 8601）时间戳列表
    :param start_time:
    :return:
    '''
    covert_time = []
    if format_c == "unix":
        min_date = time.mktime(time.strptime(start_time, datetime_format))
        covert_time.append(int(min_date))
        day = datetime.datetime.strptime(start_time, datetime_format)
        delta = datetime.timedelta(days=1)
        n_day = day + delta
        max_date = time.mktime(n_day.timetuple())
        covert_time.append(int(max_date))

    elif format_c == "ISO":
        day = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        # 以ISO 8601格式‘YYYY-MM-DD’返回date的字符串形式
        covert_time.append(day.isoformat())
        delta = datetime.timedelta(days=1)
        n_day = day + delta
        covert_time.append(n_day.isoformat())

    return covert_time


def get_grab_time(start_time):
    '''
    将日期字符串转化为对应抓取unix（ISO 8601）时间戳列表
    :param start_time:
    :return:
    '''
    covert_time = []
    day = datetime.datetime.strptime(start_time, datetime_format)
    covert_time.append(day.isoformat())
    for i in range(1, 9):
        delta = datetime.timedelta(hours=3*i)
        n_day = day + delta
        covert_time.append(n_day.isoformat())
    return covert_time


def add_one_day():
    '''
    实现日期配置文件中抓取日期的自动增加
    :return:
    '''
    date_file = open(config_path + 'date_config.json')
    try:
        date_config = date_file.read()
        date_dic = json.loads(date_config)
        str_datetime = json.loads(date_config)["start_time"]
        day = datetime.datetime.strptime(str_datetime, datetime_format)
        delta = datetime.timedelta(days=1)
        next_day = day + delta
        date_dic["start_time"] = next_day.strftime(datetime_format)
    finally:
        date_file.close()

    # w+: 可读可写，若文件不存在，创建，会将原来的文件内容覆盖
    storfile = file(config_path + "date_config.json", "w+")
    storfile.write(json.dumps(date_dic))
    storfile.close()

    return next_day


def sto_photos(images, filename):
    '''
    提取flickr中的photo字段，并保存本地
    :param photos:
    :param filename:
    :return:
    '''
    resultfile = file(filename, "a+")
    #print '写入文件'+ filename
    for image in images:
        # dumps: 将 Python 对象编码成 JSON 字符串
        resultfile.write(json.dumps(image))
        resultfile.write("\n")

    resultfile.close()


def data_statistics(city_name, date, count):
    '''
    统计抓取城市每天的数据获取量
    :param city_name:
    :param date:
    :param count:
    :return:
    '''
    statics = {'city_name':city_name, 'date':date, 'count':count}
    storfile = file(config_path + "mapillary_grab_statistics.json", "a+")
    storfile.write(json.dumps(statics))
    storfile.write("\n")
    storfile.close()


def e_log(city_name, date, coordinate):
    '''
    统计超过1000条数据的区域
    :param city_name:
    :param date:
    :param count:
    :return:
    '''
    logs = {'city_name':city_name, 'date':date, 'coord':coordinate}
    storfile = open(config_path + "overflow.json", "a+")
    storfile.write(json.dumps(logs))
    storfile.write("\n")
    storfile.close()


def failed_download_log(city_name, date, url):
    logs = {'city_name': city_name, 'date':date, 'url': url}
    # storfile = open(config_path + "failed_download_2048.json", "a+")
    path = os.path.join(config_path, city_name+"_failed_download_1024.json")
    storfile = open(path, "a+")
    storfile.write(json.dumps(logs))
    storfile.write("\n")
    storfile.close()




def e_log2 (city_name,date,coordinate):
    '''
    统计超过1000条数据的区域
    :param city_name:
    :param date:
    :param count:
    :return:
    '''
    logs = {'city_name':city_name,'date':date,'coor':coordinate}
    storfile = open(config_path + "overflow2.json", "a+")
    storfile.write(json.dumps(logs))
    storfile.write("\n")
    storfile.close()


def write_config():
    #date = {"Client_ID":"ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy","Client Secret":"MWQ2MWViYjBmZTRlNGJhNmYxZTZhYjI2MjczN2UzMDM="}
    date = {"start_time": "2014-04-01 00:00:00"}
    storfile = file(config_path+"date_config.json", "w+")
    storfile.write(json.dumps(date))
    storfile.close()


# 测试类
if __name__=="__main__":
    #write_config()
    timelist = get_grab_time('2007-01-01 00:00:00')
    for i in range(8):
        print str(timelist[i]) + '  '+str(timelist[i + 1])

    #load_city_area('paris')

    # dic_list = grab_area4over()
    # for dic in dic_list:
    #     print dic["date"]+" 00:00:00"
    #     print '%f'% dic['coordinates'][0][0]





