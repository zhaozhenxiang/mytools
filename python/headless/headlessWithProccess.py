from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from multiprocessing import Process, Pool

chrome_options = Options()
#不显示GUI
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-images')
chrome_options.add_argument('--disable-plugins')
#不加载图片
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)

chrome_options.binary_location = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
# chrome_options.binary_location = '/opt/google/chrome/chrome'
chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3') 
#设置代理
#chromeOptions.add_argument('--proxy-server=http://ip:port')  
chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:1080')  
def load(url, times):
    # time.sleep(2)
    # return
    opener = webdriver.Chrome(chrome_options=chrome_options, )
    for i in range(0, times):
        # opener.get('http://192.168.101.12:91/admin/login')
        opener.get(url)
        # print(opener.get_cookies())
        opener.delete_all_cookies()
        print(opener.title)
        time.sleep(random.uniform(1, 1.5))
    
    opener.close()
        


if __name__ == '__main__':    
    a = time.time()
    pList = []
    for i in range(0, 1):
        print('create process:' + str(i))
        # p = Process(target=load, args=('http://192.168.100.165:85/', 100,))
        p = Process(target=load, args=('http://google.com', 1,))        
        
        p.daemon = True
        pList.append(p)
        p.start()
        
    for p in pList:
        p.join()
    print('time seconds:' + str(time.time() - a))

