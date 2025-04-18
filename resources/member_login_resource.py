from flask_restful import Resource
from utils.rsa_helper import RSAHelper
from resources import api


class MemberLoginResource(Resource):
    def post(self):
        private_key_str = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCus2kTKxyRSgQLYKUNd9o8GfmiC6nFUmhkiXf78zzjrfds21LF94JA6jQE6uyWzZIaWMriDJ75YlMTdx/kQT46zua/D4H8HfaTHDizMGKkQXnB8B+zv6mAd9ndQjuzdE+FuXe/vulq9XK/Duy5YwXGzfMLtGfXpJB3OVxFiAkRmBgCot51I/WTwxC6/ki6VwnXpQTeAUKggoug3tw8YCaDB4K3ueRn/gTTbtdGcM3r19iyOUGUWgQEL8SuLcFIn581x4dirV8uMXdGWOs8CcdxTBvLIqFmTs5rsDsWmKwQ6IeEKAtNyJcEsv4fPQ6BNhZq/xfeV/V0lQWYkgw7SxLzAgMBAAECggEAa/fXbZBMVIKQ41M0TpGO32wSOpLItnmKqO/Ipn6aV//xFWaqzkx8RJA52/wwgbbEn+HWaUPxkCCzRSlvHUsxIXkzZEs6Q01lUV+0rxGtNOR+UlyLyzQdlpb7n2HKscqlRvjryCY97euJogigRqarMEWh+s7hCoXa/sQFgbdkG2mFkn+R11Cb7m05aUQ4dbScr+b90qdDKPovlFnUjOgudbdZJOTTeP4sb3eRqhOB8aZUCpWNtfFgxBULr3vKmQGJV9z8anjGzznBNcNEvwVUPMV9l2WPyGwz2joALN/k6xQV70t1jTr2kRuz9EsmtdawiyuJ4F1T+FV9gyjXe4KL+QKBgQDZvenDVqSa14ZqpUS381gG2+7CMpkstLEzQMVegi73Id4420/9SGTs5Olo/MZ+Gd1PzSHul9EcIPwJylCW6+pms1rtWH1K29m4ImU9W/aq2xugGIIJzzwdZrO0G8mlKuZRWciktnUOL6uLveMC8yyf5azPdFr6NXW912UzOOjEPQKBgQDNZYAZWaEhNkdhzRq7jHr1/Cmpho6y6KFJaurvTweH0R/KJ0LvO9pc3zThm521Y9XnKN/61l1XHpJoFOU/uG/OfI6ED3oUB+ikTNyP1QApPvyldUkj6xxY9ZPzpJPRUDMdBSRuZ73/pRLXoPK5PIgFy5LPCqxpYj4OTaPiYWM27wKBgQDXxmSOSCFMtMImkuqbZBHakj5zwdKbQ+DKSqiMNHQ4QR7Ht0X4WLJzM5G+kaheNGFlgIHcwCPgPSumxA/Cz7z0004LIILhGScTWzp6aNTzkbg5ma/b6rrG5Ay3MkZMYEvnWBMGby1mxoS4MY9yT+rr9Z2f4814YFvyqi5GaWH5fQKBgEXzu5zmmanmAomcgO4++eGs78N8wDzOXZ/Teg/mqnnnDxyaIoG3sLbQjgIILb4JMmB321BikYeKMfKgqzL4bZu1cBQp8TnBN8o9IyEZOeTSPtlbCH3jJNRnTuw7sNwopD/N8IppapwWbERj3EaaBvlyS52X1QBPJTNZ3ebLpC6hAoGAfW/yHB4VqDGfmh4pb3M13svplRusDujbjuJcECS1Xk67ZOYrXCEHAtFIwj7xgpJo9krdVJhfI/aZWq26rTRLCxdsHpQP95PHSSYO47pwC8PVQz2D2DhiFwhm27YAAEEg9o12cvmK30Ca/x7mwvpfSjydw7T4bYU5vYta9V/XNHk='
        public_key_str = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArrNpEysckUoEC2ClDXfaPBn5ogupxVJoZIl3+/M84633bNtSxfeCQOo0BOrsls2SGljK4gye+WJTE3cf5EE+Os7mvw+B/B32kxw4szBipEF5wfAfs7+pgHfZ3UI7s3RPhbl3v77pavVyvw7suWMFxs3zC7Rn16SQdzlcRYgJEZgYAqLedSP1k8MQuv5IulcJ16UE3gFCoIKLoN7cPGAmgweCt7nkZ/4E027XRnDN69fYsjlBlFoEBC/Eri3BSJ+fNceHYq1fLjF3RljrPAnHcUwbyyKhZk7Oa7A7FpisEOiHhCgLTciXBLL+Hz0OgTYWav8X3lf1dJUFmJIMO0sS8wIDAQAB'
        # 初始化帮助类
        rsa_helper = RSAHelper(private_key_str, public_key_str)
        authorization = rsa_helper.encrypt_str(str({'member_id': 1}))
        return {'authorization': authorization}


api.add_resource(MemberLoginResource, '/member/login')
