import time
from threading import Thread
import os
from datetime import datetime, timedelta
import subprocess
from dotenv import dotenv_values


def sync_user_ids():
    user_ids_file = 'user_ids.txt'

    with open(user_ids_file, 'r') as f:
        user_ids = [line.strip() for line in f.readlines() if line.strip()]

    if user_ids:
        env = dotenv_values(".env")
        allowed_ids = env.get('ALLOWED_TELEGRAM_USER_IDS', '').split(',')

        if len(allowed_ids) < len(user_ids):
            allowed_ids.extend(user_ids)
            allowed_ids = list(set(allowed_ids))

            env['ALLOWED_TELEGRAM_USER_IDS'] = ','.join(allowed_ids)
            with open('.env', 'w') as f:
                for k, v in env.items():
                    f.write(f"{k}={v}\n")

            print('.env file updated, restarting docker containers...')
            subprocess.run(["docker-compose", "restart"])


def start_sync_thread():
    thread = Thread(target=sync_user_ids_loop)
    thread.start()


def sync_user_ids_loop():
    while True:
        sync_user_ids()
        time.sleep(1)  # раз в секунду
