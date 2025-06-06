import pymysql, pymysql.cursors
from dbutils.pooled_db import PooledDB


class MySQLHelper:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=3,
            maxcached=9,
            blocking=True,
            host='101.43.65.120',
            port=3306,
            user='root',
            passwd='123456',
            charset='utf8',
            database='travel_china',
            cursorclass=pymysql.cursors.DictCursor
        )

    def single(self, sql: str, params: dict = None):
        try:
            # 使用 with 语句来管理连接和游标
            with self.pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    return result if result else None  # 返回结果，若为空则返回 None
        except Exception as e:
            # 捕获并记录异常
            print(f"Error occurred while executing query: {e}")
            return None  # 异常发生时返回 None

    def insert(self, sql: str, params: dict = None):
        try:
            # 使用 with 语句来管理连接和游标
            with self.pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    conn.commit()

                    # 使用 rowcount 判断影响的行数
                    if cursor.rowcount > 0:
                        return True  # 表示插入成功
                    else:
                        return False  # 表示没有插入任何记录
        except Exception as e:
            # 捕获并记录异常
            print(f"Error occurred while executing query: {e}")
            return False

    def update(self, sql: str, params: dict = None):
        try:
            # 使用 with 语句来管理连接和游标
            with self.pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    conn.commit()
                    return cursor.rowcount  # 返回影响的行数
        except Exception as e:
            # 捕获并记录异常
            print(f"Error occurred while executing query: {e}")
            return 0
