import sys
import os
from datetime import datetime
imprt = 'from modules.log.logging import get_log_path, get_time, send_log, log_traceback'


def get_log_path():
    if sys.platform == 'win32':
        userprofile = os.getenv('UserProfile')
        return f'{userprofile}/Documents/GitHub/suitbot/modules/log'
    elif sys.platform.startswith('linux'):
        return '/home/pi/suitbot/modules/log'
    else:
        return None


def send_log(string, time=True, prnt=True):
    if time:
        time = f'[{get_time()}] '
    else:
        time = ''

    with open(f'{get_log_path()}/{log_name}', 'a') as log:
        log.write(f'{time}{string}\n')

    if prnt:
        return print(f'{time}{string}')
    else:
        return f'{time}{string}'


def log_traceback(traceback, command):
    time = get_time().replace(':', '_')
    file_name = f'traceback_{time}.txt'
    with open(f'{get_log_path()}/tracebacks/{file_name}', 'a') as log:
        for line in traceback:
            log.write(line)
    return send_log(f'[Error ] Ignoring exception in command \'{command}\'.')


def get_time():
    return datetime.now().strftime('%H:%M:%S')


log_name = 'log_' + datetime.now().strftime('%d_%m_%y') + '.txt'
open(f'{get_log_path()}/{log_name}', 'w').close()
