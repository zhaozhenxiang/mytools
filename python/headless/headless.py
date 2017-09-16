#coding=utf-8
#"使用headlines登录"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os 
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0  
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

chrome_options.binary_location = r'C:\Users\zhaozhenxiang\AppData\Local\Google\Chrome\Application\chrome.exe'
# chrome_options.binary_location = '/opt/google/chrome/chrome'

opener = webdriver.Chrome(executable_path=r"C:\Python27\chromedriver.exe", chrome_options=chrome_options)

opener.get("http://xxxx/admin/login")

u = opener.find_element_by_id("username")
u.send_keys("cuisy")  

p = opener.find_element_by_id("password") 
p.send_keys("123456")  

button = opener.find_element_by_id("btnSumit")
button.click()

#admin/gateway/list 爱悠后台
print(opener.title, opener.current_url)


try: 
    WebDriverWait(opener, 10, 0.5).until(EC.presence_of_element_located((By.ID, "ring")))
    print(opener.title, opener.current_url) 
  
finally:  
    opener.quit()  