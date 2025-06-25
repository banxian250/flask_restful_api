from datetime import datetime

from utils.mysql_helper import MySQLHelper
from managers.base_cfg import BaseConfig
from managers.number_generator import NumberGeneratorManager
from wechatpy import WeChatClient
import uuid
from utils.redis_helper import RedisHelper
import json
from models.miniprogram_member import MiniProgramMember
from repositorys.miniprogram_member import MiniProgramMemberRepository


class Member():
    def member_login(self, code: str):
        cfg = BaseConfig()
        base_cfg = cfg.get()

        client = WeChatClient(base_cfg['app_id'], base_cfg['app_secret'])
        login_res = client.wxa.code_to_session(code)

        # sql = '''select *
        #          from miniprogram_member
        #          where openid = %(openid)s'''
        # params = {'openid': login_res['openid']}
        # db = MySQLHelper()
        # member_info = db.single(sql, params)

        member_info = MiniProgramMember.query.filter_by(openid=login_res['openid']).first()

        _member_id = 0
        _openid = ''

        if not member_info:
            id_generator = NumberGeneratorManager()
            member_id = id_generator.get('miniprogram_member', 1)
            # insert_sql = '''insert into miniprogram_member(id, openid, create_time)
            #                 values (%(member_id)s, %(openid)s, %(create_time)s)'''
            # insert_params = {'member_id': member_id, 'openid': login_res['openid'], 'create_time': datetime.now()}
            # db = MySQLHelper()
            # db.insert(insert_sql, insert_params)
            MiniProgramMemberRepository.create(member_id, login_res['openid'], datetime.now())
            _member_id = member_id
            _openid = login_res['openid']
        else:
            member_info_dict = member_info.to_dict()
            _member_id = member_info_dict['id']
            _openid = member_info_dict['openid']

        authorization = uuid.uuid4().hex
        redis_helper = RedisHelper()
        cache_data = json.dumps({'member_id': _member_id, 'openid': _openid})
        redis_helper.set(f'login:{authorization}', cache_data, 60 * 60 * 24)

        return {'authorization': authorization}

    def get_member(self, request_headers):
        authorization_header = request_headers.get('Authorization')
        if not authorization_header:
            return None
        else:
            redis_helper = RedisHelper()
            authorization = authorization_header.replace('Bearer ', '')
            authorization_res = redis_helper.get(f'login:{authorization}')
            return authorization_res
