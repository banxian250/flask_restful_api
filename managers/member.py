from datetime import datetime

from utils.mysql_helper import MySQLHelper
from managers.base_cfg import BaseConfig
from managers.number_generator import NumberGenerator
from wechatpy import WeChatClient


class Member():
    def member_login(self, code: str):
        cfg = BaseConfig()
        base_cfg = cfg.get()

        client = WeChatClient(base_cfg['app_id'], base_cfg['app_secret'])
        login_res = client.wxa.code_to_session(code)

        sql = '''select *
                 from miniprogram_member
                 where openid = %(openid)s'''
        params = {'openid': login_res['openid']}
        db = MySQLHelper()
        member_info = db.single(sql, params)
        if not member_info:
            id_generator = NumberGenerator()
            member_id = id_generator.get('miniprogram_member', 1)
            insert_sql = '''insert into miniprogram_member(id, openid, create_time)
                            values (%(member_id)s, %(openid)s, %(create_time)s)'''
            insert_params = {'member_id': member_id, 'openid': login_res['openid'], 'create_time': datetime.now()}
            db.insert(insert_sql, insert_params)
            return {'member_id': member_id, 'openid': login_res['openid']}
        else:
            return {'member_id': member_info['id'], 'openid': member_info['openid']}
