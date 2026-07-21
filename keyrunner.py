from keyboard import KEY_DOWN, hook
from threading import Thread
from time import sleep
from os import system
from random import randint

# ANSI-codes
G, Y, B, P, BO, RED, R = '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\x1b[1m', '\033[31m', '\033[0m'

keyboard_view = [
    [f'{BO}{G} Q {R}  {BO}{Y} W {R}  {BO}{B} E {R}  {BO}{P} R {R}  {BO}{P} T {R}  {BO}  {P} Y {R}  {BO}{P} U {R}  {BO}{B} I {R}  {BO}{Y} O {R}  {BO}{G} P {R}\n'],
    [f'{BO}{G} A {R}  {BO}{Y} S {R}  {BO}{B} D {R}  {BO}{P} F {R}  {BO}{P} G {R}  {BO}  {P} H {R}  {BO}{P} J {R}  {BO}{B} K {R}  {BO}{Y} L {R}\n'],
    [f'{BO}{G} Z {R}  {BO}{Y} X {R}  {BO}{B} C {R}  {BO}{P} V {R}  {BO}{P} B {R}  {BO}  {P} N {R}  {BO}{P} M {R}']
]
keys_list = 'QWERTYUIOPASDFGHJKLZXCVBNM'

# global vars
time_left = 30
time = 0
key = ''
keys_pressed = 0
right_keys = 0
lose = False
keyboard_in_game_view = []
# this var is needed to change the color of the "YOUR KEYBOARD:" label to red in the event of a miss.
mistake = ''

# time_left – remaining game time, time – total game time for statistics
def timer():
    global time
    global time_left
    global lose
    while not lose:
        if time_left < 2:
            lose = True
        time_left -= 1
        time += 1
        sleep(1)

# changes the color of the corresponding key and collects everything into a single list
def keyboard_maker():
    global keyboard_in_game_view
    global key
    key = keys_list[randint(0, 25)]
    keyboard_in_game_view = keyboard_view.copy()
    for n, row in enumerate(keyboard_in_game_view):
        try:
            _row = ''.join(keyboard_in_game_view[n]).split(' ')
            i = _row.index(key)
            if i != -1:
                _row[i-1] = '\033[4m'
                for _n, i in enumerate(_row):
                    if i == '':
                        _row[_n] = '  '
                    elif len(i) == 1:
                        _row[_n] = f' {i} '
                keyboard_in_game_view[n] = _row
        except:
            pass

def controls(event):
    global right_keys
    global keys_pressed
    global time_left
    global key
    global lose
    global mistake
    if event.event_type == KEY_DOWN:
        if event.name == 'esc':
            lose = True
        elif event.name == key.lower():
            keyboard_maker()
            time_left += 0.25
            keys_pressed += 1
            right_keys += 1
            keyboard_maker()
            mistake = ''
        else:
            keys_pressed += 1
            time_left -= 1
            mistake = RED

def main():
    keyboard_maker()
    Thread(target=timer).start()
    hook(controls)
    while not lose:
        global mistake
        sleep(0.3333333333333)
        system('clear')
        print(f'\n{' ' * 17}{mistake}{BO}YOUR KEYBOARD:\n')
        print(' ', ''.join(keyboard_in_game_view[0]), '  ',
              ''.join(keyboard_in_game_view[1]), '    ',
              ''.join(keyboard_in_game_view[2]), '\n')
        print(f'{' ' * 16}{BO}SECONDS LEFT: {round(time_left)}\nPRESS ESC TO LEAVE')

    system('clear')
    print(f'{BO}GOOD JOB!\nACCURACY: {round(right_keys/keys_pressed*100, 2)}%, RATE: {round(keys_pressed/time, 2)}k/s\n')

if __name__ == '__main__':
    main()
