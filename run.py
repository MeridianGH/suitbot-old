import subprocess
import sys
import os
import suitbot
from modules.log.logging import get_log_path, get_time, send_log, log_traceback


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


def start_lavalink():
    lavalink = subprocess.Popen(['java', '-jar', 'Lavalink.jar'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    while True:
        line = str(lavalink.stdout.readline())
        if 'Started Launcher' in line:
            send_log(f'[Status] Successfully started music server \'WaveLink\'')
            return True
        elif 'FAILED' in line or 'failed' in line:
            send_log(f'[Error ] Failed to start music server \'WaveLink\'.')
            send_log(f'     ->    [ Info ] Music commands might not work!', time=False)
            return False


if __name__ == '__main__':
    os.chdir(resource_path('./music/wavelink/'))
    send_log(f'[Status] Loading extensions...')
    start_lavalink()
    suitbot.run()
