import subprocess
import sys
import os
import suitbot


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


def start_lavalink():
    lavalink = subprocess.Popen(['java', '-jar', 'Lavalink_fixed.jar'], stdout=subprocess.PIPE)
    while True:
        line = str(lavalink.stdout.readline())
        if 'Started Launcher' in line:
            print('[Status] Successfully started music server \'WaveLink\'')
            return True
        elif 'FAILED' in line:
            print('[Error ] Failed to start music server \'WaveLink\'.\n[ Info ] Music commands might not work!')
            return False


if __name__ == '__main__':
    os.chdir(resource_path('./music/wavelink/'))
    print('[Status] Loading extensions...')
    start_lavalink()
    suitbot.run()
