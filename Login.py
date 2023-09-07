import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def Cypher(original:bytes, salt:bytes):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    basic = kdf.derive(original)
    return  basic + salt

def login(datafile:str):
    try:
        with open(datafile, 'rb') as saved:
            saved_data = saved.read().split(b'\n')
    except:
        print('未发现所需文件。将创建。')
        with open(datafile, 'wb') as saved:
            saved.write(b'')
            saved_data = []
            
    R = True
    while(R):
        R = False
        username = str.encode(input('请输入用户名：'))
        for i in range(len(saved_data)):
            savedCypher = base64.urlsafe_b64decode(saved_data[i])
            savedSalt = savedCypher[-32:]
            savedCypherUsrsalt = savedCypher[:32] + savedSalt
            savedCypherPwdsalt = savedCypher[32:]
            
            if savedCypherUsrsalt == Cypher(username, savedSalt):
                R = True
                password = str.encode(input('请输入密码：'))
                if savedCypherPwdsalt == Cypher(password, savedSalt):
                    print('登录成功。')
                    return_salt = savedSalt
                    return (bool(True), return_salt)
                else:
                    print('密码错误。')
                break
            
        if not R:
            reg = input('未发现用户。是否进行注册？(Y/N):').upper()
            while(True):
                if reg == 'Y':
                    password = str.encode(input('请输入密码：'))
                    salt = os.urandom(32)
                    return_salt = salt
                    CypherUsr = Cypher(username, salt)
                    CypherPwd = Cypher(password, salt)
                    data = base64.urlsafe_b64encode(CypherUsr[:32] + CypherPwd)
                    saved_data.append(data)
                    print('已成功注册。')
                    with open('users.txt', 'wb') as writer:
                        writer.write(b'\n'.join(saved_data).lstrip(b'\n'))
                    break
                elif reg == 'N':
                    R = True
                    break
                else:
                    reg = input('输入错误，请输入(Y/N):').upper()
            
    return (bool(False), return_salt)

if __name__ == '__main__':
    isLogin, key = login('users.txt')
    print(isLogin, key)