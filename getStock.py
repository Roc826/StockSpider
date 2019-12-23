import bs4 as bs
import requests#python的http客户端
import pickle#用于序列化反序列化
import re
import json
import time
import os

def GetHuStock():
    url = {
        "sh": "https://www.banban.cn/gupiao/list_sh.html",
        "sz": "https://www.banban.cn/gupiao/list_sz.html",
        "cyb": "https://www.banban.cn/gupiao/list_cyb.html"
    }
    result= {}
    for u in url:
        res = requests.get(url[u])
        res.encoding = res.apparent_encoding
        soup = bs.BeautifulSoup(res.text,'lxml')
        content = soup.find('div',{'class':'u-postcontent cz'})
        for item in content.findAll('a'):
            stock=re.match(r"(\w*)\((\w*)\)",item.text)
            name = stock.group(1)
            result[name]=stock.group(2)
    return result

def DownloadStock(start=20010101,end=20191220):
    stocks = GetHuStock()
    i=0
    for stock in stocks:
        print("正在下载：" + stock, end="")
        params = {
            "code": stocks[stock],
            "start": start,
            "end": end,
            "file": "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        }
        if int(params["code"][0]) in [0, 2, 3, 6, 9]:
            if int(params["code"][0]) in [6, 9]:
                params["code"] = "0" + params["code"]
                type="上证"
            elif int(params["code"][0]) in [0, 2, ]:
                params["code"] = '1' + params["code"]
                type="深证"
            elif int(params["code"][0]) in [3 ]:
                params["code"] = '1' + params["code"]
                type = "创业版"
        else:
            continue
        try:
            res = requests.get("http://quotes.money.163.com/service/chddata.html",params=params)
            path = r"StockDir/"+ type +"/"
            if not os.path.exists(path):
                os.makedirs(path)
            filename = path + stock + "_" + stocks[stock] + ".csv"
            with open(filename,"wb") as file:
                file.write(res.content)
        except BaseException:
            print("\r" + stock + "下载错误")
            continue
        if os.path.isfile(filename):
            print("\r" + stock + "下载成功")
        else:
            print("\r" + stock + "下载失败")
        i += 1
        if i % 3 == 0:
            #time.sleep(3)
            i=0
DownloadStock(20000101,20191220)