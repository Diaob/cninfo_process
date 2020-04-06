# coding=utf-8
#
# Author: ECNU 虾饺同学
#

import requests
import os
import random
import urllib
import time
import sys

#关键词
keyword = "你的关键词"

#白名单和黑名单（请一定参照格式）
allowed_list = [
]

block_list = [
        '子公司',
        '控股',
        '到期',
        '关联交易',
        '收回',
        '归还',
        '下属公司',
        '参股公司'
]

# 时间区间（请一定参照格式）
rangetime = '2001-01-01+~+2020-04-03'

#若不熟悉Pyhon，以下内容请勿更改==========================================================================

download_path = 'http://static.cninfo.com.cn/'
saving_path = './pdf/'
shcount = 0    #计数，若发现是上海证券交易所的股票超过5次，直接调用上交所而不是深交所数据

User_Agent = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
]


headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
           'Host': 'www.cninfo.com.cn',
           'Origin': 'http://www.cninfo.com.cn',
           'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice',
           'X-Requested-With': 'XMLHttpRequest'
           }


def search(stock):
    query_path = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    headers['User-Agent'] = random.choice(User_Agent)
    
    global shcount
    if shcount < 6:
                query = {'pageNum': 1,
                         'pageSize': 30,
                         'tabName': 'fulltext',
                         'column': 'szse',
                         'stock': stock,
                         'searchkey': keyword,
                         'secid': '',
                         'plate': 'sz',
                         'category': '',
                         'trade': '',
                         'seDate': rangetime
                         }
    else:
                 query = {'pageNum': 1,
                         'pageSize': 30,
                         'tabName': 'fulltext',
                         'column': 'sse',
                         'stock': stock,
                         'searchkey': keyword,
                         'secid': '',
                         'plate': 'sh',
                         'category': '',
                         'trade': '',
                         'seDate': rangetime
                         }
                
    for page in range(1,100):
        try:
            query["pageNum"] = page

            try:
                namelist = requests.post(query_path, headers=headers, data=query)
                report_inform = namelist.json()['announcements']
            except:
                print(stock + ' error')
                
            if len(report_inform) == 0:
                query["column"] = 'sse'
                query["plate"] = 'sh'
                try:
                    namelist = requests.post(query_path, headers=headers, data=query)
                    report_inform = namelist.json()['announcements']
                    if len(report_inform) != 0:
                        shcount += 1
                except:
                    print(stock + ' error')

            if len(report_inform) == 0:
                break
                    
            Download(report_inform)
        except:
            return
        


def Download(req):
    if req is None:
        return

    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
               'Host': 'www.cninfo.com.cn',
               'Origin': 'http://www.cninfo.com.cn'
               }
    
    for i in req:
        title = i['announcementTitle']
        allowed = True

        if len(allowed_list) != 0:
            allowed = title in allowed_list

        if len(block_list) != 0:
            for item in block_list:
                if item in title:
                    allowed = False
                    break
                
        if allowed == False:
            continue
        
        download = download_path + i["adjunctUrl"]
        tmp = str(i['announcementTime'])
        report_time = time.localtime(int(tmp[0:10]))
        announce_time = time.strftime("%y-%m-%d", report_time)
        name = i["secCode"] + '_' + announce_time + '_' + i['secName'] + '_' + i['announcementTitle'] + '.pdf'
        if '*' in name:
            name = name.replace('*', '')

        if ' ' in name:
            name = name.replace(' ','')

        file_path = saving_path + name
        time.sleep(random.random() * 2)

        isExist = os.path.exists(file_path)
        if isExist == False:
            headers['User-Agent'] = random.choice(User_Agent)
            r = requests.get(download)
        else:
            size = os.path.getsize(file_path)
            if size < 15000:
                headers['User-Agent'] = random.choice(User_Agent)
                r = requests.get(download) 


        f = open(file_path, "wb")
        f.write(r.content)
        f.close()

def main(argv):
    with open('company_id.txt') as file:
        lines = file.readlines()
        count = 1
        TotalCount = len(lines)
        for line in lines:
            search(line)
            print(str(line[:6]), end="")
            print(" " + str(count) + "/" + str(TotalCount) + " finished")
            count += 1


if __name__ == "__main__":
    main(sys.argv)
