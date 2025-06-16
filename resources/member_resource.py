from resources import api
from resources.auth_resource import AuthResource


class MemberResource(AuthResource):
    def get(self, member_id: int, current_user=None):
        print(1234556)
        print(current_user)
        return {'method': 'get', 'member_id': member_id, 'user': current_user}

    def put(self, member_id: int, current_user=None):
        # 抛出异常，将被全局异常处理器捕获
        raise Exception('Something went wrong')
        # 这行代码永远不会执行
        return {'method': 'put', 'member_id': member_id, 'user': current_user}


api.add_resource(MemberResource, '/member/<int:member_id>')
