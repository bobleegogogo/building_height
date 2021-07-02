# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
import urllib, urllib2, datetime, os, json, requests
from dateutil import parser as dp
from utils.grab_utils import *
from utils.mysql_utils import *
from multi_thread import *
import random

MAPILLARY_API_IM_SEARCH_URL = 'https://a.mapillary.com/v3/images?client_id=ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy&'
MAPILLARY_IM_RETRIEVE_URL = 'https://d1cuyjsrcm0gby.cloudfront.net/%s/thumb-1024.jpg'

'''
调用flickr api的search接口，实现flickr的自动抓取
'''
client_id='ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy'

storage_path = "/home/zcq/oliverData/MapillaryData"


def grab_date_data(db, city_name, startdate, enddate, proxies):
    '''
    根据城市名，自动抓取该城市的指定日期的mapillary数据
    :param city_name:
    :param last_days:
    :return:
    '''
    city_coor_list = load_city_area(city_name)

    while startdate <= enddate:
        print u'==============正在抓取日期：%s ==============' % (startdate.strftime('%Y-%m-%d'))

        start_time = startdate.strftime('%Y-%m-%d')
        min_time = convert_grab_date(start_time, 'ISO')[0]
        max_time = convert_grab_date(start_time, 'ISO')[1]
        data_count = 0
        for coor_index in range(len(city_coor_list)):
            coordinate = city_coor_list[coor_index]
            print u'----抓取%s第 %d 区域----'% (city_name, coor_index)
            coordinate = "%f,%f" % (city_coor_list[coor_index][0], city_coor_list[coor_index][1])
            try:
                params = urllib.urlencode(zip(['closeto', 'lookat', 'start_time', 'end_time', 'per_page', 'radius'],
                                              [coordinate, coordinate, min_time, max_time, 1000, 5566]))
                query = urllib2.urlopen(MAPILLARY_API_IM_SEARCH_URL + params).read()
                query = json.loads(query)
                # print 'query2: ', query
                images = query["features"]
                # print 'images: ', images

                if len(images) == 0:
                    print "no data here"

                elif len(images) < 1000:
                    # sto_photos(images, filename)
                    print u'该区域共 %d 条数据' % (len(images))
                    data_count += len(images)

                    res = parsedate(images)
                    sql = "INSERT IGNORE INTO `" + city_name + \
                                 "` (img_key,user_key,username,camera_make,camera_model,ca,lon,lat,pano,captured_at)" \
                                 " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    sql_insert_many(db, sql, res)

                    img_keys = [x[0] for x in res]
                    img_urls = [MAPILLARY_IM_RETRIEVE_URL % key for key in img_keys]

                    download_pic(img_urls, city_name, str(startdate.year), str(startdate.month), startdate.strftime('%Y-%m-%d'), proxies)

                elif len(images) >= 1000:
                    print u'该区域共 %d 条数据' % (len(images))
                    data_count += len(images)

                    num = len(images) / 1000
                    for i in range(num):
                        if i == num - 1:
                            temp = images[i*1000:]
                        else:
                            temp = images[i*1000:(i+1)*1000]

                        res = parsedate(temp)
                        sql = "INSERT IGNORE INTO `" + city_name + \
                              "` (img_key,user_key,username,camera_make,camera_model,ca,lon,lat,pano,captured_at)" \
                              " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                        sql_insert_many(db, sql, res)

                        img_keys = [x[0] for x in res]
                        img_urls = [MAPILLARY_IM_RETRIEVE_URL % key for key in img_keys]

                        download_pic(img_urls, city_name, str(startdate.year), str(startdate.month),
                                     startdate.strftime('%Y-%m-%d'), proxies)

                    # print "count over 1000"
                    # date_log = startdate.strftime('%Y-%m-%d')
                    # e_log(city_name, date_log, coordinate)

            except Exception as e:
                print e

        data_statistics(city_name, startdate.strftime('%Y-%m-%d'), data_count)
        startdate = add_one_day()


def parsedate(images):
    res = []
    for item in images:
        img_key = item['properties']['key']
        user_key = item['properties']['user_key']
        username = item['properties']['username']
        camera_make = item['properties']['camera_make']
        camera_model = item['properties']['camera_model']
        ca = item['properties']['ca']
        lon = item['geometry']['coordinates'][0]
        lat = item['geometry']['coordinates'][1]
        pano = str(item['properties']['pano'])
        captured_at = str(item['properties']['captured_at'])

        record = [img_key, user_key, username, camera_make, camera_model, ca, lon, lat, pano, captured_at]
        res.append(record)

    return res


