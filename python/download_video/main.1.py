import handleData
import callCMD
import time
import os
import sys
import re
import datetime
import crawlSubTitle

#
#todo 字幕合成使用如下命令
#./bin/ffmpeg.exe -i 2.mp4 -vf subtitles=2.srt output2.mkv
#todo 错误处理以及LOG
#
downFileDir = sys.path[0] +  '\\file\\'
#在for里面push这个array
updateRows = []
#下载视频使用代理
downVideoProxy = ' -x 127.0.0.1:26362 '
#开始处理数据
#todo 下载字幕以及合并视频文件
def handle(onceLimit):
    #获取数据
    # data = handleData.loadMysqlData(10)
    data = handleData.loadMysqlData(onceLimit)
    if 0 == len(data):
        print('没有找到可以处理的数据')
        return updateRows

    print(data)
    #循环下载
    for item in data:
        print('开始一次循环')
        #开始下载的时间
        startDownDate = getCustomFormatDate()
        #下载视频的返回值
        print('you-get -o ' + downFileDir + downVideoProxy + item[1])
        youGetResult = callCMD.done('you-get -o ' + downFileDir + downVideoProxy + item[1])
        print(youGetResult)
        #判断是否下载成功
        if None == youGetResult or 0 == len(youGetResult.strip()):
            #下载失败
           updateRows.append((startDownDate, '', 2, '', '', '', item[0]))
           print('下载失败1')
           continue
            

        title = getTitle(youGetResult)        
        size = getSize(youGetResult)
        filename = getFileName(youGetResult)

        if None == title or None == size or None == filename :
            #下载失败
           updateRows.append((startDownDate, '', 2, '', '', '', item[0]))
           print('下载失败2')
           continue
            
        print(title, size, filename)
        #判断文件是否存在
        fileIndex = 0
        filePath, subPath = '', ''
        for item1 in filename:
            tmp = downFileDir + item1
            #如果有两个文件，那么第一个文件是视频文件，第二个文件是字幕文件
            if 0 == fileIndex:              
                filePath = tmp
                fileIndex += 1
            elif 1 == fileIndex:                
                subPath = tmp
            if False == os.path.exists(tmp):
                print('下载的文件不存在本磁盘中')
                continue;
            else:            
                print('下载的文件存在')

        #开始下载字幕文件
        downResult, downFile = crawlSubTitle.downFile(item(1))
        print('下载字幕文件的结果是' + str(downResult) + ';文件路径为' + str(downFile))
        #开始处理数据
        if False == downResult:
            downFile = subPath

        #下载完成的时间
        doneDownDate = getCustomFormatDate()
        #updateRows = [('2017-08-29 14:14:00', '2017-08-29 14:14:00', 1, 'asd', 'asd', 'asd', 1)]
        updateRows.append((startDownDate, doneDownDate, 1, filePath, downFile, '', item[0]))

    print('结束一次循环')
    #判断递归
    if len(updateRows) == onceLimit:
        print('开始一次递归')
        handle(onceLimit)
    else:
        print('递归结束')
        return updateRows
        

#文件名
titlePattern = re.compile('title:\s+?(.+?)[\n\r]+?')
def getTitle(yougetResult):    
    title = titlePattern.findall(yougetResult)
    if 1 <= len(title):
        return title[0]        
    return 'title is none'

#文件大小
sizePattern = re.compile('size:\s+([0-9\.]+)\s+MiB')  
def getSize(yougetResult):
    size = sizePattern.findall(yougetResult)
    if 1 <= len(size):
        return size[0]
    return 'size is none'


#文件名
namePattern = re.compile('Downloading\s+(.+?)\s+[\.]{3}')  
#Skipping E:\python\python36\download_video\file\Internet of Things - Why You Need MQTT.mp4: file already exists
namePattern1 = re.compile('Skipping:\s+(.+?)(?=:\s+file\s+already)')
def getFileName(yougetResult):
    name = namePattern.findall(yougetResult)
    if 1 <= len(name):
        return name[0]
    else:
        name = namePattern1.findall(yougetResult)
        if 1 <= len(name):
            return name[0]
    return 'filename is none'

#获取自定义的时间格式
def getCustomFormatDate():
    now = datetime.datetime.now()  
    return now.strftime("%Y-%m-%d %H:%M:%S")


#todo 合并视频和字幕文件
#todo 未测试
def mergeFile(videoPathInfo, subPath):
    # ./bin/ffmpeg.exe -i 2.mp4 -vf subtitles=2.srt output2.mkv
    videoPathInfo = os.path.split(videoPathInfo)
    return callCMD.done(' ./bin/ffmpeg.exe -i ' + videoPathInfo + ' -vf subtitles=' + subPath + ' ' + videoPathInfo[0] + '/MERGE-' + videoPathInfo[1])
# handleResult = handle(10)
# print('handle的返回值', handleResult)

# handleData.updateRows(handleResult)



aaa = "site:                YouTube \
title:               Internet of Things - Why You Need MQTT \
stream:\
    - itag:          22\
      container:     mp4\
      quality:       hd720\
      size:          11.1 MiB (11626286 bytes)\
Downloading Internet of Things - Why You Need MQTT.mp4 ...\
 100% ( 11.1/ 11.1MB) ├███████████████████████████████████████████████\
Saving Internet of Things - Why You Need MQTT.en.srt ... Done."

print(getTitle(aaa))
print(getFileName(aaa))
print(getSize(aaa))







