'''
Йоу, лицензии нет, пользуйтесь на здоровье,
всё равно MaximaTelecom блокирует.
'''


import webbrowser
import time
import pyautogui


def autologin():
    '''Tries to log in MT_FREE for 7 minutes.'''

    webbrowser.open('http://auth.wi-fi.ru/auth?segment=metro')
    time.sleep(10)
    loc_big = pyautogui.locateCenterOnScreen('enter_big.png',
                                             grayscale=True,)
    loc_small = pyautogui.locateCenterOnScreen('enter_small.png')
    try:
        pyautogui.click(loc_big[0], loc_big[1])
        print('OK, waiting for 7 minutes...')
        time.sleep(420)
        autologin()
    except TypeError:
        try:
            pyautogui.click(loc_small[0], loc_small[1])
            print('OK, waiting for 7 minutes...')
            time.sleep(420)
            autologin()
        except TypeError:
            print('''Something has gone wrong, I'll try again in 10 sec...''')
            time.sleep(10)
            autologin()


autologin()
