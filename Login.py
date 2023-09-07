import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#加密函数
def Cypher(original:bytes, salt:bytes):
    #使用PBKDF2HMAC函数生成密钥推导kdf
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    #将原始信息original用kdf推导产生密钥basic
    basic = kdf.derive(original)
    #返回的是推导后的密钥basic和盐值salt的bytes类型连接
    return  basic + salt

#主要的登录函数，需要的登录信息存储文件名称datafile作为参数
def login(datafile:str) -> tuple[bool, bytes]:
    #读取存储信息，每一行为一个用户的信息，传入saved_data列表储存
    try:
        with open(datafile, 'rb') as saved:
            saved_data = saved.read().split(b'\n')
    
    #没找到文件就建一个
    except:
        print('未发现所需文件。将创建。')
        with open(datafile, 'wb') as saved:
            saved.write(b'')
            saved_data = []
            
#判断用户输入的用户名是否存在，存在即已注册则登录，不存在则注册
#设置一个r代表用户是否已注册，初始值为True
    r = True
    while(r):
        r = False
        username = str.encode(input('请输入用户名：'))
        
        #遍历saved_data，每条信息base64解码后截取数据，前32位为加密的用户名，32~64位为加密密码，后32位为盐值
        for i in range(len(saved_data)):
            savedCypher = base64.urlsafe_b64decode(saved_data[i])
            savedSalt = savedCypher[-32:]
            savedCypherUsrsalt = savedCypher[:32] + savedSalt
            savedCypherPwdsalt = savedCypher[32:]
            
            #使用用户输入的用户名和储存的盐值进行加密，若结果和存储的加密用户名一致则判断用户名已存在，R设为True代表此用户已注册
            if savedCypherUsrsalt == Cypher(username, savedSalt):
                r = True
                password = str.encode(input('请输入密码：'))
                
                #使用用户输入的密码和储存的盐值进行加密，若结果和存储的加密密码一致则判断登录成功
                if savedCypherPwdsalt == Cypher(password, savedSalt):
                    print('登录成功。')
                    return_salt = savedSalt
                    return(r, savedSalt)
                else:
                    print('密码错误。')
                break
            
        #若r为False即未注册，则执行以下注册部分
        if r == False:
            reg = input('未发现用户。是否进行注册？(Y/N):').upper()
            while(True):
                #输入Y进行注册
                if reg == 'Y':
                    password = str.encode(input('请输入密码：'))
                    salt = os.urandom(32)
                    return_salt = salt
                    CypherUsr = Cypher(username, salt)
                    CypherPwd = Cypher(password, salt)
                    data = base64.urlsafe_b64encode(CypherUsr[:32] + CypherPwd)
                    
                    #将已加密的且base64编码的新用户注册信息添加为saved_data的新元素并整个覆写回datafile
                    saved_data.append(data)
                    print('已成功注册。')
                    with open(datafile, 'wb') as writer:
                        writer.write(b'\n'.join(saved_data).lstrip(b'\n'))
                    break
                
                #输入N不注册，R设为True并跳出注册循环，此时退回上层while(R)，重新开始输入用户名
                elif reg == 'N':
                    r = True
                    break
                
                #输入的不是Y或N提示输入错误，重新输入
                else:
                    reg = input('输入错误，请输入(Y/N):').upper()
                    
    #返回r值（True为登录，False为新用户注册）以及盐值
    return(r, return_salt)

#测试用
if __name__ == '__main__':
    isLogin, key = login('users.txt')
    print(isLogin, key)