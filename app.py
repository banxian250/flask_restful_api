"""from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)"""
from resources import app


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获，也相当于一个视图函数
    """
    return {'error': 1, 'message': str(e)}, 500
    # return {'error': 1, 'message': str(e)}


if __name__ == '__main__':
    app.run(debug=True)
