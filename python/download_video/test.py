#coding=utf-8
# teststr = "site:                Bilibili \
# title:               二维动画怎么做 \
# stream:\
#     - format:        flv\
#       container:     flv\
#       size:          14.5 MiB (15205885 bytes)\
#     # download-with: you-get --format=flv [URL]\
# \
# Downloading 二维动画 怎么做.flv ..."

# print(teststr)
# import re

# #文件名
# titlePattern = re.compile('title:\s+(.+?)(?=[\s\r\n])')
# #文件大小
# sizePattern = re.compile('size:\s+([0-9\.]+)\s+MiB')
# #文件名
# namePattern = re.compile('Downloading\s+(.+?)\s+[\.]{3}')  

# title = titlePattern.findall(teststr)
# size = sizePattern.findall(teststr)
# name = namePattern.findall(teststr)
# print('re result is :', title, size, name)


# import datetime
# now = datetime.datetime.now()  #这是时间数组格式
# #转换为指定的格式:
# otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
# print(otherStyleTime)


# import callCMD

# # callCMD.done()

# a = 'E:\python\python36\download_video\file\\'

# import os

# # os.path.split

# import json
# f = open('./1.txt')
# jsonData = json.loads(f.read())
# # print(json.loads(f.read()).get('title'))
# for item in jsonData.get('streams'):
#       print(item, jsonData.get('streams').get(item))



# print(53, jsonData.get('streams'))
# print([1, 2, 3].index(1))


# import SearchFile

# searchFileInstance = SearchFile.SearchFile()
# print(searchFileInstance.findfile('1', 'E:\python\python36\download_video'))

# #获取下载资源的信息
# def getTAG(youGetJSON):
#     #todo 下载资源的优先级
#     #优先下载hd720的资源
#     downORDER = ['hd720', 'quality', 'medium']

#     if None == youGetJSON.get('streams'):
#         print('you-get --json的返回值中没有streams数据项')
#         return None, None

#     orderIndex = len(downORDER)
#     target = None
#     for item in youGetJSON.get('streams'):
#         #找到最靠近前面的值
#         #一旦找到最高的值就退出循环
#         if None == youGetJSON.get('streams').get(item).get('quality'):
#             continue
#         # item.get('quality')
#         try:
#             tmpIndex = downORDER.index(youGetJSON.get('streams').get(item).get('quality'))
#             #冒泡
#             if tmpIndex <= orderIndex:
#                 orderIndex = tmpIndex
#                 target = item
#         except:
#             continue
            
#     #没有找到数据，则选择streams中第一个数据
#     if len(downORDER) == orderIndex:
#         #随机返回一个key,item
#         item = youGetJSON.get('streams').popitem()
#         return item, item.get('container')
#     else:
#         print(downORDER[orderIndex], orderIndex)
#         return orderIndex, youGetJSON.get('streams').get(target).get('container')


# f = open('./1.txt')
# jsonData = json.loads(f.read())
# f.close()

# print(getTAG(jsonData))


# import crawlSubTitle

# a,b = crawlSubTitle.downFile('https://www.youtube.com/watch?v=exMm-fmU5ck')
# print(a, b)


import callCMD
import os
import re
def mergeFile(videoPath, subPath):
    # ./bin/ffmpeg.exe -i 2.mp4 -vf subtitles=2.srt output2.mkv
    videoPathInfo = os.path.split(videoPath)
    targetPath = videoPathInfo[0] + '/MERGE-' + videoPathInfo[1]

    if os.path.exists(targetPath):
        return targetPath
    import platform
    #系统是windows subtitle后面的字符串需要特殊的转义
    if 'Windows' == platform.system():
          # "E:\python\python36\download_video/ffmpeg.exe" -i "E:\python\python36\download_video\file\1.mp4" -vf "subtitles='E\\:\\\\python\\\\python36\\\\download_video\\\\file\\\\1.srt'" "1.mp4"
 
          # "E:\python\python36\download_video/ffmpeg.exe" -i "E:\python\python36\download_video\file\1.mp4" -vf "subtitles='E\\:\\\\python\\\\python36\\\\download_video\\\\file\\\\[DownSub.com] Internet of Things - Why You Need MQTT.srt'" "1.mp4"
          # aSplit = '\\\\\\\\'.join(subPath.split('\\')).split(':')          
          # subPathTmp = aSplit[0] + '\\\\' + ':'
          # for item in aSplit[1:]:
          #     subPathTmp += item
          
          # subPath = subPathTmp

          aSplit = '\\\\\\\\'.join(subPath.split('\\')).split(':')          
          subPathTmp = '\\' + aSplit[0] + '\\' + ':'
          for item in aSplit[1:]:
              subPathTmp += item
          
          subPath = subPathTmp
          
          
    ffmpegResult = callCMD.done('"E:/python/python36/download_video/ffmpeg.exe" -i "' + videoPath + '" -vf "subtitles=\'' + subPath + '\'" "' + targetPath + '"')
 
    #todo 应该return targetPath
    #todo 应该处理ffmpengResult 这个string
    if None == re.match('Error', ffmpegResult):
        #存在就删除
        if None != os.path.exists(targetPath):
            os.remove(targetPath)
        return None
    
    return targetPath


# print(mergeFile('E:\python\python36\download_video\\file\Internet of Things - Why You Need MQTT.mp4'.replace('\\', '/'), 'E:\python\python36\download_video\\file\[DownSub.com] Internet of Things - Why You Need MQTT.srt'.replace('\\', '/')))

# print(mergeFile('E:/python/python36/download_video/file/Internet of Things - Why You Need MQTT.mp4', 'E:/python/python36/download_video/file/[DownSub.com] Internet of Things - Why You Need MQTT.srt'))


#处理路径
# E\\:\\\\python\\\\python36\\\\download_video\\\\file\\\\[DownSub.com] Internet of Things - Why You Need MQTT.srt
# a = 'E:\python\python36\download_video\\file\[DownSub.com] Internet of Things - Why You Need MQTT.srt'

# a = '\\\\\\\\'.join(a.split('\\'))
# aSplit = a.split(':')
# b = aSplit[0] + '\\\\' + ':'
# for item in a.split(':')[1:]:
#     b += item


# print(b)

# a = 'E:\python\python36\download_video\file\Internet of Things - Why You Need MQTT.mp4'
# print(a.replace('\\', '/'))

# import configInfo

# a = configInfo.configInfo()
# print(a.get('ffmpeg', 'position'))



import os 
import time
# os.rename()
counter = 0
# while 1:
    # time.sleep(1)    
    
    # print(counter)
    