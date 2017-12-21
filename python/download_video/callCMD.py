# -*- coding:utf-8 -*-  
#import commands
#(status, output) = commands.getstatusoutput('ping baidu.com')
#print(status, output)

#尝试调用命令行的方式来调用命令
import os
import subprocess
#return string
def done(cmd):
    # output = os.popen('ping baidu.com')
    
    print('调用done的实参为=>' + cmd)
    output = os.popen(cmd)

    result = output.read()
    print('调用done的返回值字符串为=>' + result)
    return result

#使用子进程
#但是什么时候结束呢
def done1(cmd):
    sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    sub.wait()
    return sub.stdout.read().decode('gbk')

# print(done1('ping baidu.com'))