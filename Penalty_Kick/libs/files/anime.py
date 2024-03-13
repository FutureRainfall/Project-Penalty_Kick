import time
import os
class man(object):

    def keep(self, dir: str, pos: int):
        print('\r\t\t\t', end='', flush=True)
        if dir == 'right': 
            for _ in range(pos-1):
                print('    ', end='', flush=True)
            print('>=|O', end='', flush=True)
        
        if dir == 'left': 
            # for _ in range(3):
            print(' ', end='', flush=True)
            for _ in range(pos):
                print('\b\b\b', end='', flush=True)
            print('O|=<', end='', flush=True)
            
        elif dir == 'center':
            if pos == 1:
                print('O', end='', flush=True)
            elif pos == 2:
                print('=O=', end='', flush=True)
            else:
                print('/=O=\\', end='', flush=True)

keeper = man()

class ball(object):

    def dir(self, direction: str, keep: str):
        if direction == keep:
            is_goal = False
        else:
            is_goal = True
        
        if direction == 'left':
            self._left(keep, is_goal)
        elif direction == 'center':
            self._center(keep, is_goal)
        elif direction == 'right':
            self._right(keep, is_goal)
        
    def _left(self, k: str, isgoal: bool):
        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 1)
        print('\n\n')
        print('\t\t\t___')
        print('\t\t       /   \\')
        print('\t\t       \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 2)
        print('\n')
        print('\t\t    ___')
        print('\t\t   /   \\')
        print('\t\t   \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 3)
        print('')
        print('\t\t ___')
        print('\t\t/   \\')
        print('\t\t\\___/')
        time.sleep(0.2)

        if isgoal == True:
            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||')
            keeper.keep(k, 4)
            print('\r\t     ___')
            print('\t    /   \\')
            print('\t    \\___/')
            time.sleep(0.2)

            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||', end='')
            print('\r\t ___')
            keeper.keep(k, 5)
            print('\r\t/   \\')
            print('\t\\___/')


    def _right(self, k: str, isgoal: bool):
        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 1)
        print('\n\n')
        print('\t\t\t___')
        print('\t\t       /   \\')
        print('\t\t       \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 2)
        print('\n')
        print('\t\t\t    ___')
        print('\t\t\t   /   \\')
        print('\t\t\t   \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 3)
        print('')
        print('\t\t\t\t___')
        print('\t\t\t       /   \\')
        print('\t\t\t       \\___/')
        time.sleep(0.2)

        if isgoal == True:
            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||')
            keeper.keep(k, 4)
            print('\r\t\t\t\t    ___')
            print('\t\t\t\t   /   \\')
            print('\t\t\t\t   \\___/')
            time.sleep(0.2)

            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||', end='')
            print('\r\t\t\t\t\t ___')
            keeper.keep(k, 5)
            print('\r\t\t\t\t\t/   \\')
            print('\t\t\t\t\t\\___/')


    def _center(self, k: str, isgoal: bool):
        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 1)
        print('\n\n')
        print('    \t\t\t___')
        print('\t\t       /   \\')
        print('\t\t       \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 2)
        print('\n')
        print('\t\t\t___')
        print('\t\t       /   \\')
        print('\t\t       \\___/')
        time.sleep(0.2)

        os.system('cls')
        for _ in range(2):
            print('||\t\t\t\t\t\t   ||')
        print('||=================================================||')
        keeper.keep(k, 3)
        print('')
        print('\t\t\t___')
        print('\t\t       /   \\')
        print('\t\t       \\___/')
        time.sleep(0.2)

        if isgoal == True:
            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||')
            keeper.keep(k, 4)
            print('\r\t\t\t___')
            print('\r\t\t       /   \\')
            print('\t\t       \\___/')
            time.sleep(0.2)

            os.system('cls')
            for _ in range(2):
                print('||\t\t\t\t\t\t   ||')
            print('||=================================================||', end='')
            print('\r\t\t\t___')
            keeper.keep(k, 5)
            print('\r\t\t       /   \\')
            print('\t\t       \\___/')
            
    
    def goal(self):
        time.sleep(1)
        os.system('cls')
        goal = r'''
           ______            ______                           
          /                 /      \             /\           |                 |	|
         /                 /        \           /  \          |                 |	|
        /      _______    /          \         /    \         |                 |	|
        \           /     \          /        /______\        |                 |	|
         \         /       \        /        /        \       |
          \_______/         \______/        /          \      |_________        o	o
        '''
        print(goal)
        time.sleep(1)

    def save(self):
        time.sleep(1)
        os.system('cls')
        save = r'''
           ________                                            _________        |   |
         /                     /\           \          /      |                 |   |
        |                     /  \           \        /       |                 |   |
         \_________          /    \           \      /        |________         |   |
                   \        /______\           \    /         |                 |   |
                    |      /        \           \  /          |                 
         __________/      /          \           \/           |__________       o   o
        '''
        print(save)
        time.sleep(1)
        
    def no(self):
        time.sleep(1)
        os.system('cls')
        no = r'''
        |\          |         ______
        | \         |        /      \
        |   \       |       /        \
        |     \     |      /          \
        |       \   |      \          /
        |         \ |       \        /
        |          \|        \______/       o     o     o
        '''
        print(no)
        time.sleep(1)
        
    def miss(self):
        time.sleep(1)
        os.system('cls')
        miss = r'''
        |\            /|         |           ________          ________         |   |
        | \          / |         |          /                 /                 |   |
        |  \        /  |         |         |                 |                  |   |
        |   \      /   |         |          \_________        \_________        |   |
        |    \    /    |         |                    \                 \       |   |
        |     \  /     |         |                     |                 |
        |      \/      |         |          __________/       __________/       o   o
        '''
    
        print(miss)
        time.sleep(1)

#测试用，被调用时无效
if __name__ == '__main__':
    football = ball()
    football.dir(direction='right', keep='left')
    football.miss()
