#coding=utf-8
import handleData
import callCMD
import time
import os
import sys
import re
import datetime
import crawlSubTitle
import SearchFile
import json
import configInfo

#
#todo 字幕合成使用如下命令
#./bin/ffmpeg.exe -i 2.mp4 -vf subtitles=2.srt output2.mkv
#todo 错误处理以及LOG
#todo 配置文件管理配置
#

configInfoInstance = configInfo.configInfo()
#downFileDir = sys.path[0] +  '\\file\\'
downFileDir = configInfoInstance.get('download', 'downDIR')
#在for里面push这个array
updateRows = []
#下载视频使用代理
# downVideoProxy = ' -x 127.0.0.1:1080 '
downVideoProxy = configInfoInstance.get('proxy', 'proxy')
if None == downVideoProxy or 0 == len(downVideoProxy.strip()):
    downVideoProxy = ' '
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
        print('开始一次循环=========')
        #开始下载的时间
        startDownDate = getCustomFormatDate()
        #获取视频的json数据
        print('you-get --json' + downVideoProxy + item[1])
        #         {
        #     "site": "YouTube",
        #     "streams": {
        #         "17": {
        #             "container": "3gp",
        #             "itag": "17",
        #             "mime": "video/3gpp",
        #             "quality": "small",
        #             "s": null,
        #             "sig": null,
        #             "type": "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
        #             "url": "https://r12---sn-oguesnss.googlevideo.com/videoplayback?key=yt6&gir=yes&mime=video%2F3gpp&requiressl=yes&initcwndbps=5773750&signature=5AC9E57050F10B70DC2B5D674A77B713EE51B5ED.18F764A288CC11C1B988F4B2409BFF9BD3EAD469&lmt=1406334932623128&expire=1504105863&dur=281.890&ipbits=0&source=youtube&itag=17&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&clen=1300088&mn=sn-oguesnss&mm=31&id=7b1326f9f994e5c9"
        #         },
        #         "18": {
        #             "container": "mp4",
        #             "itag": "18",
        #             "mime": "video/mp4",
        #             "quality": "medium",
        #             "s": null,
        #             "sig": null,
        #             "type": "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
        #             "url": "https://r12---sn-oguesnss.googlevideo.com/videoplayback?key=yt6&gir=yes&mime=video%2Fmp4&requiressl=yes&initcwndbps=5773750&ratebypass=yes&signature=D8388333DBAA6C89B0B2FE4CFBB504699A0546F7.6229497B361C5953E781DBC8D25EC0CCFEE0CC31&lmt=1420816844642387&expire=1504105863&dur=281.704&ipbits=0&source=youtube&itag=18&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&clen=6535017&mn=sn-oguesnss&mm=31&id=7b1326f9f994e5c9"
        #         },
        #         "22": {
        #             "container": "mp4",
        #             "itag": "22",
        #             "mime": "video/mp4",
        #             "quality": "hd720",
        #             "s": null,
        #             "sig": null,
        #             "size": 11626286,
        #             "src": [
        #                 "https://r12---sn-oguesnss.googlevideo.com/videoplayback?source=youtube&key=yt6&mime=video%2Fmp4&requiressl=yes&dur=281.704&initcwndbps=5773750&ratebypass=yes&signature=ADD3BF91F3F139E2DED0999CDF894E32F5BC690F.041305CD45E17FB3ACCA9628D084B955D18B35EE&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=dur%2Cei%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&lmt=1471160705716952&expire=1504105863&mn=sn-oguesnss&itag=22&ipbits=0&mm=31&id=7b1326f9f994e5c9"
        #             ],
        #             "type": "video/mp4; codecs=\"avc1.64001F, mp4a.40.2\"",
        #             "url": "https://r12---sn-oguesnss.googlevideo.com/videoplayback?source=youtube&key=yt6&mime=video%2Fmp4&requiressl=yes&dur=281.704&initcwndbps=5773750&ratebypass=yes&signature=ADD3BF91F3F139E2DED0999CDF894E32F5BC690F.041305CD45E17FB3ACCA9628D084B955D18B35EE&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=dur%2Cei%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&lmt=1471160705716952&expire=1504105863&mn=sn-oguesnss&itag=22&ipbits=0&mm=31&id=7b1326f9f994e5c9"
        #         },
        #         "36": {
        #             "container": "3gp",
        #             "itag": "36",
        #             "mime": "video/3gpp",
        #             "quality": "small",
        #             "s": null,
        #             "sig": null,
        #             "type": "video/3gpp; codecs=\"mp4v.20.3, mp4a.40.2\"",
        #             "url": "https://r12---sn-oguesnss.googlevideo.com/videoplayback?key=yt6&gir=yes&mime=video%2F3gpp&requiressl=yes&initcwndbps=5773750&signature=05B35F4BE357FADABDBDF8E1407B2D6E405EECFF.D43458551095F5025519447B6DE48D96F6E082F6&lmt=1406334956704455&expire=1504105863&dur=281.843&ipbits=0&source=youtube&itag=36&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&clen=3276701&mn=sn-oguesnss&mm=31&id=7b1326f9f994e5c9"
        #         },
        #         "43": {
        #             "container": "webm",
        #             "itag": "43",
        #             "mime": "video/webm",
        #             "quality": "medium",
        #             "s": null,
        #             "sig": null,
        #             "type": "video/webm; codecs=\"vp8.0, vorbis\"",
        #             "url": "https://r12---sn-oguesnss.googlevideo.com/videoplayback?key=yt6&gir=yes&mime=video%2Fwebm&requiressl=yes&initcwndbps=5773750&ratebypass=yes&signature=3B6C88F7F641FD760AFE586D06D23305814A0CB3.36548A034E0E6FBD7B2DFF56FEA309ED3F7FF2CE&lmt=1406338609073393&expire=1504105863&dur=0.000&ipbits=0&source=youtube&itag=43&ei=J4GmWdLFKdjSqAH8o4PADw&pl=19&mv=m&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cexpire&mt=1504084060&ms=au&ip=45.32.37.194&clen=6751968&mn=sn-oguesnss&mm=31&id=7b1326f9f994e5c9"
        #         }
        #     },
        #     "title": "Internet of Things - Why You Need MQTT",
        #     "url": "http://www.youtube.com/watch?v=exMm-fmU5ck"
        # }
        downJSONCMD = 'you-get --json' + downVideoProxy + item[1]
        print('开始下载' + downJSONCMD)
        youGetJSONString = callCMD.done(downJSONCMD)        
        print(downJSONCMD + '的返回值为' + youGetJSONString)
        try:
            youGetJSON = json.loads(youGetJSONString)
        except:
            print(downJSONCMD + '的返回值的json格式化失败')
            youGetJSON = {}
        


        title = youGetJSON.get('title')
        if None == title:
            print('没有获取到资源的title')
            updateRows.append((startDownDate, getCustomFormatDate(), 2, '', '', '', item[0]))
            continue

        #获取下载资源的信息
        def getTAG(youGetJSON):
            #todo 下载资源的优先级
            #优先下载hd720的资源
            downORDER = ['hd720', 'quality', 'medium']
        
            if None == youGetJSON.get('streams'):
                print('you-get --json的返回值中没有streams数据项')
                return None, None

            orderIndex = len(downORDER)
            target = None
            for item in youGetJSON.get('streams'):
                #找到最靠近前面的值
                #一旦找到最高的值就退出循环
                if None == youGetJSON.get('streams').get(item).get('quality'):
                    continue
                # item.get('quality')
                try:
                    tmpIndex = downORDER.index(youGetJSON.get('streams').get(item).get('quality'))
                    #冒泡
                    if tmpIndex <= orderIndex:
                        orderIndex = tmpIndex
                        target = item
                except:
                    continue
                    
            #没有找到数据，则选择streams中第一个数据
            if len(downORDER) == orderIndex:
                #随机返回一个key,item
                item = youGetJSON.get('streams').popitem()
                return item, item.get('container')
            else:
                return target, youGetJSON.get('streams').get(target).get('container')

        
        targetTag, targetVideoFormat = getTAG(youGetJSON)
        if None == targetTag:
            updateRows.append((startDownDate, getCustomFormatDate(), 2, '', '', '', item[0]))
            # print('')
            continue
        # 不需要size
        # title = getTitle(youGetResult)        
        # size = getSize(youGetResult)
        # filename = getFileName(youGetResult)
        
        filename = title + '.' + targetVideoFormat

        #todo 这里判断视频是否下载过了
        print(downFileDir + filename, os.path.exists(downFileDir + filename))
        
        if True == os.path.exists(downFileDir + filename):
            print('想要下载的视频已存在')
            youGetResult = 'True'
        else:
            #下载视频的返回值
            downCMD = 'you-get -o ' + downFileDir + ' -F ' + str(targetTag) +  downVideoProxy + item[1]
            print('开始下载视频文件' + downCMD)
            youGetResult = callCMD.done(downCMD)
            
            print('下载视频的返回值:' + youGetResult)

        #判断是否下载成功
        if None == youGetResult or 0 == len(youGetResult.strip()):
            #下载失败
           updateRows.append((startDownDate, getCustomFormatDate(), 2, '', '', '', item[0]))
           print('下载失败1')
           continue         


        # if None == title or None == filename :
        #     #下载失败
        #    updateRows.append((startDownDate, '', 2, '', '', '', item[0]))
        #    print('下载失败2')
        #    continue
            
        print(title, filename)
        #判断文件是否存在
        if False == os.path.exists(downFileDir + filename):
            print('下载的视频文件不存在本磁盘中')
            updateRows.append((startDownDate, getCustomFormatDate(), 2, '', '', '', item[0]))
            continue;
   
        #下载字幕文件
        def downSUBFile(url):
            print('you-get没有下载成功中文字幕')
            #开始下载字幕文件
            print('将使用crawlSubTitle来下载字幕文件')
            #第二选择爬虫下载的中文字幕                
            crawlDownResult, crawlDownFile = crawlSubTitle.downFile(url)
            # crawlDownResult, crawlDownFile = False, None
            print('下载字幕文件的结果是' + str(crawlDownResult) + ';文件路径为' + str(crawlDownFile))
            #开始处理数据
            if True == crawlDownResult:
                subTitlePath = crawlDownFile
            else:
                subTitlePath = None
            return subTitlePath
        #视频文件可以直接根据文件名来判断，但是字幕文件的文件名称不确定（可能下载0或多个字幕文件）                
        searchFileInstance = SearchFile.SearchFile()
        searchFileResult = searchFileInstance.findfile(title, downFileDir)
        #字幕文件地址
        subTitlePath = ''
        #多余一个说明下载字幕文件成功了,直接找到.zh-CN.srt结尾的文件
        if 1 < len(searchFileResult):
            #第一选择youtube下载的中文字幕，很少时候会下载成功
            #zh-CN.srt => 简体中文
            #zh-Hans.srt => 简体中文
            #zh-Hant.srt =>繁体中文
            #zh-TW.srt => 繁体中文
            #todo 目前没有处理繁体中文
            if True == os.path.exists(downFileDir + title + '.zh-Hans.srt'):
                subTitlePath = downFileDir + title + '.zh-Hans.rst'              
            elif True == os.path.exists(downFileDir + title + '.zh-CN.srt'):
                subTitlePath = downFileDir + title + '.zh-CN.rst'
            elif True == os.path.exists(downFileDir + title + '.zh-HantCN.srt'):
                subTitlePath = downFileDir + title + '.zh-Hant.rst'
            elif True == os.path.exists(downFileDir + title + '.zh-TWCN.srt'):
                subTitlePath = downFileDir + title + '.zh-TW.rst'
            else:
                subTitlePath = downSUBFile(item[1])
                #第三选择youtube下载的英文字幕                
                if None == subTitlePath:
                    if True == os.path.exists(downFileDir + title + '.en.srt'):
                        subTitlePath = downFileDir + title + '.en.srt'
                    else:
                        subTitlePath = None
        #下载的文件最多只有一个即最多只下载了一个视频文件
        else:
            subTitlePath = downSUBFile(item[1])
            
        try:
            subTitlePath1 = downFileDir + str(int(time.time())) + '.srt'
            os.rename(subTitlePath, subTitlePath1)
            subTitlePath = subTitlePath1
        except:
            print('os.rename srt 文件失败')
            subTitlePath = None
        #下载完成的时间
        doneDownDate = getCustomFormatDate()
        #todo 这里需要需要合并视频文件
        if None == subTitlePath:
            videoMergeFile = downFileDir + filename
            subTitlePath = ''
        else:
            videoMergeFile = mergeFile(downFileDir + filename, subTitlePath)
        if None == videoMergeFile:
            videoMergeFile = ''
        #updateRows = [('2017-08-29 14:14:00', '2017-08-29 14:14:00', 1, 'asd', 'asd', 'asd', 1)]
        updateRows.append((startDownDate, doneDownDate, 1, downFileDir + filename, subTitlePath, videoMergeFile, item[0]))
    print('结束一次循环=========')
    #判断递归
    if len(updateRows) == onceLimit:
        print('开始一次递归=========')
        handle(onceLimit)
    else:
        print('递归结束=========')
        return updateRows
        



