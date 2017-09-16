#! /usr/bin/env python
#encoding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 

from selenium import webdriver 
import time 

driver = webdriver.PhantomJS(executable_path="./phantomjs.exe")
url = 'http://www.baidu.com/s?wd=%CC%EC%CF%C2%CE%DE%D4%F4'

def get_html():
    return driver.page_source.encode('gbk','ignore')

def get_screen_shot():
    driver.get_screenshot_as_file("3.jpg")

def test():      
    driver.get(url)
    time.sleep(5)

    print(get_html())
    get_screen_shot() 

    driver.close()

if __name__ == '__main__':
    test()