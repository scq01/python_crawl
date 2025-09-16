from flask import Flask,request,jsonify
from 酷狗音乐 import search
app = Flask(__name__)
# 全局配置
app.config['JSON_AS_ASCII'] = False  # 禁用 ASCII 转义
app.config['JSON_SORT_KEYS'] = False  # 保持字典顺序

@app.after_request
def after_request(response):
    """添加必要的响应头"""
    response.headers.add('Content-Type', 'application/json; charset=utf-8')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
    return response
@app.route('/search',methods=['GET'])
def search_music():
    keyword = request.args.get('keyword')
    page = request.args.get('page')
    data = search(keyword,page)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5500)