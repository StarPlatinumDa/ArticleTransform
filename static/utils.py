import requests
import re #正则表达式筛选
import json

def img_replace(text,token):
    """csdn的图片url会换行"""
    # csdn1 = re.findall('!\].*\n.*\)', text)
    # for line in csdn1:
    #     text=text.replace(line,line.replace('\n',''))
    #
    # li = re.findall('!\[.*\)', text)
    #
    # urllist = []
    # for line in li:
    #     temp = re.findall('http.*\)', line)[0].strip(')')
    #     urllist.append(temp)
    #
    # print(urllist)
    # print('')

    csdn1 = re.findall('\]\(http.*\n.*\)', text)
    for line in csdn1:
        text = text.replace(line, line.replace('\n', ''))

    li = re.findall('\]\(http.*\)', text)

    urllist = []
    for line in li:
        temp = re.findall('http.*\)', line)[0].strip(')')
        urllist.append(temp)

    # print(urllist)
    # print('')


    # csdn2 = re.findall('!\[.*\n.*\)', text)
    # for line in csdn2:
    #     temp = re.findall('http.*\n.*\)', line)[0].strip(')')
    #     urllist.append(temp)


    # csdn4 = re.findall('!\[.*\)', text)
    # for line in csdn4:
    #     temp = re.findall('http.*\n.*\)', line)[0].strip(')')
    #     urllist.append(temp)
    rs = upload_img(urllist,token)
    for i in rs:
        # print(i, rs[i])
        text = text.replace(i, rs[i])
    return text

"""请求服务器将文章中的url变为服务器里存储的"""
def upload_img(urllist,token):
    urldict = {'imageUrls': urllist}
    urldict = json.dumps(urldict)
    tempheaders = {'Authorization': token,
                   'Content-Type': 'application/json'}
    uploadurl = 'http://sharer.violetfreesia.com:666/sharer-api/save-article-images'
    response = requests.post(url=uploadurl, headers=tempheaders, data=urldict)
    rs = response.json()
    return rs