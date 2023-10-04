import time
from threading import Thread
import os
from datetime import datetime, timedelta
import subprocess
from dotenv import dotenv_values


def sync_user_ids():
    user_ids_file = 'user_ids.txt'

    with open(user_ids_file, 'r') as f:
        user_ids = [value.strip() for line in f.readlines() for value in line.strip().split(',') if value.strip()]

    if user_ids:
        with open('../.env', 'r') as f:
            env_lines = f.readlines()

        env = []
        update_allowed_ids = False

        for line in env_lines:
            if line.startswith('#') or '=' not in line:
                env.append(line)
            else:
                key, value = line.strip().split('=', 1)
                if key.strip() == 'ALLOWED_TELEGRAM_USER_IDS':
                    current_allowed_ids = value.split(',')
                    if len(current_allowed_ids) < len(user_ids):
                        current_allowed_ids.extend(user_ids)
                        current_allowed_ids = list(set(current_allowed_ids))
                        updated_value = ','.join(current_allowed_ids) if current_allowed_ids else ""
                        env.append(f"{key}={updated_value}\n")
                        update_allowed_ids = True
                else:
                    env.append(line)

        if update_allowed_ids:
            with open('../.env', 'w') as f:
                f.writelines(env)

            print('.env file updated, restarting docker containers...')
            subprocess.run(["docker-compose", "restart"])


def start_sync_thread():
    thread = Thread(target=sync_user_ids_loop)
    thread.start()


def sync_user_ids_loop():
    while True:
        sync_user_ids()
        time.sleep(1)  # раз в секунду
