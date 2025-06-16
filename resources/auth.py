from functools import wraps
from flask import request, jsonify
from utils.redis_helper import RedisHelper

# 这里可以替换为实际的用户验证逻辑，如数据库查询、JWT验证等
def verify_token(token):
    """
    验证token的有效性
    :param token: 用户提供的token
    :return: 如果token有效返回用户信息，否则返回None
    """
    # 示例：简单的token验证
    # 在实际应用中，您应该实现更安全的验证逻辑
    # if token == "valid_token":
    #     return {"user_id": 1, "username": "admin"}
    redis_helper = RedisHelper()
    authorization_res = redis_helper.get(f'login:{token}')
    if not authorization_res:
        return None
    else:
        return authorization_res

def require_auth(f):
    """
    验证用户身份的装饰器
    可以应用在Resource类或具体的方法上
    """
    @wraps(f)
    def decorated(*args, **kwargs):
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
        
        return f(*args, **kwargs)
    
    return decorated