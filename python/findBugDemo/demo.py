#!/usr/bin/python
# coding:utf8
# -*- coding: utf-8 -*-
import os
import re
import sys
import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import copy
import sqlite3
import platform

reload(sys)
sys.setdefaultencoding('utf8')
class analyze(object):
    #初始化数据
    __configParseinstance = None
    __mailHandler = None
    __historyInfo = None
    __content = ''
    __sqlite = "log.db"


    def __init__(self):
        self.__init_param(self)

    #析构函数
    def __del__(self):
        #退出mail(类似于消耗该对象吧)
        #self.__get_mail_handler().quit()
	1
    #初始化参数
    def __init_param(self, obj):
        self.__dir = os.path.dirname(__file__)
        configPaser = self.get_configparse()
        self.__sender = configPaser.get('mail', 'sender')
        self.__receiver = configPaser.get('mail', 'receiver').split(',')
        self.__smtp = configPaser.get('mail', 'server')
        self.__smtpUser = configPaser.get('mail', 'user')
        self.__smtpUserPass = configPaser.get('mail', 'passwd')
        self.__subject = configPaser.get('mail', 'subject')
        #list(列表中有元组) [('file1', '/1.txt,/2.txt,/3.txt'), ('match1', "'123'"), ('file2', '/4.txt'), ('match2', "'4'")]
        self.__file = configPaser.items('file')
        self.__path = configPaser.items('path')
        self.__ishistory = configPaser.get('writeHistory', 'writeHistory')
        self.__fileMaxSize = int(self.__count_memory_size() / self.__count_cpu() * 0.5 * 1024 * 1024)

    #内存大小
    def __count_memory_size(self):
        if ('Windows' == platform.system()):
            print '请输入您的服务器的内存大小MB:'.decode('utf-8')
            memory = raw_input()
            if '' == memory or 0 > int(memory):
                return 100 * 1024 * 1024
            return int(memory) * 1024 * 1024
        return int(os.popen("free -m|awk  '{print $2}'|sed -n '2p'").readline().strip())
    #cpu数目
    def __count_cpu(self):
        if ('Windows' == platform.system()):
            return 1
        file = open('/proc/cpuinfo')
        cpu_sum = []
        for line in file.readlines():
            cpu_he = re.findall('^processor', line)
            if len(cpu_he) == 1:
                cpu_sum.append(cpu_he)
            else:
                continue
        file.close()
        return len(cpu_sum)
    #去读json文件中内容转成dict
    #idea 该文件一般都很小 不需要去专门去读取
    def __processJson(self, inputJsonFile):
        fin = open(inputJsonFile, 'r')
        str = ''
        for eachLine in fin:
            str += eachLine.strip().decode('utf-8')  # 去除每行首位可能的空格，并且转为Unicode进行处理
        fin.close()
        # 关闭文件
        return json.loads(str)

    #解析conf文件
    def get_configparse(self):
        if (None == analyze.__configParseinstance):
            config = ConfigParser.ConfigParser()
            config.read(os.path.join(self.__dir, "./config.conf"))
            analyze.__configParseinstance = config

        return analyze.__configParseinstance

    def __get_history_info(self, pathList):
        #@todo 获取history信息是否也要放在这里
        #获取history信息
        #只获取一次,类似于单例模式
        if None == analyze.__historyInfo:
            # analyze.__historyInfo = self.__processJson(self.__dir + 'history.json')
            analyze.__historyInfo = self.__readDB(pathList)
            self.__history = copy.deepcopy(analyze.__historyInfo)

        return analyze.__historyInfo

    #读取sqlite
    def __readDB(self, pathList):
        # 连接数据库
        try:
            sqlite_conn = sqlite3.connect(analyze.__sqlite)
        except sqlite3.Error, e:
            print "连接sqlite3数据库失败".decode('utf-8'), "\n", e.args[0]
            return

        # 获取游标
        sqlite_cursor = sqlite_conn.cursor()
        def createTable():
            # 创建表
            sql_add = '''CREATE TABLE IF NOT EXISTS file_log(
                file VARCHAR(255) PRIMARY KEY,
                num  INTEGER,
                modified INTEGER DEFAULT 0
                );'''
            try:
                sqlite_cursor.execute(sql_add)
            except sqlite3.Error, e:
                print "创建数据库表失败！".decode('utf-8'), "\n", e.args[0]
                return
            sqlite_conn.commit()
        # 检查是否存在不存在该创建
        sql_exists = "select count(*)  from sqlite_master where type='table' and name = 'file_log';"
        try:
            result = sqlite_cursor.execute(sql_exists)
            if (0 == result.fetchone()[0]):
                createTable()
                pathList1 = []
                for o in pathList:
                    pathList1.append(tuple(o.values()))
                del pathList
                return pathList1;
        except sqlite3.Error, e:
            print "检查数据库表失败！".decode('utf-8'), "\n", e.args[0]
            return
        sqlite_conn.commit()
        sql_in = ''
        for o in pathList:
            sql_in += "'" + o.get('file') + "',"

        #读取数据库
        sql_in = sql_in.strip(',')
        sql_select="SELECT * FROM file_log where file in (" + sql_in +");"
        sqlite_cursor.execute(sql_select)
        #list包裹元组类似于[(u'/1.txt', 1222, 2222), (u'/4.txt', 1222, 2222), (u'/123.txt', 1222, 2222)]
        dbList = sqlite_cursor.fetchall()
        sqlite_cursor.close()

        return dbList
        for o in dbList:
            #获取名字
            file = o[0]
            for o1 in pathList:
                if (file == o1.get('file')):
                    o1['number'] = o[1]
                    o1['modified'] = o[2]

        return pathList
    #获取mail的发送实例类
    def __get_mail_handler(self):
	print analyze
        if (None == analyze.__mailHandler):
            smtp = smtplib.SMTP()
            smtp.connect(self.__smtp)
            smtp.login(self.__smtpUser, self.__smtpUserPass)
            analyze.__mailHandler = smtp
	    print '__get_mail_handler'
            # smtp.sendmail(sender, receiver, msgRoot.as_string())
            # smtp.quit()
        return analyze.__mailHandler

    #发送邮件
    #发送内容最好有匹配到的信息或者文件名和行号的组合
    def __send_mail(self, content):
        mail = self.__get_mail_handler()
        #设置邮件内容
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.__subject
        msgRoot['From'] = self.__sender
        msgRoot['To'] = ",".join(self.__receiver)
        msgText = MIMEText(content, 'plain', 'utf-8')
        msgRoot.attach(msgText)
        #发送邮件
        mail.sendmail(self.__sender, self.__receiver, msgRoot.as_string())
        # mail.quit()

    #返回更新文件和行号和match
    def __load_files(self):

        #遍历path信息
        pathDict = dict(self.__path)
        pathFiled = ('path', 'isrecursive', 'match')
        currentList = []
        fileList = []
        for o in pathDict:
            current = self.__get_num_by_str(o)
            #检查是否存在该值
            if current not in currentList:
                #写入list标识该值已经处理过
                currentList.append(current)
                #判断是否是递归获取该文件夹下文件
                currentIsrecursive = pathDict.get(pathFiled[1] + current) == '1'
                #push进入列表
                # fileList.extend(self.__walk_dir(pathDict.get(pathFiled[0] + current), isrecursive = currentIsrecursive))
                #当前文件
                currentFile = self.__walk_dir(pathDict.get(pathFiled[0] + current), isrecursive = currentIsrecursive)
                #遍历
                for currentFileItem in currentFile:
                    fileList.append({'file':currentFileItem, 'match':pathDict.get(pathFiled[2] + current), 'number':0})

        #遍历file信息
        fileDict = dict(self.__file)
        currentList = []
        for o in fileDict:
            current = self.__get_num_by_str(o)
            if current not in currentList:
                # 写入list标识该值已经处理过
                currentList.append(current)
                #临时变量
                fileListVal = fileDict.get(o);
                fileList.append({'file':fileListVal, 'match':fileDict.get(pathFiled[2] + current), 'number':0})
        # 读取DB中的历史记录
        hisrotyList = self.__get_history_info(fileList)
        for o in hisrotyList:
            # 获取名字
            file = o[0]
            for o1 in fileList:
                if (file == o1.get('file')):
                    o1['number'] = o[1]
                    o1['modified'] = o[2]

        return fileList

    #获取一个dir下面的全部文件,默认递归获取
    def __walk_dir(self, dir, isrecursive=True):
        fileInfo = []
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                fileNameTmp = os.path.join(root, name)
                # 该值为True则全部记录
                if (True == isrecursive):
                    fileInfo.append(fileNameTmp)
                elif (False == isrecursive and root == dir):
                    fileInfo.append(fileNameTmp)
                if True == isrecursive:
                    for name in dirs:
                        if fileNameTmp not in fileInfo:
                            fileInfo.append(os.path.join(root, name))

        return fileInfo

    #从字符串从读取从数据组合成string
    def __get_num_by_str(self, str):
        r = re.compile(r'[0-9]+')
        result = r.findall(str)
        resultStr = ''
        for o in result:
            resultStr += o

        return resultStr
    #获取文件的最后修改时间，返回unix时间戳
    def __get_file_time(self, filePath):
        return os.path.getmtime(filePath)

    #从确定的行号开始读取文件
    #考虑是否分段读取文件
    #分段读取文件的话造成文件有一些原本被标记的string可能被截断
    def __read_file(self, file, re, num=1):
        if False == os.path.exists(file):
            print ('文件没有找到:' + file).decode('utf-8')
            return ['', 0]

        f = open(file, 'rb')
        str = ''
        counter = num;
        result = []
        for line in f.readlines()[num:len(f.readlines()) - 1]:
            str += line
            counter += 1
            #判断当前字节大小
            if sys.getsizeof(str) > self.__fileMaxSize:
                result.extend(re.findall(str))
                str = ''

        if '' != str:
            result.extend(re.findall(str))
        f.close()
        return (result, counter)
    #根据传递进来的参数来做不同的事情
    #参数有test => 测试conf文件是否可以使用
    #action 执行
    def action(self, argv):
        # print self, argv
        handleFile = self.__load_files()

        updateJson = []
        #遍历文件
        for o in handleFile:
            targetFile = o.get('file')
            targetStr = self.__read_file(targetFile, re.compile(o.get('match')), num = o.get('number'))
            #不为空则进行re操作
            matchList = targetStr[0]
            if 0 < len(matchList):
                print (targetFile + '匹配到内容').decode('utf-8')
                # analyze.__content += targetFile + '文件从'.decode('utf-8') + str(targetStr[1]) + '行号之后匹配的内容如下' + ''.join(matchList)
                analyze.__content += (targetFile + '文件从' + str(targetStr[1]) + '行号之后匹配的内容如下' + ''.join(matchList)).decode('utf-8') + '\n'
                # analyze.__content += targetFile + 'from' + str(targetStr[1]) + 'match' + ''.join(matchList)
                updateJson.append({'file':targetFile, 'number':targetStr[1], 'modified': self.__get_file_time(targetFile)})
            else:
                print (targetFile + '该文件没有匹配到内容').decode('utf-8')

        if  '' != analyze.__content:
            self.__send_mail(analyze.__content)
            self.__update_json(updateJson)

    #更新json文件
    #param dict
    def __update_json(self, json):
        # 连接数据库
        try:
            sqlite_conn = sqlite3.connect(analyze.__sqlite)
        except sqlite3.Error, e:
            print "连接sqlite3数据库失败".decode('utf-8'), "\n", e.args[0]
            return

        # 获取游标
        sqlite_cursor = sqlite_conn.cursor()

        def updateDB(json):
            updateSql = 'update file_log set num = ' + str(json.get('number')), ',modified = ' + str(json.get('modified')) + 'where file = ' + json.get('file')
            print 'updateSql', updateSql
            sqlite_cursor.execute(updateSql)
            sqlite_conn.commit()
        def insertDB(json):
            updateSql = "insert into file_log(num, modified, file) values('" + str(json.get('number')) +"', '" + str(json.get('modified')) + "', '" + json.get('file') + "')"
            print 'updateSql', updateSql
            sqlite_cursor.execute(updateSql)
            sqlite_conn.commit()
        #之前有数据
        for o in json:
            for o1 in self.__history:
                #执行update操作
                if (o.get('file') == o1[0]):
                    #更新
                    updateDB(o)
                    #干掉他
                    json.remove(o)
        #之前没有数据
        for o in json:
            # 插入
            insertDB(o)
            # 干掉他
            json.remove(o)
        sqlite_cursor.close()
    #调试输出
    def printArg(self):
        # print self.__sender, self.__receiver, self.__smtp, self.__smtpUser, self.__smtpUserPass, self.__subject
        #print type(self.__file)
        # print self.__history.get('file')
        #print self.__file
        #print self.__path
        # print '__content', analyze.__content, len(analyze.__content)
        1
analyzeObj = analyze()

#action
analyzeObj.action(sys.argv)
analyzeObj.printArg()
