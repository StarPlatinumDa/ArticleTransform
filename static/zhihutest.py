import requests
import re #正则表达式筛选
import os
from bs4 import BeautifulSoup
import html2text as ht2
import traceback
import json


def getArticle(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

    text_maker = ht2.HTML2Text()
    text_maker.bypass_tables = False
    text_maker.ignore_links = True
    aaa = requests.get(url, headers=headers).text

    soup = BeautifulSoup(aaa, 'html.parser')
    articlename = soup.find('h1', class_='Post-Title').text + '.md'
    """消除顶部"""
    soup.find('div', class_='ColumnPageHeader-Wrapper').extract()
    soup.find('header', class_='Post-Header').extract()
    """去除点赞"""
    soup.find('div', class_='Sticky RichContent-actions is-bottom').extract()
    """去除标签"""
    soup.find('div', class_='Post-topicsAndReviewer').extract()
    """消除底部专栏收录评论"""
    soup.find('div', class_='Post-Sub Post-NormalSub').extract()
    """消除底部发布时间"""
    soup.find('div', class_='ContentItem-time').extract()

    text1 = text_maker.handle(soup.prettify())

    """正则表达式去除多余的图片标签"""
    text1 = re.sub('!\\[\\]\\(data.*\n.*svg>\\)', '', text1)
    text1 = re.sub('!\\[\\]\\(data.*\n.*\n.*svg>\\)', '', text1)


    newtext=img_replace(text1)
    with open(articlename, mode='w', encoding='utf-8') as f:
        f.write(newtext)

def download(url, filename):  # 判断文件是否存在，存在则退出本次循环
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

        r = requests.get(url,headers=headers, stream=True, timeout=60)  # 以流数据形式请求，你可获取来自服务器的原始套接字响应
        r.raise_for_status()
        with open(filename, 'wb') as f:  # 将文本流保存到文件
            """content是bytes 型的二进制数据 text是unicode 型的文本数据"""
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        print('{}下载完毕！'.format(filename))
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)

"""请求服务器将文章中的url变为服务器里存储的"""
def upload_img(urllist):
    urldict = {'imageUrls': urllist}
    urldict = json.dumps(urldict)
    tempheaders = {'Authorization': 'd08d95b7cf91448bb825929456f5f4c7',
                   'Content-Type': 'application/json'}
    uploadurl = 'http://sharer.violetfreesia.com:666/sharer-api/save-article-images'
    response = requests.post(url=uploadurl, headers=tempheaders, data=urldict)
    rs = response.json()
    return rs

def img_replace(text):
    # if os.path.exists('pictures') is False:
    #     os.makedirs('pictures')

    li = re.findall('!\[.*\)', text)
    i = 0
    urllist=[]
    """本地下载"""
    # for line in li:
    #     temp = re.findall('http.*\)', line)[0].strip(')')
    #     urllist.append(temp)
    #     filename = os.path.join('pictures', temp.split('/')[-1])
    #     if len(temp.split('.')[-1])!=3:
    #         filename = os.path.join('pictures', temp.split('.')[-2].split('/')[-1])
    #         filename=filename+'.jpg'
    #         print(filename)
    #
    #     download(temp,filename)
    #     aaa = aaa.replace(temp,filename)
    #     # line=line.replace(temp,'sss')
    #     i += 1
    for line in li:
        temp = re.findall('http.*\)', line)[0].strip(')')
        urllist.append(temp)
    rs=upload_img(urllist)
    for i in rs:
        print(i,rs[i])
        text=text.replace(i,rs[i])
    return text


if __name__ == '__main__':

    # url = 'https://zhuanlan.zhihu.com/p/378317629'
    url='https://zhuanlan.zhihu.com/p/38366833'
    # url='https://zhuanlan.zhihu.com/p/356987472'
    getArticle(url)

# #标签
# for i in soup.find_all('div',class_='Tag Topic'):
# 	print(i.find('div',id='null-toggle').text)


# print(soup.find_all('div',class_='Popover'))
