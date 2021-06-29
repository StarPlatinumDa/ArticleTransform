import requests
import re #正则表达式筛选
import os
import json

def img_replace(articlename):
    # if os.path.exists('pictures') is False:
    #     os.makedirs('pictures')


    file = open(articlename, encoding='utf-8')
    aaa = file.read()
    li = re.findall('!\[.*\)', aaa)
    i = 0
    urllist=[]
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
        aaa=aaa.replace(i,rs[i])
    with open(articlename, mode='w', encoding='utf-8') as f:
        f.write(aaa)

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