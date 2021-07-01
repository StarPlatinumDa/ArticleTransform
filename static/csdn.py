import requests
import os
from bs4 import BeautifulSoup
import html2text as ht2
from static.utils import *


def getArticle(url,token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

    text_maker = ht2.HTML2Text()
    text_maker.bypass_tables = False
    text_maker.ignore_links = True
    aaa = requests.get(url, headers=headers).text


    soup = BeautifulSoup(aaa, 'html.parser')

    tempstr=soup.find('h1', class_='title-article').text
    articlename = tempstr + '.md'
    """消除底部多余"""
    soup=soup.find('div',class_='article_content')


    # print(soup.prettify())
    text1 = text_maker.handle(soup.prettify())

    """正则表达式将格式变正常"""

    text1 = re.sub('img-\n', 'img-', text1)


    # newtext=text1
    newtext=img_replace(text1,token)
    # with open('test.md', mode='w', encoding='utf-8') as f:
    #     f.write(newtext)
    return newtext




if __name__ == '__main__':
    # url = 'https://blog.csdn.net/sfakh/article/details/114579255'
    url='https://blog.csdn.net/hihell/article/details/118340372?utm_medium=distribute.pc_feed_v2.none-task-blog-yuanlijihua_tag_v1-2.pc_personrecdepth_1-utm_source=distribute.pc_feed_v2.none-task-blog-yuanlijihua_tag_v1-2.pc_personrec'
    # url='https://blog.csdn.net/Mculover666/article/details/118247915?utm_medium=distribute.pc_feed_v2.none-task-blog-user_follow-1.pc_personrecdepth_1-utm_source=distribute.pc_feed_v2.none-task-blog-user_follow-1.pc_personrec'
    getArticle(url,token='dd2fb0bf452f4f46985e5d926c33f158')
    #
    # text_maker = ht2.HTML2Text()
    # with open('E:\work\文章爬虫\weixin.html', encoding='utf-8')as f:
    #     file = f.read()
    #     text1 = text_maker.handle(file)
    #     with open('weixinpart.md', mode='w', encoding='utf-8') as f:
    #         f.write(text1)
