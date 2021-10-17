#author:zac
import requests
from bs4 import BeautifulSoup
import re
import os
from contextlib import closing
from tqdm import tqdm

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
        ,"Referer": "https://manhua.dmzj.com/guowangpaiming/116550.shtml"
}

def get_imgurl(url0,url1):              #url0是该章节的首页 url1是该章节的第一个图片的地址
        rsp = requests.get(url=url0, headers=header)
        rsp.encoding = 'utf-8'
        bs = BeautifulSoup(rsp.text, 'lxml')
        script_info = bs.script
        # 利用正则将script其中的图片页数提取出来
        nums = re.findall('\|(\d{4})', str(script_info))
        nums.sort(reverse=True)
        urls = []
        for num in nums:
                urls.insert(0,url1[:-8] + num + ".jpg")
        #返回一个章节的图片地址数组
        return urls
def get_chapers(url0):                  #url0是该漫画的首页地址
        change_ref(url0)
        rsp = requests.get(url=url0, headers=header)
        rsp.encoding = 'utf-8'
        bshtml = BeautifulSoup(rsp.text, 'lxml')
        chaperlist = bshtml.find('div', class_="cartoon_online_border")
        chapers = chaperlist.find_all('a')
        chaperurls = []
        chapernames = []
        for chaper in chapers:
                chaperurls.insert(0, "https://manhua.dmzj.com/" + chaper.get('href'))
                chapernames.insert(0, "国王排名" + chaper.text)
        #返回漫画的所有章节首地址和章节名(数)
        return chapernames,chaperurls
def get_firstimgurl(chapernum):             #chapernum是该章节的章节数
        url = "https://images.dmzj.com/g/%E5%9B%BD%E7%8E%8B%E6%8E%92%E5%90%8D/%E7%AC%AC"+chapernum+"%E5%8D%B7/0000.jpg"
        #返回某章节第一个图片地址
        return url

#该方法是因为我发现第一张的url不是卷编码 而是话编码，所以给第一章用这个函数
def get_firstimgurl1():
    return "https://images.dmzj.com/g/%E5%9B%BD%E7%8E%8B%E6%8E%92%E5%90%8D/%E7%AC%AC01%E8%AF%9D/0000.jpg"

def down_img(url,num,dirname): #url是图片地址 ,num是图片编号,chapername是文件夹名
    with closing(requests.get(url, headers=header, stream=True)) as response:
        chunk_size = 1024
        if response.status_code == 200:
            with open(dirname+'/'+num+'.jpg', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
        else:
            print('链接异常')

def change_ref(chaperurl):
    global header
    header['Referer'] = chaperurl

#url0是漫画首页
url0 = "https://manhua.dmzj.com/guowangpaiming"
#chapername是每一章的名字,chaperurl是每一章的首页
chapernames,chaperurls = get_chapers(url0)
for i in range(len(chaperurls)):
        chapernum = chapernames[i][-3:-1]
        chapername= chapernames[i]
        chaperurl = chaperurls[i]
        firstimgurl = get_firstimgurl(chapernum) if i<len(chaperurls)-1 else get_firstimgurl1()
        imgurls = get_imgurl(chaperurl,firstimgurl)
        os.mkdir(chapername)
        for imgurl in tqdm(imgurls):
            down_img(imgurl,imgurl[-8:-4],chapername)
        print(chapername+"下载完成")
