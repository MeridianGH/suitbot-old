import subprocess
import os
import suitbot


def start_lavalink():
    lavalink = subprocess.Popen('java -jar Lavalink.jar', stdout=subprocess.PIPE)
    while True:
        line = str(lavalink.stdout.readline())
        if 'Started Launcher' in line:
            print('[Status] Successfully started music server \'WaveLink\'')
            return True
        elif 'FAILED' in line:
            print('[Error ] Failed to start music server \'WaveLink\'.\n[ Info ] Music commands might not work!')
            return False


if __name__ == '__main__':
    os.chdir('./music/wavelink')
    print('[Status] Loading extensions...')
    start_lavalink()
    suitbot.run()
