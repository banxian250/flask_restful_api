from utils.mysql_helper import MySQLHelper


class BaseConfig():
    def get(self):
        db = MySQLHelper()
        sql = '''select *
                 from base_cfg'''
        base_cfg = db.single(sql)
        return base_cfg
