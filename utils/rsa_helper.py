import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


class RSAHelper:
    def __init__(self, private_key_str: str = None, public_key_str: str = None):
        """
        初始化 RSA 帮助类
        :param private_key_str: PKCS8 格式的私钥字符串
        :param public_key_str:  PKCS8 格式的公钥字符串
        """
        self.private_key = None
        self.public_key = None

        if private_key_str:
            # 检查是否已经包含 PEM 头尾
            if not private_key_str.startswith('-----BEGIN'):
                # 格式化 Base64 字符串，每 64 个字符添加一个换行
                formatted_key = '\n'.join([private_key_str[i:i + 64] for i in range(0, len(private_key_str), 64)])
                # 添加 PEM 格式的头尾
                private_key_str = f"-----BEGIN PRIVATE KEY-----\n{formatted_key}\n-----END PRIVATE KEY-----"

            try:
                self.private_key = serialization.load_pem_private_key(
                    private_key_str.encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )
            except Exception as e:
                raise ValueError(f"无法加载私钥: {str(e)}")

        if public_key_str:
            # 检查是否已经包含 PEM 头尾
            if not public_key_str.startswith('-----BEGIN'):
                # 格式化 Base64 字符串，每 64 个字符添加一个换行
                formatted_key = '\n'.join([public_key_str[i:i + 64] for i in range(0, len(public_key_str), 64)])
                # 添加 PEM 格式的头尾
                public_key_str = f"-----BEGIN PUBLIC KEY-----\n{formatted_key}\n-----END PUBLIC KEY-----"

            try:
                self.public_key = serialization.load_pem_public_key(
                    public_key_str.encode('utf-8'),
                    backend=default_backend()
                )
            except Exception as e:
                raise ValueError(f"无法加载公钥: {str(e)}")

    def sign(self, data: bytes) -> bytes:
        """
        使用私钥对数据进行签名
        :param data: 要签名的二进制数据
        :return: 签名结果
        """
        if not self.private_key:
            raise ValueError("Private key is required for signing")

        return self.private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        使用公钥验证签名
        :param data: 原始二进制数据
        :param signature: 要验证的签名
        :return: 验证结果
        """
        if not self.public_key:
            raise ValueError("Public key is required for verification")

        try:
            self.public_key.verify(
                signature,
                data,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        使用公钥加密数据
        :param plaintext: 要加密的二进制数据
        :return: 加密结果
        """
        if not self.public_key:
            raise ValueError("Public key is required for encryption")

        return self.public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        使用私钥解密数据
        :param ciphertext: 要解密的二进制数据
        :return: 解密结果
        """
        if not self.private_key:
            raise ValueError("Private key is required for decryption")

        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def sign_str(self, data: str) -> str:
        """
        使用私钥对数据进行签名
        :param data: 要签名的文本数据
        :return: 签名结果
        """
        data = data.encode('utf-8')
        sign_res = self.sign(data)

        return base64.b64encode(sign_res).decode('utf-8')

    def verify_str(self, data: str, signature: str) -> bool:
        """
        使用公钥验证签名
        :param data: 原始文本数据
        :param signature: 要验证的签名
        :return: 验证结果
        """
        data = data.encode('utf-8')
        signature = base64.b64decode(signature)

        return self.verify(data, signature)

    def encrypt_str(self, plaintext: str) -> str:
        """
        使用公钥加密数据
        :param plaintext: 要加密的文本数据
        :return: 加密结果
        """
        plaintext = plaintext.encode('utf-8')
        ciphertext = self.encrypt(plaintext)

        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt_str(self, ciphertext: str) -> str:
        """
        使用私钥解密数据
        :param ciphertext: 要解密的文本数据
        :return: 解密结果
        """
        ciphertext = base64.b64decode(ciphertext)
        plaintext = self.decrypt(ciphertext)
        plaintext = plaintext.decode('utf-8')

        return plaintext


# ====================== 使用示例 ======================
if __name__ == "__main__":
    # # 生成测试密钥对（实际使用时应使用预先生成好的密钥）
    # private_key = rsa.generate_private_key(
    #     public_exponent=65537,
    #     key_size=2048,
    #     backend=default_backend()
    # )
    #
    # # 转换为 PKCS8 格式字符串
    # private_key_str = private_key.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.PKCS8,
    #     encryption_algorithm=serialization.NoEncryption()
    # ).decode('utf-8')
    #
    # public_key_str = private_key.public_key().public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PublicFormat.SubjectPublicKeyInfo
    # ).decode('utf-8')

    private_key_str = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCus2kTKxyRSgQLYKUNd9o8GfmiC6nFUmhkiXf78zzjrfds21LF94JA6jQE6uyWzZIaWMriDJ75YlMTdx/kQT46zua/D4H8HfaTHDizMGKkQXnB8B+zv6mAd9ndQjuzdE+FuXe/vulq9XK/Duy5YwXGzfMLtGfXpJB3OVxFiAkRmBgCot51I/WTwxC6/ki6VwnXpQTeAUKggoug3tw8YCaDB4K3ueRn/gTTbtdGcM3r19iyOUGUWgQEL8SuLcFIn581x4dirV8uMXdGWOs8CcdxTBvLIqFmTs5rsDsWmKwQ6IeEKAtNyJcEsv4fPQ6BNhZq/xfeV/V0lQWYkgw7SxLzAgMBAAECggEAa/fXbZBMVIKQ41M0TpGO32wSOpLItnmKqO/Ipn6aV//xFWaqzkx8RJA52/wwgbbEn+HWaUPxkCCzRSlvHUsxIXkzZEs6Q01lUV+0rxGtNOR+UlyLyzQdlpb7n2HKscqlRvjryCY97euJogigRqarMEWh+s7hCoXa/sQFgbdkG2mFkn+R11Cb7m05aUQ4dbScr+b90qdDKPovlFnUjOgudbdZJOTTeP4sb3eRqhOB8aZUCpWNtfFgxBULr3vKmQGJV9z8anjGzznBNcNEvwVUPMV9l2WPyGwz2joALN/k6xQV70t1jTr2kRuz9EsmtdawiyuJ4F1T+FV9gyjXe4KL+QKBgQDZvenDVqSa14ZqpUS381gG2+7CMpkstLEzQMVegi73Id4420/9SGTs5Olo/MZ+Gd1PzSHul9EcIPwJylCW6+pms1rtWH1K29m4ImU9W/aq2xugGIIJzzwdZrO0G8mlKuZRWciktnUOL6uLveMC8yyf5azPdFr6NXW912UzOOjEPQKBgQDNZYAZWaEhNkdhzRq7jHr1/Cmpho6y6KFJaurvTweH0R/KJ0LvO9pc3zThm521Y9XnKN/61l1XHpJoFOU/uG/OfI6ED3oUB+ikTNyP1QApPvyldUkj6xxY9ZPzpJPRUDMdBSRuZ73/pRLXoPK5PIgFy5LPCqxpYj4OTaPiYWM27wKBgQDXxmSOSCFMtMImkuqbZBHakj5zwdKbQ+DKSqiMNHQ4QR7Ht0X4WLJzM5G+kaheNGFlgIHcwCPgPSumxA/Cz7z0004LIILhGScTWzp6aNTzkbg5ma/b6rrG5Ay3MkZMYEvnWBMGby1mxoS4MY9yT+rr9Z2f4814YFvyqi5GaWH5fQKBgEXzu5zmmanmAomcgO4++eGs78N8wDzOXZ/Teg/mqnnnDxyaIoG3sLbQjgIILb4JMmB321BikYeKMfKgqzL4bZu1cBQp8TnBN8o9IyEZOeTSPtlbCH3jJNRnTuw7sNwopD/N8IppapwWbERj3EaaBvlyS52X1QBPJTNZ3ebLpC6hAoGAfW/yHB4VqDGfmh4pb3M13svplRusDujbjuJcECS1Xk67ZOYrXCEHAtFIwj7xgpJo9krdVJhfI/aZWq26rTRLCxdsHpQP95PHSSYO47pwC8PVQz2D2DhiFwhm27YAAEEg9o12cvmK30Ca/x7mwvpfSjydw7T4bYU5vYta9V/XNHk='
    public_key_str = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArrNpEysckUoEC2ClDXfaPBn5ogupxVJoZIl3+/M84633bNtSxfeCQOo0BOrsls2SGljK4gye+WJTE3cf5EE+Os7mvw+B/B32kxw4szBipEF5wfAfs7+pgHfZ3UI7s3RPhbl3v77pavVyvw7suWMFxs3zC7Rn16SQdzlcRYgJEZgYAqLedSP1k8MQuv5IulcJ16UE3gFCoIKLoN7cPGAmgweCt7nkZ/4E027XRnDN69fYsjlBlFoEBC/Eri3BSJ+fNceHYq1fLjF3RljrPAnHcUwbyyKhZk7Oa7A7FpisEOiHhCgLTciXBLL+Hz0OgTYWav8X3lf1dJUFmJIMO0sS8wIDAQAB'
    # 初始化帮助类
    rsa_helper = RSAHelper(private_key_str, public_key_str)

    # 测试签名验签
    data = b"Hello, RSA!"
    signature = rsa_helper.sign(data)
    print(f"验签结果: {rsa_helper.verify(data, signature)}")  # 应该输出 True

    # 测试加密解密
    plaintext = b"Sensitive data"
    ciphertext = rsa_helper.encrypt(plaintext)
    decrypted = rsa_helper.decrypt(ciphertext)
    print(f"解密结果匹配: {decrypted == plaintext}")  # 应该输出 True

    # 测试签名验签
    data = '文本1'
    signature = rsa_helper.sign_str(data)
    print(f'签名结果: {signature}')
    print(f"验签结果: {rsa_helper.verify_str(data, signature)}")  # 应该输出 True

    # 测试加密解密
    plaintext = "文本2"
    ciphertext = rsa_helper.encrypt_str(plaintext)
    decrypted = rsa_helper.decrypt_str(ciphertext)
    print(f"加密结果: {ciphertext}")
    print(f"解密结果: {decrypted}")
    print(f"解密结果匹配: {decrypted == plaintext}")  # 应该输出 True