def getTitle(yougetResult): 
    #文件名
    titlePattern = re.compile('title:\s+?(.+?)[\n\r]+?')   
    title = titlePattern.findall(yougetResult)
    if 1 <= len(title):
        return title[0]        
    return 'title is none'



def getSize(yougetResult):
    #文件大小
    sizePattern = re.compile('size:\s+([0-9\.]+)\s+MiB')  
    size = sizePattern.findall(yougetResult)
    if 1 <= len(size):
        return size[0]
    return 'size is none'



def getFileName(yougetResult):
    #文件名
    namePattern = re.compile('Downloading\s+(.+?)\s+[\.]{3}')  
    #Skipping E:\python\python36\download_video\file\Internet of Things - Why You Need MQTT.mp4: file already exists
    namePattern1 = re.compile('Skipping:\s+(.+?)(?=:\s+file\s+already)')    
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
def mergeFile(videoPath, subPath):
    # ./bin/ffmpeg.exe -i 2.mp4 -vf subtitles=2.srt output2.mkv
    videoPath = videoPath.replace('\\', '/')
    subPath = subPath.replace('\\', '/')
    
    videoPathInfo = os.path.split(videoPath)
    # targetPath = videoPathInfo[0] + '/MERGE-' + videoPathInfo[1]     
    targetPath = videoPathInfo[0] + '/MERGE-' + str(int(time.time())) + os.path.splitext(videoPath)[1]

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
          
          
    # ffmpegResult = callCMD.done('"E:/python/python36/download_video/ffmpeg.exe" -i "' + videoPath + '" -vf "subtitles=\'' + subPath + '\'" "' + targetPath + '"')
    ffmpegResult = callCMD.done('"' + configInfoInstance.get('ffmpeg', 'position') + '" -i "' + videoPath + '" -vf "subtitles=\'' + subPath + '\'" "' + targetPath + '"')
 
    #ffmpegResult
    print(ffmpegResult)
    #todo 应该return targetPath
    #todo 应该处理ffmpengResult 这个string
    # if None == re.match('Error', ffmpegResult):
    #     #存在就删除
    #     if None != os.path.exists(targetPath):
    #         os.remove(targetPath)
    #     return None
    
    return targetPath



while 1:
    handleResult = handle(10)
    print('handle的返回值', handleResult)
    handleData.updateRows(handleResult)
    time.sleep(300)
    print('now date is' +  getCustomFormatDate())




