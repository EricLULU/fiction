import aiohttp
import asyncio
from bs4 import BeautifulSoup


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

file = open("novel_1.txt",'a+')



def url_cre():
    """
        产生url
    """
    for i in range(1,201):
        url_start = "http://www.qingdoutxt.cc/chapter_1205728_"
        params = '.html'
        url = url_start + str(i) + params
        yield url 


async def parse_html(html):
    """
        进行解析
    """
    try:
        
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find(class_="readtxt").find("h2").find('a').string
        print(title)
        await save_to(title)
        p_list = soup.find(id="chapter_content").find_all('p')
        for p in p_list:
            if p.string == None:
                pass
            else:
                await save_to(p.string)
    except:
        pass

async def save_to(para):
    """
        开始存储
    """
    global file
    if file.write(para + '\n'+ '\n'):
        pass
    else:
        print("保存失败")


async def fetch(session, url):
    global headers
    async with session.get(url, headers=headers, timeout=10) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        for url in url_cre():
            print(url)
            html = await fetch(session, url)
            await parse_html(html)
 
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
