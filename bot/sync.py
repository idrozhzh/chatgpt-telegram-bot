import time
from threading import Thread
import os
from datetime import datetime, timedelta
import subprocess


def sync_user_ids():
    last_sync = datetime.min
    sync_interval = timedelta(seconds=1)  # раз в секунду

    if datetime.now() - last_sync > sync_interval:
        last_sync = datetime.now()

        user_ids_file = 'user_ids.txt'
        env_file = '.env'

        with open(user_ids_file, 'r') as f:
            user_ids = [line.strip() for line in f.readlines() if line.strip()]

        if user_ids:
            with open(env_file, 'r') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if line.startswith('ALLOWED_TELEGRAM_USER_IDS'):
                    allowed_ids = line.split('=')[1].strip().split(',')
                    allowed_ids.extend(user_ids)
                    allowed_ids = list(set(allowed_ids))  # убрать дубликаты

                    allowed_ids_str = ','.join(allowed_ids)
                    lines[i] = f'ALLOWED_TELEGRAM_USER_IDS={allowed_ids_str}\n'

                    with open(env_file, 'w') as f:
                        f.write(lines)

                    print('.env file updated, restarting docker containers...')
                    subprocess.run(["docker-compose", "restart"])


def start_sync_thread():
    thread = Thread(target=sync_user_ids_loop)
    thread.start()


def sync_user_ids_loop():
    while True:
        sync_user_ids()
        time.sleep(1)  # раз в секунду
