import redis
from typing import Optional, Union


class RedisHelper:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host='101.43.65.120',
            port=6379,
            password='liu281265',
            decode_responses=True,
            db=0
        )
        self.conn = redis.Redis(connection_pool=self.pool)

    def set(self,
            key: str,
            value: Union[str, int, float],
            ex: Optional[int] = None,
            ) -> bool:
        return self.conn.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[str]:
        return self.conn.get(key)


if __name__ == '__main__':
    # 使用示例 --------------------------
    helper = RedisHelper()

    # 设置值（带 60 秒过期）
    helper.set("test_key", "hello_redis", ex=60)

    # 获取值
    value = helper.get("test_key")
    print(f"获取到的值: {value}")  # 输出 hello_redis

    # 获取不存在的键
    print(helper.get("non_existent"))  # 输出 None