def download_pic(img_urls, city_name, year, month, date, proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}

    for url in img_urls:
        pic_name = url.split('/')[3] + '.jpg'
        datapath = os.path.join(storage_path, city_name, year, month)

        if os.path.isdir(datapath):
            filename = os.path.join(datapath, pic_name)
        else:
            os.makedirs(datapath)
            filename = os.path.join(datapath, pic_name)

        if os.path.exists(filename):
            print 'already downloaded'
        else:
            print 'downloading %s' % pic_name
            # for i in range(10):

            flag = True
            n = 0
            while flag:
                try:
                    print 'url: ', url
                    # multi thread download, but failed
                    # proxy = random.choice(proxies)
                    # downloader = Downloader(url, filename, proxy)
                    # downloader.run()

                    img = requests.get(url, headers=headers, proxies=random.choice(proxies), timeout=5)
                    f = open(filename, "wb")
                    f.write(img.content)
                    f.close()
                    flag = False
                    n = 0

                except requests.exceptions.Timeout:
                    # if getting no response within 10s, log the url and re-download it latter
                    print 'requests Timeout'
                    if n < 2:
                        n += 1
                        time.sleep(0.5)
                    else:
                        failed_download_log(city_name, date, url)
                        time.sleep(0.5)
                        break

                except Exception, e:
                    print(e.message)
                    if n >= 3:
                        failed_download_log(city_name, date, url)
                    else:
                        n += 1
                        time.sleep(0.5)
                    time.sleep(0.5)

                else:
                    time.sleep(0.1)
                    # break


def grab_over_data():
    '''
    补全超过1000区域的数据
    :param city_name:
    :param last_days:
    :return:
    '''
    exc_list = grab_area4over()
    err_num = 0
    for exc_obj in exc_list:
        city_name = exc_obj['city_name']
        year = exc_obj["date"].split('-')[0]
        month = exc_obj["date"].split('-')[1]
        print(u'==============正在抓取日期：%s ==============' % (exc_obj["date"]))
        datapath =  os.path.join(storage_path, year, month)
        if os.path.isdir(datapath):
            filename =os.path.join(datapath ,city_name + '.txt')
        else:
            os.makedirs(datapath)
            filename = os.path.join(datapath, city_name + '.txt')
        start_time = exc_obj["date"] + ' 00:00:00'
        min_time = convert_grab_date(start_time,'ISO')[0]
        max_time =  convert_grab_date(start_time,'ISO')[1]
        data_count = 0
        coordinates = exc_obj['coordinates']
        for coordinate in coordinates:
            print(u'----抓取%s第 %s 区域----'% (city_name,coordinate))
            coordinate = "%f,%f" %(coordinate[0],coordinate[1])
            try:

                params = urllib.urlencode(zip(['closeto', 'lookat', 'start_time', 'end_time', 'per_page', 'radius'],
                                                  [coordinate, coordinate, min_time, max_time, 1000, 696]))
                query = urllib2.urlopen(MAPILLARY_API_IM_SEARCH_URL + params).read()
                query = json.loads(query)
                images = query["features"]
                if len(images) >= 1000:
                    print "count over 1000"
                    e_log2(city_name,exc_obj["date"],coordinate)
                    sto_photos(images, filename)
                elif len(images)==0:
                    print "no data here"
                else :
                    sto_photos(images,filename)
                    print u'该区域共 %d 条数据' % (len(images))
                    data_count += len(images)
            except Exception as e:
                print e


if __name__ == "__main__":
    #create_db('mapillary')
    
    db = connect_db('mapillary')

    '''
    table_name = 'Berlin'
    sql = "CREATE TABLE IF NOT EXISTS `" + table_name + "` (`img_key` varchar(22) CHARACTER SET utf8 Not NULL, " \
                                                "`user_key` varchar(22) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`username` varchar(50) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`camera_make` varchar(70) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`camera_model` varchar(70) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`ca` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`lon` varchar(20) CHARACTER SET utf8 DEFAULT NULL, " \
                                                "`lat` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`pano` varchar(5) CHARACTER SET utf8 DEFAULT NULL, " \
                                                "`captured_at` varchar(24) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "PRIMARY KEY (`img_key`)) ENGINE=InnoDB DEFAULT CHARSET= utf8"
    creat_table(db, sql)
    '''


    city_name = 'Berlin'
    startdate = get_grab_date()
    enddate = dp.parse("2014-12-31 23:59:59")

    fp = open('proxy/host.txt', 'r')
    ips = fp.readlines()
    proxies = []
    for ip in ips:
        ip = ip.strip('\n').split('\t')
        proxy = 'http://' + ip[0] + ':' + ip[1]
        proxies.append({'proxy': proxy})

    grab_date_data(db, city_name, startdate, enddate, proxies)

