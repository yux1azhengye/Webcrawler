#author:zzzzachary
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}

def get_Content(url):
    response = requests.get(url=url,headers=header)
    response.encoding = 'utf-8'
    html = response.text
    bs = BeautifulSoup(html,'lxml')
    content = bs.find('div',id='content')
    content = content.text.strip( ).split('\xa0'*4)
    return content

def find_all_url(url0):
    url = [20]
    url[0] = url0
    for i in range(2, 10):
        url1 = url[0][:-5] + "_" + '{}'.format(i) + ".html"
        req = requests.get(url=url1)
        req.encoding = 'utf-8'
        html = req.text
        url.append(url1)
        if html.find('下一页') == -1:
            break
    return url

if __name__ == '__main__':
    url0 = 'http://www.xsbiquge.cc/19_19256/'
    rps = requests.get(url=url0,headers=header)
    rps.encoding = 'utf-8'
    html = rps.text
    bss = BeautifulSoup(html,'lxml')
    chapers = bss.find('div',id='list').find_all('a')

    for chaper in tqdm(chapers[9:]):#这里用了切片把置顶在最上面的9个最新章节去掉
        url = "http:"+chaper.get('href')
        chapername = chaper.string+'.txt'
        contents = []
        for url in find_all_url(url):
            contents.append(get_Content(url))
            with open(chapername,'a',encoding='utf-8') as f:
                for content in contents:
                    f.write("".join(content))

