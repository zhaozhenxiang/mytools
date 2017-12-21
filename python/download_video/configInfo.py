#coding=utf-8
import configparser

class configInfo():
    cf = configparser.ConfigParser()
    cf.read('./config.ini')
    #然后进行配置文件的读取操作。

    #以get为例，示例代码如下：

    #  定义方法，获取config分组下指定name的值
    def get(self, key, name):
        value = self.cf.get(key, name)
        return value

# instance = configInfo()
# print(instance.get('mysql', 'user'))