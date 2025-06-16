"""from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)"""
from resources import app
import traceback
from flask import request, jsonify, g
from managers.member import Member


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获，也相当于一个视图函数
    """
    return {'error': 1, 'message': f'{e.__class__.__name__}：{str(e)}', 'traceback': traceback.format_exc()}, 500
    # return {'error': 1, 'message': str(e)}


@app.before_request
def log_before_request():
    # 打印请求方法、路径、参数
    print(f"\n[Request] {request.method} {request.path}")
    print(f"[Headers] {request.headers}")

    # if not request.path == '/member/login':
    #     member = Member()
    #     member_res = member.get_member(request.headers)
    #     print('get member')
    #     print(member_res)
    #     if not member_res:
    #         return {'error': 1, 'message': '', 'traceback': ''}, 401
    #     else:
    #         g.current_user = member_res
    #     print('get member end')

    # GET 请求的查询参数
    if request.method == 'GET':
        print(f"[Query Params] {request.args}")

    # POST/PUT/PATCH 请求的 JSON 数据
    elif request.method in ('POST', 'PUT', 'PATCH'):
        if request.is_json:
            print(f"[JSON Body] {request.get_json()}")
        else:
            print(f"[Form Data] {request.form}")

    # 打印 URL 参数（适用于动态路由）
    print(f"[View Args] {request.view_args}")


if __name__ == '__main__':
    app.run(debug=True)
