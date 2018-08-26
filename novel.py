import requests
from requests.exceptions import Timeout
import threading
from bs4 import BeautifulSoup
from queue import Queue
import time
import random


q_url = Queue()          #消息队列
Thread_num = 4
lock = threading.Lock()  #添加锁
file = open("novel.txt",'a+')

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'Hm_lvt_a60a7b9e01a686181bbc4e04a9306bb5=1535244619; Hm_lpvt_a60a7b9e01a686181bbc4e04a9306bb5=1535244619; UM_distinctid=16573b5ce891ae-07794f45a4a332-454c092b-100200-16573b5ce8a1b4; CNZZDATA1256261660=294109264-1535239938-%7C1535239938; CNZZDATA1253244348=1986706387-1535242925-%7C1535242925; __qiqi__view_ads106308=%2C24346; uv_cookie_109465=1; uv_cookie_106305=1; bdshare_firstime=1535244683398; uv_cookie_106307=1; __qiqi__view_plan106308=%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071%2C4071',
    'DNT':'1',
    'Host':'www.qingdoutxt.cc',
    'Referer':'http://www.qingdoutxt.cc/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

def url_cre():
    """
        产生url
    """
    global seen 
    
    for i in range(1,201):
        url_start = "http://www.qingdoutxt.cc/chapter_1205728_"
        params = '.html'
        url = url_start + str(i) + params
        #yield url 
        q_url.put(url)
    

def worker():
    """
        获取网页信息
    """
    global q_url
    global headers
    global lock
    while True:
        try: 
            lock.acquire()
            url = q_url.get(timeout = 1)
            
            r = requests.get(url, headers=headers, timeout=30)
            lock.release()

            html = r.content
            parse_html(html)

        except Timeout as e:
            lock.release()  #释放锁
            print(str(e))
            break
        except queue.Empty:
            lock.release()
        




def parse_html(html):
    """
        进行解析
    """
    try:
        
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find(class_="readtxt").find("h2").find('a').string
        print(title)
        lock.acquire()
        save_to(title)
        p_list = soup.find(id="chapter_content").find_all('p')
        for p in p_list:
            if p.string == None:
                pass
            else:
                #print(p.string)
                save_to(p.string)
    except:
        print("解析出错")
        pass
    finally:
        lock.release()



def save_to(para):
    """
        开始存储
    """
    global file
    if file.write(para + '\n'+ '\n'):
        pass
    else:
        print("保存失败")

print("working.....")
c_start = time.time()#获取开始时间
ths = []   #线程列表
#批量创建线程
for i in range(Thread_num):
    t = threading.Thread(target = worker)
    ths.append(t)
#创建产生url 的线程
url_thread = threading.Thread(target = url_cre)
#批量开始线程
for i in range(Thread_num):
    ths[i].start()
    
url_thread.start()

for i in range(Thread_num):
    ths[i].join()

url_thread.join()
  
end_time = time.time()
print("All Done")
print("总用时:", end_time - c_start)