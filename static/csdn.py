import requests
import os
from bs4 import BeautifulSoup
import html2text as ht2
from static.utils import *


def getArticle(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

    text_maker = ht2.HTML2Text()
    text_maker.bypass_tables = False
    text_maker.ignore_links = True
    aaa = requests.get(url, headers=headers).text
    aaa=aaa.replace('data-src','src')


    soup = BeautifulSoup(aaa, 'html.parser')

    tempstr=soup.find('h2', class_='rich_media_title').text.replace('\n','')
    tempstr=tempstr.replace(' ','')
    articlename = tempstr + '.md'
    """消除底部多余"""
    soup.find('div', class_='article-tag__error-tips').extract()
    soup.find('div', class_='article-tag__list').extract()
    soup.find('div', class_='album_read_hd weui-flex').extract()
    soup.find('div', class_='like_comment_bd').extract()
    soup.find('span', class_='album_read_nav_item album_read_nav_prev weui-flex__item').extract()
    soup.find('span', class_='album_read_nav_item album_read_nav_next weui-flex__item').extract()
    soup.find('span', class_='rich_media_meta rich_media_meta_nickname').extract()
    for i in soup.findAll('div', class_='weui-flex__item'):
        i.extract()
    for i in soup.findAll('span', class_='sns_opr_gap'):
        i.extract()
    for i in soup.findAll('div', class_='weui-dialog__hd'):
        i.extract()
    for i in soup.findAll('div', class_='weui-dialog__bd'):
        i.extract()
    for i in soup.findAll('div', class_='weui-dialog__ft'):
        i.extract()
    for i in soup.findAll('p', class_='weui-toast__content'):
        i.extract()
    soup.find('div', class_='like_comment_primary_inner').extract()
    soup.find('div', class_='qr_code_pc_outer').extract()
    soup.find('div', class_='weui-desktop-popover__desc').extract()
    for i in soup.findAll('pre'):
        i.extract()


    text1 = text_maker.handle(soup.prettify())

    """正则表达式将格式变正常"""
    #先把**asd** **dsadsa**加一个空格再减去一个空格，不然连在一起不符合md规则
    text1 = re.sub('\*\*\s\*', '**  *', text1)
    text1 = re.sub('\*\*\s', '**', text1)
    text1 = re.sub('\*\*\*\*', '', text1)

    newtext=img_replace(text1)
    # with open(articlename, mode='w', encoding='utf-8') as f:
    #     f.write(newtext)
    return newtext




if __name__ == '__main__':
    # url='https://mp.weixin.qq.com/s?__biz=MjM5MjAwODM4MA==&mid=2650851243&idx=1&sn=7ab164a6bf60680d3bf78ff70dd5df52&chksm=bd58b6788a2f3f6e6b31db53709894954aa0c86647f8d394042be0f9ce4f07aa3cc9ad54aed7&token=2028362782&lang=zh_CN#rd'
    url = 'https://mp.weixin.qq.com/s/eyQZhDNFvJus6foa3pzz9Q'
    # url='https://mp.weixin.qq.com/s?__biz=MzA3OTQxNjUwNg==&mid=2651896486&idx=2&sn=8f5049c505fb6e93bc3dbffe4f8918ba&chksm=8457c773b3204e65aa8bdfee779eeefc399d5bdbbdc0e9a4f06189505c757e96223da58be9b5&token=2028362782&lang=zh_CN#rd'
    getArticle(url)
    #
    # text_maker = ht2.HTML2Text()
    # with open('E:\work\文章爬虫\weixin.html', encoding='utf-8')as f:
    #     file = f.read()
    #     text1 = text_maker.handle(file)
    #     with open('weixinpart.md', mode='w', encoding='utf-8') as f:
    #         f.write(text1)
