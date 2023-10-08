import base64
import getpass
import os
import re
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class default(object):
    #初始化，filepath为用户信息文件路径，username为用户名
    def __init__(
        self, 
        filepath: str, 
        username: str, 
        ) -> None:
        current_path = os.path.dirname(__file__)
        self._filepath = current_path + filepath
        self._username = username

    #加密函数
    def __Cypher(self, original: bytes, salt: bytes):
        #使用PBKDF2HMAC函数生成密钥推导kdf
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        #将原始信息original用kdf推导产生密钥basic
        basic = kdf.derive(original)
        #返回的是推导后的密钥basic和盐值salt的bytes类型连接
        return  basic + salt

    #哈希计算函数
    def __SHA(self, data: bytes) -> bytes:
        hash = hashes.Hash(algorithm=hashes.SHA256())
        hash.update(data)
        return (hash.finalize())

    #正则函数
    def __RegEx(self, user: str) -> bytes:
        temp = user

        #如果输入了quit或exit直接结束程序
        if (temp == 'quit' or temp == 'exit'):
            sys.exit()

        m = re.findall(r'\W', temp)
        while m:
            print('** Username can only contain Chinese characters, English letters, digits and underscores. **')
            temp = input('Username: ')
            m = re.findall(r'\W',temp)
            if temp.lower() == 'exit' or temp.lower() == 'quit':
                sys.exit()
        return str.encode(temp)


    #主要的登录函数
    def login(self) -> tuple[bool, bytes, bytes]:
        #读取存储信息，每一行为一个用户的信息，传入saved_data列表储存
        try:
            with open(self._filepath, 'rb') as saved:
                saved_data = saved.read().split(b'\n')
        
        #没找到文件就建一个
        except:
            print('User profile not found. Creating one. ')
            with open(self._filepath, 'wb') as saved:
                saved.write(b'')
                saved_data = []


    #判断用户输入的用户名是否存在，存在则登录，不存在则注册
        while(True):
            #调用正则函数判断用户名是否合规
            username = self.__RegEx(self._username)
            isLogged = False
            r = True

            #遍历saved_data，每条信息base64解码后截取数据，前32位为加密的用户名，32~64位为加密密码，后32位为盐值
            for i in range(len(saved_data)):
                savedCypher = base64.urlsafe_b64decode(saved_data[i])
                sha_username = savedCypher[:32]

                #计算输入的用户名的哈希，若结果和存储的哈希值一致则判断用户名已存在，读取此用户的密码+盐值组合和单独盐值
                if sha_username == self.__SHA(username):
                    r = False
                    savedSalt = savedCypher[-32:]
                    savedCypherPwdsalt = savedCypher[32:]
                    password = str.encode(getpass.getpass('Password(input will be hidden): '))
                    if(password == 'quit' or password == 'exit'):
                        sys.exit()

                    #使用用户输入的密码和储存的盐值进行加密，若结果和存储的加密密码一致则判断登录成功
                    if savedCypherPwdsalt == self.__Cypher(password, savedSalt):
                        print('Login successfully. ')
                        #返回新注册为False以及盐值base64编码
                        return(False, base64.urlsafe_b64encode(savedSalt), sha_username)
                    else:
                        print('Incorrect password. Login again. ')
                        isLogged = False
                        break

            #这行是在输错密码以后执行的
            if not isLogged and not r:
                self._username = input('Username: ')

            #这里开始是注册过程
            if not isLogged and r:
                reg = input('No username match. Register? (Y/N):').upper()
                
                #输入的不是Y或N提示输入错误，重新输入
                while(reg != 'Y' and reg != 'N'):
                    reg = input('Invalid input. Please input (Y/N):').upper()

                #输入Y开始注册
                if reg == 'Y':
                    while True:
                        password = str.encode(getpass.getpass('Set a password(input will be hidden): '))
                        #重复确认密码
                        check_pwd = str.encode(getpass.getpass('Confirm password(input will be hidden): '))
                        if password == check_pwd:
                            break
                        else:
                            print('Confirmation failed. \n')
                    #盐值是32位随机值
                    salt = os.urandom(32)
                    #计算用户名哈希值
                    sha_usr = self.__SHA(username)
                    #使用加密函数加密密码
                    CypherPwd = self.__Cypher(password, salt)
                    data = base64.urlsafe_b64encode(sha_usr + CypherPwd)
                    #将已加密的且base64编码的新用户注册信息添加为saved_data的新元素并整个覆写回self._filepath
                    saved_data.append(data)
                    print('Register successfully. ')
                    with open(self._filepath, 'wb') as writer:
                        writer.write(b'\n'.join(saved_data).lstrip(b'\n'))

                    #返回新注册为True以及盐值base64编码
                    return(True, base64.urlsafe_b64encode(salt), sha_usr)

                #输入N不注册，此时重新开始输入用户名，回到最外层while(True)
                elif reg == 'N':
                    self._username = input('Username: ')

#测试用，被调用时无效
if __name__ == '__main__':
    l = default('users.txt', input('Username: '))
    isReg, key, sha_username = l.login()
    print(isReg, key, sha_username)