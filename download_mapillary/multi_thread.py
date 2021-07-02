#coding:utf-8

import requests
import threading, random

lock = threading.RLock()


class Downloader:
    def __init__(self, url, filename, proxy):
        self.url = url
        self.num = 8
        self.filename = filename
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        # print 'total is %s' % (self.total)
        self.proxy = proxy

    def get_range(self):
        ranges = []
        offset = int(self.total/self.num)
        for i in range(self.num):
            if i == self.num-1:
                ranges.append((i*offset, ''))
            else:
                ranges.append((i*offset, (i+1)*offset))
        return ranges

    def download(self, start, end):
        # 拼接Range字段,accept字段支持所有编码
        headers = {'Range':'Bytes=%s-%s' % (start, end), 'Accept-Encoding':'*'}
        res = requests.get(self.url, headers=headers, proxies=self.proxy, timeout=5)
        # print '%s:%s download success' % (start, end)

        # seek到start位置
        with lock:
            self.fd.seek(start)
            self.fd.write(res.content)



    def run(self):
        self.fd = open(self.filename, 'w')
        thread_list = []
        # 一个数字,用来标记打印每个线程
        n = 0
        for ran in self.get_range():
            start, end = ran
            # print 'thread %d start:%s,end:%s' % (n, start, end)
            n += 1
            # 创建线程 传参,处理函数为download
            thread = threading.Thread(target=self.download, args=(start, end))
            # 启动
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待
            i.join()

        # print 'download %s load success'%(self.name)
        self.fd.close()


if __name__=='__main__':
    url = 'https://d1cuyjsrcm0gby.cloudfront.net/aCQuU_MsVgbnMJYJJVIlow/thumb-2048.jpg'
    filename = '/home/wlw/oliverProjects/VGI-flickr/aCQuU_MsVgbnMJYJJVIlow.jpg'
    down = Downloader(url, filename)
    down.run()