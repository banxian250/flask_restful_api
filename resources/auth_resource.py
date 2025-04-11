from flask import request
from flask_restful import Resource
from functools import wraps
from resources.auth import verify_token


class AuthResource(Resource):
    """
    需要身份验证的资源基类
    所有需要身份验证的资源都应该继承这个类，而不是直接继承Resource
    这样就不需要在每个方法上单独添加装饰器了
    """
    
    def dispatch_request(self, *args, **kwargs):
        """
        重写dispatch_request方法，在调用HTTP方法前进行身份验证
        """
        # 从请求头中获取token
        auth_header = request.headers.get('Authorization')
        
        # 检查是否提供了token
        if not auth_header:
            return {"error": "未提供认证信息"}, 401
        
        # 通常Authorization头的格式是"Bearer token"
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return {"error": "无效的认证类型"}, 401
        except ValueError:
            # 如果分割失败，说明格式不正确
            return {"error": "认证格式不正确"}, 401
         
        # 验证token
        user = verify_token(token)
        if not user:
            return {"error": "无效的认证信息"}, 401
        
        # 将用户信息添加到kwargs中，以便在资源方法中使用
        kwargs['current_user'] = user
        
        # 调用父类的dispatch_request方法，继续处理请求
        return super(AuthResource, self).dispatch_request(*args, **kwargs)