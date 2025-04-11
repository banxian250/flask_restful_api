from flask import Flask
from flask_restful import Api

app = Flask(__name__)
# api = Api(app)

# 保存Flask原始的异常处理器
original_handle_exception = app.handle_exception
original_handle_user_exception = app.handle_user_exception

api = Api(app, catch_all_404s=False)

# 初始化API后恢复Flask原始的异常处理器
app.handle_exception = original_handle_exception
app.handle_user_exception = original_handle_user_exception

from resources import member_resource,member_login_resource
