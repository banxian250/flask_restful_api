from utils.mysql_helper import MySQLHelper
from models.base_cfg import db, BaseCfg


class BaseConfig():
    def get(self):
        # db = MySQLHelper()
        # sql = '''select *
        #          from base_cfg'''
        # base_cfg = db.single(sql)
        # return base_cfg
        res = BaseCfg.query.first()
        return res.to_dict()
