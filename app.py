from flask import Flask,request,abort,Response
from static.zhihutest import getArticle as zhihu_get
from static.weixinchange import getArticle as wechat_get
app = Flask(__name__)
from flask_cors import CORS#跨域

CORS(app,supports_credentials=True)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/articledownload',methods=['post'])
def deal_url():
	url=request.json['url']
	token=request.json['token']
	if url.__contains__('zhihu.com'):
		article = zhihu_get(url,token)
		print('Done!')
		return {'article': article}
	elif url.__contains__('weixin.qq'):
		article = wechat_get(url,token)
		print('Done!')
		return {'article': article}
	else:
		# res=Response('链接错误或不支持！')
		print('url error or not supported now!')
		abort(404)

	# # article = wechat_get(url)
	# print(type(article))
	# return {'article':article}

if __name__ == '__main__':
	app.run()
