import random
import os
import sys
import base64
import files.Login as Login
from files.data_encrypt import data_process as process
import files.anime as anime


def check(sp: str):      #输入方向拼写检查
    spell = str(sp).lower()
    while True:
        for i in range(3):
            if spell == 'exit' or spell == 'quit':  #输入exit或quit直接退出
                sys.exit()
            elif spell == direction[i]:             #输入的是left、center或right则返回此次输入结果
                return spell
        print('Invalid input. Try again. ')         #输错就提示输入错误，重新输入
        spell = str(input()).lower()


def kick(rd):   #游戏进行函数，参数为第几回合数
    football = anime.ball()
    print('--#--You kick:--#--')                    #玩家射门
    ai = random.choice(direction)                   #电脑玩家随机一个方向
    you = check(input())                            #玩家输入一个方向
    football.dir(direction=you, keep=ai)
    # print('(You kicked ' + str(you) + ')  ' + '(AI saved ' + ai + ')')

    if ai == you:                                   #方向一样则射门失败
        # print('[[<<< Oops! >>>]]')
        football.miss()
    else:                                           #方向不一样则射门成功
        # print(r'[[<<< *\/* Goal! :D >>>]]')
        football.goal()
        score[0] = score[0] + 1

    gap = 5 - rd + 1                                #计算分差，判断比赛是否还需继续
    if rd < 6:
        if score[1]-score[0]>gap or score[0]-score[1]>gap:
            return 0
    
    print('--#--You save:--#--')                    #玩家守门，逻辑和射门一样，方向一致则守门成功，不一致则失败
    ai = random.choice(direction)
    you = check(input())
    football.dir(direction=ai, keep=you)
    # print('(AI kicked: ' + ai + ')  ' + 'You saved: ' + str(you) + ')')
    if ai == you:
        # print('[[<<< Saved! ;P >>>]]')
        football.save()
    else:
        # print('[[<<< No... T_T >>>]]')
        football.no()
        score[1] = score[1] + 1
    print('--current score: %d(you) : %d(AI)--\n'%(score[0],score[1]))


def main():                                         #主函数
    g = 5                                           #五局三胜
    r = 1
    for r in range(1,6):
        print(f'<<<\tROUND {r}\t    >>>')
        kick(r)
        g = 5 - r

        
        if score[1]-score[0]>g or score[0]-score[1]>g:  #如果分差过大，则可直接结束比赛；否则比赛继续
            break
    while r >= 5 and score[0] == score[1]:
        r += 1
        print(f'<<<\tROUND {r}\t    >>>')
        kick(r)

    return r                                        #返回比赛总回合数

if __name__ == '__main__':                          #判断是否为主执行函数
    score = [0,0]
    direction = ['left','center','right']
    print('Tip: using "exit" or "quit" to quit the game whenever you want. ')
    print('-- Use a username to register or login. --')
    try:
        user = input('Username: ')
        l = Login.default(filepath=r'\users.pk', username=user)     #登录/注册
        isReg, mykey, sha_username = l.login()      #获取是否是新用户、密钥和用户名哈希
    except:
        print('Invalid return. Please check. ')     #万一报错呢 :D
        raise

    record = []                                     #建立列表用来存用户数据
    pos = int()                                     #这个变量用来存当前用户数据在数据文件中的位置
    f = process(mykey)                              #一个数据加解密类的实例

    current_path = os.path.dirname(__file__)
    save_path = current_path + r'\files\save.pk'
    
    if isReg:                                       #新用户注册
        record = [0, 0, 0, 0, 0]                    #新用户直接新建游戏数据
        try:
            with open(save_path, 'rb') as savefile: #读存档
                savedata = base64.urlsafe_b64decode(savefile.read())
        except:
            with open(save_path, 'wb') as savefile:
                savefile.write(b'')                 #没存档就新建
            savedata = b''

    else:                                           #不是新用户注册
        with open(save_path, 'rb') as savefile:     #读存档
            savedata = base64.urlsafe_b64decode(savefile.read())

        #每132位为一个用户的数据
        for i in range(int(len(savedata.rstrip())/132)):
            pos = i * 132
            if savedata[pos:][:32] == sha_username: #前32位为用户名哈希，如果和输入用户名的哈希一样则确定为这个用户的数据
                #把用户名哈希后面的内容解密，即为[ ,int,int,int,int,int]的数据形式，将其拆分为列表
                record = f.Decrypt(savedata[pos+32:pos+132]).strip().split(b' ')
                record = [int(j) for j in record]   #转为int
                break
            else:
                pass
    
    won, lost, max_last, min_last, total = record   #变量存取
    played = won + lost                             #总局数played，和总回合数total区分开
    if min_last > 0:
        average_last = total / played               #总回合数/总局数，为平均一局能持续几回合
    else:
        average_last = 0


    if isReg:                                       #新老用户不同显示
        print(f'>> Hello, {user}! Welcome to Penalty Kick!! <<')
        print('>> Type "left", "center" or "right" to shoot in different directions! <<')
        print('>> Good luck! <<')

    else:
        print(f'>> Welcome back, {user}! <<')
        print('''>> You have played {0} times, with {1} wins and {2} losses. <<
    >> You have played a {3} rounds rally and a blitz with {4} rounds. <<
    >> You end the game with an average of {5:.2f} rounds. <<'''
    .format(played, won, lost, max_last, min_last, average_last))
    print('>> (Tip: using "exit" or "quit" to quit the game whenever you want, while the score will not be saved. ) <<')

    rounds = main()                                 #main()函数会执行游戏内容，同时返回此次游戏的回合数
    print(f'\n{rounds} rounds played. ')
    if score[0] > score[1]:
        won += 1
        print('GAME OVER. You won! Congrats!')
        print('-----------------------------')
        print('FINAL SCORE: {0}(you) : {1}(AI)'.format(score[0], score[1]))
        print('-----------------------------')
    else:
        lost += 1
        print('GAME OVER. You lost. Try again!')
        print('-----------------------------')
        print('FINAL SCORE: {0}(you) : {1}(AI)'.format(score[0], score[1]))
        print('-----------------------------')

    total += rounds
    if rounds > max_last:                           #如果此次游戏回合数比存档里的最高回合数多，就刷新纪录
        max_last = rounds
    if min_last == 0 or min_last > rounds:          #如果此次游戏回合数比存档里的最少回合数少，也刷新纪录
        min_last = rounds

    #将游戏结果保存为bytes格式
    result = str.encode(' {0} {1} {2} {3} {4}'.format(won, lost, max_last, min_last, total))
    result = f.Encrypt(result)                      #加密
    result = sha_username + result                  #用户哈希和加密后的游戏数据
    if isReg:                                       #注册用户直接把数据放在所有存档的后面
        savedata += result
    else:                                           #登录用户则要覆盖自己之前的数据
        #每个玩家的数据都占132位，pos之前是此用户前面其他玩家的数据，pos+132后是后面其他玩家的数据
        savedata = savedata[:pos] + result + savedata[pos+132:]

    with open(save_path, 'wb') as savefile:  #写入数据
        savefile.write(base64.urlsafe_b64encode(savedata))
    os.system('pause')