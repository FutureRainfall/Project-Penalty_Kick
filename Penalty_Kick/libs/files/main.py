import random
import os
import sys
import base64
from rich.console import Console
from files.Login import default as LoggingIn
from files.data_encrypt import data_process as process
import files.anime as anime

console = Console()
def check(sp: str):      #输入检查函数
    spell = str(sp).lower()
    direction = ['left','center','right']
    while True:
        for i in range(3):
            if spell == 'exit' or spell == 'quit':  #输入exit或quit直接退出
                console.print('User quit. ', style='bold red1')
                sys.exit()
            elif spell == direction[i]:             #输入的是left、center或right则返回此次输入结果
                return spell
        console.print('Invalid input. Try again. ', style='red1')         #输错就提示输入错误，重新输入
        spell = str(input()).lower()


def main():                                         #主函数
    football = anime.ball()                         #导入动画模块
    direction = ['left','center','right']
    score = [0,0]
    r = 0
    while True:
        r += 1
        console.rule(f'<<<   ROUND {r}   >>>')
        
        print('--#--You kick:--#--')                    #玩家射门
        bot = random.choice(direction)                  #电脑玩家随机一个方向
        player = check(input())                         #玩家输入一个方向
        football.dir(direction=player, keep=bot)

        if bot == player:                               #方向一样则射门失败
            football.miss()
        else:                                           #方向不一样则射门成功
            football.goal()
            score[0] = score[0] + 1

        gap = 5 - r + 1                                 #计算分差
        if r < 6:                                       #通过分差判断比赛是否还需继续
            if score[1]-score[0]>gap or score[0]-score[1]>gap:
                break
        
        print('--#--You save:--#--')                    #玩家守门，逻辑和射门一样，方向一致则守门成功，不一致则失败
        bot = random.choice(direction)
        player = check(input())
        football.dir(direction=bot, keep=player)

        if bot == player:
            football.save()
        else:
            football.no()
            score[1] = score[1] + 1
        console.print(f'--current score: %d(you) : %d(bot)--\n'%(score[0],score[1]))
        
        g = 5 - r if r < 6 else 0
        if score[1]-score[0]>g or score[0]-score[1]>g:  #如果分差过大，则可直接结束比赛；否则比赛继续
            break

    return r, score[0], score[1]                        #返回比赛总回合数

def penalty_kick():                         
    
    console.print('Tip: using [red]"exit"[/] or [red]"quit"[/] to quit the game whenever you want. ')
    console.print('-- Use a username to register or login. --', style='magenta')
    try:
        user = input('Username: ')
        l = LoggingIn(filepath=r'.\files\users.pk', username=user)     #登录/注册
        isReg, mykey, sha_username = l.login()      #获取是否是新用户、密钥和用户名哈希
        quit_prompt = sha_username.lower()
        if (quit_prompt == b'quit' or quit_prompt == b'exit'):
            sys.exit(0)
        else:
            pass
    except SystemExit:
        console.print('User quit. ', style='bold red1')
        sys.exit()
    except:
        console.print('Invalid return. Please check. ', style='red1')     #万一报错呢 :D
        raise

    record = []                                     #建立列表record[]用来存用户数据
    pos = int()                                     #pos变量用来存当前用户数据在数据文件中的位置
    f = process(mykey)                              #f为一个数据加解密类的实例

    #current_path = os.path.dirname(os.path.abspath(__file__))        #获取当前工作路径，以防后面的文件路径出错
    save_path = r'.\files\save.pk'    #在当前工作路径下的files子目录中存放 /读取存档文件
    
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


    if isReg:                                       #新用户echo
        console.print(f'>> Hello, [bold green]{user}[/bold green]! Welcome to Penalty Kick!! <<')
        console.print(f'>> Type [blue]"left", "center" or "right"[/] to shoot in different directions! <<')
        console.print(f'>> Good luck! <<')

    else:                                           #老用户echo
        console.print(f'>> Welcome back, [bold green]{user}[/bold green]! <<')
        console.print(f'''>> You have played {played} times, with {won} wins and {lost} losses. <<
    >> You have played a {max_last} rounds rally and a blitz with {min_last} rounds. <<
    >> You end the game with an average of {average_last:.2f} rounds. <<''')
    console.print('>> (Tip: using [red]"exit"[/] or [red]"quit"[/] to quit the game whenever you want, while the score will not be saved. ) <<')

    rounds, pscore, bscore = main()                                 #main()函数会执行游戏内容，同时返回此次游戏的回合数
    console.print(f'\n{rounds} rounds played. ', justify='center')
    if pscore > bscore:
        won += 1
        console.rule('GAME OVER. [bright_green]You won! Congrats![/]')
        console.print(f'FINAL SCORE: {pscore}(you) : {bscore}(bot)', justify='center')
    else:
        lost += 1
        console.rule('GAME OVER. [red]You lost. Try again![/]')
        console.print(f'FINAL SCORE: {pscore}(you) : {bscore}(bot)', justify='center')

    total += rounds
    if rounds > max_last:                           #如果此次游戏回合数比存档里的最高回合数多，就刷新纪录
        max_last = rounds
    if min_last == 0 or min_last > rounds:          #如果此次游戏回合数比存档里的最少回合数少，或没有最少回合记录，也刷新纪录
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
    
if __name__ == '__main__': 
    penalty_kick()