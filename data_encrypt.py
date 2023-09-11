from cryptography.fernet import Fernet

#数据加解密
class data_process:

    #初始化参数为密钥
    def __init__(self, key: bytes) -> None:
        self._key = key

    #加密
    def Encrypt(self, content: bytes) -> bytes:
        f = Fernet(self._key)
        encrypted = f.encrypt(content)
        return encrypted

    #解密
    def Decrypt(self, encrypted: bytes) -> bytes:
        f = Fernet(self._key)
        decrypted = f.decrypt(encrypted)
        return decrypted