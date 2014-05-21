#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 20, 2014

@author: seny
'''
from pytesser.pytesser import image_to_string
import Image
import cStringIO
import cookielib
import re
import time
import urllib
import urllib2
import datetime

class BJRCW:
    # like browser
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'}
    cookie = None  # cookie obj
    cookiefile = './cookies.dat'  # cookie file

    def __init__(self):
        self.cookie = cookielib.LWPCookieJar()  # save cookies obj
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)

    def get_home_page_company_url(self):
        print '正在爬首页～～～～～～～'
        base_url = "http://bj.597rcw.com"
        uid_url = urllib2.Request(
               url=(base_url),
               headers=self.header
        )
        auth = urllib2.urlopen(uid_url).read()
        result = str(auth)
        #匹配 all company url
        h_urls= re.findall('/Company/Info/Com_View_VR\d*.html', result, re.S)
        print '在首页爬了',len(h_urls),'个公司信息～～～～～'
        return h_urls
    
    def get_search_page_company_url(self, pageNo):
        print '正在爬搜索页面第',pageNo,'页～～～～'
        base_url = "http://bj.597rcw.com/Person/Per_Search_Quick.shtml?"
        query_param = urllib.urlencode({'PageNo':pageNo,'PCount':'20','Psize':'100'})
        uid_url = urllib2.Request(
               url=(base_url + query_param),
               headers=self.header
           )
        auth = urllib2.urlopen(uid_url).read()
        result = str(auth)
        # re.S是任意匹配模式，也就是.可以匹配换行符
        s_urls= re.findall('/Company/Info/Com_View_VR\d*.html', result, re.S)
        print '爬了',len(s_urls),'个公司信息～～～～～'
        return s_urls

    def get_all_company_url(self):
        #爬取首页所有公司url
        h_urls=list(set(self.get_home_page_company_url()))
        s_urls=[]
        for x in range(1,21):
            #获取搜索页面最新20*100条公司url
            try:
                s_urls+=list(set(self.get_search_page_company_url(x)))
            except urllib2.URLError as e:
                print e
                time.sleep(2)
        return h_urls+s_urls

    def access_company_url(self,company_url):
        base_url ='http://bj.597rcw.com'
        page = urllib2.urlopen(base_url+company_url).read().decode("gbk")
        number_urls=re.findall('/AspNet/StrToImg.ashx.+?/>', page, re.S)
        if len(number_urls)!=0:
            #'<td><b>北京中泰安瑞科技发展有限公司</b></td>"' 截取
            commpany_name=re.findall('<td><b>.+?</b></td>', page, re.S)[0][7:-9]
            #<td height="25" width="85%">饶经理</td>
            contacts_name=re.findall('<td height="25" width="85%">.+?</td>', page, re.S)[0][28:-5]
            #<img src="/AspNet/StrToImg.ashx?type=code&amp;email=p7JDp9Jzqo3AaSHCR4ySUg%3D%3D">
            number_url=number_urls[0][:-4]
            #把号码图片转换为文本
            img = Image.open(cStringIO.StringIO(urllib2.urlopen(base_url+number_url).read()))
            number = image_to_string(img)
            return commpany_name+","+contacts_name+","+number
        else:
            return ''

        

print '~~~~~~~~~~~~~~~~~~~~~~~爬虫出发～～～～～～～～～～～～～～～'
print '开始时间:',datetime.datetime.now()
f = open('hr.txt','w')
obj=BJRCW()
urls=obj.get_all_company_url()
for i in range(len(urls)):
    try:
        info=obj.access_company_url(urls[i])
        if info!='':
            f.write(info)
            f.flush()
    except urllib2.URLError as e:
            #请求频繁的异常处理
            print urls[i],e
            time.sleep(2)
f.close()
print '结束时间:',datetime.datetime.now()
