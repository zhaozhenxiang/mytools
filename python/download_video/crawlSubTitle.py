#coding=utf-8
import requests	
from bs4 import BeautifulSoup
import urllib
import re
import sys
import configInfo 
import time

configInfoInstance = configInfo.configInfo()
proxies = {
     "http": configInfoInstance.get('proxy', 'proxy')
}

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }
#downFileDir = sys.path[0] +  '\\file\\'
downFileDir = configInfoInstance.get('download', 'downDIR')

def __getHTML(url):
    # return open('./1.html').read() 
    urlPrefix = 'http://downsub.com/?url='
    if None == configInfoInstance.get('proxy', 'proxy') or 0 == len(configInfoInstance.get('proxy', 'proxy').strip()):
        return requests.get(urlPrefix + url, headers=headers).text
    else:
        return requests.get(urlPrefix + url, headers=headers, proxies=proxies).text


def __getHTML1(url):   
    return open('./1.html').read() 
    req = urllib.request.Request("http://downsub.com/?url=" + url)

    req.add_header("Connection", "keep-alive")
    req.add_header("Cache-Control", "max-age=0")
    req.add_header("Upgrade-Insecure-Requests", "1")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("Referer", "http://downsub.com")
    req.add_header("Accept-Encoding", "gzip, deflate")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8")
    req.add_header("Cookie", "__cfduid=dfcb4eec2f76fbd3c74037981d48416921503996908; _ga=GA1.2.453797912.1504059996; _gid=GA1.2.1549513515.1504059996")

    response = urllib.request.urlopen(req)
    return response[0]



# print(__getHTML('www.youtube.com%2Fwatch%3Fv%3DexMm-fmU5ck'))

#从html的响应中获取下载URL
#todo 此处应该获取到能够获取中文字幕的URL
def __getDownURL(html):
    domain = 'http://downsub.com'
    # rePattern = re.compile('href="(.+?)".+?Simplified')
    #">>>Download<<</a> </b>&nbsp;&nbsp;Chinese
    # sp = BeautifulSoup(html, 'lxml')
    # hrefs = sp.find(attrs={"id":"show"}).find_all('a')
    # print(hrefs, type(hrefs), type(hrefs[0]), hrefs[0].get('href'))

    # for item in hrefs:
    #     # if None == re.match('href="' + item.get('href') + '"[>]+?Download[<]+?\/a>\s+?\<\/b>[&nbsp;]+?Chinese', html):
        
    #     if None == re.match(item.get('href'), html):
    #         print('skip一次href，href为' + item.get('href'))
    #         continue
    #     else:
    #         print('chinses', item.get('href'))
    #         break
            
    # exit()
    rePattern = re.compile('href="(.+?)".{1,60}Chinese')
    
    # print('href', rePattern.findall(html))
    reResult = rePattern.findall(html)
    if 0 == len(reResult):
        return None
    else:
        return domain + reResult[0].strip('.')

#开始下载文件
def downFile(url):
    
    html = __getHTML(url)
    print('字幕列表的HTML页面的字符数为' + str(len(html)))
    if 0 == len(html):
        print('字幕列表页面的HTML字符数为0，这表示没有获取到正常的列表页面。程序将中断')
        return False, None

    fileURL = __getDownURL(html)
    print(fileURL)
    # exit()
    if None == fileURL:
        print('获取的字幕文件地址为空')
        return False, None
    
    #IO处理的函数
    def writeFile(r, fileName):
        #写入文件
        f = open(downFileDir + fileName, "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        
        f.close()
        return downFileDir + fileName

    r = requests.get(fileURL, stream=True)
    #判断是否有该header
    if None == r.headers.get('Content-disposition'):
        print('没有找response的header中找到Content-disposition项。将使用搜索关键字作为下载文件的名称，后缀使用srt')
        return True, writeFile(r, str(int(time.time())) + '.srt')
        
    #attachment; filename="[DownSub.com] Internet of Things - Why You Need MQTT.srt"            
    print(r.headers['Content-disposition'])
    #使用正则获取文件名
    rePattern = re.compile('"(.+?)"')
    fileName = rePattern.findall(r.headers['Content-disposition'])

    if 0 == len(fileName):
        print('没有找response的header中找到文件名称，后缀使用srt')
        fileName = fileURL + '.srt'
    else:
        fileName = fileName[0]
    print('filename is ', fileName)   
    
    print('下载' + fileName + '完成')
    # return True, writeFile(r, fileName)
    
    return True, writeFile(r, str(int(time.time())) + '.srt')

# print(downFile('www.youtube.com%2Fwatch%3Fv%3DexMm-fmU5ck'))



