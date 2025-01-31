# -*- coding:utf-8 -*-

import sys
import requests
import re
import random
import string
from multiprocessing.dummy import Pool
from colorama import Fore, init

init(autoreset=True)
fr = Fore.RED
fg = Fore.GREEN
requests.urllib3.disable_warnings()

ascii = """
 _     _      _               _    ______ _           _           
| |   (_)    | |             | |   |  ___(_)         | |          
| |    _  ___| |__   ___ _ __| |_  | |_   _ _ __   __| | ___ _ __ 
| |   | |/ _ \ '_ \ / _ \ '__| __| |  _| | | '_ \ / _` |/ _ \ '__|
| |___| |  __/ |_) |  __/ |  | |_  | |   | | | | | (_| |  __/ |   
\_____/_|\___|_.__/ \___|_|   \__| \_|   |_|_| |_|\__,_|\___|_|                                                                   
"""

print(ascii)
try:
    # Input site list
    if len(sys.argv) > 1:
        target_file_path = sys.argv[1]
    else:
        target_file_path = input("Enter Your Site List >> ")

    with open(target_file_path, mode='r', encoding='utf-8') as file:
        target = [line.strip() for line in file.readlines()]

    # User-Agent options
    user_agents = [
        'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
    ]

    # Display User-Agent options
    print("\nChoose a User-Agent:")
    for i, ua in enumerate(user_agents, 1):
        print(f"{i}. {ua}")
    
    # Input User-Agent choice
    try:
        ua_choice = int(input("Enter the number for User-Agent (default 1): ")) - 1
        if ua_choice not in range(len(user_agents)):
            print("Invalid choice. Using default User-Agent.")
            ua_choice = 0
    except ValueError:
        print("Invalid input. Using default User-Agent.")
        ua_choice = 0

    # Set selected User-Agent
    user_agent = user_agents[ua_choice]

    # Load paths from path.txt
    try:
        with open("path.txt", mode='r', encoding='utf-8') as path_file:
            Pathlist = [line.strip() for line in path_file.readlines()]
    except FileNotFoundError:
        print("Error: 'path.txt' file not found.")
        Pathlist = []

    def ran(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    class EvaiLCode:
        def __init__(self):
            self.headers = {
                'User-Agent': user_agent}

        def URLdomain(self, site):
            if site.startswith("http://"):
                site = site.replace("http://", "")
            elif site.startswith("https://"):
                site = site.replace("https://", "")
            pattern = re.compile('(.*)/')
            while re.findall(pattern, site):
                sitez = re.findall(pattern, site)
                site = sitez[0]
            return site

        def checker(self, site):
            try:
                url = "http://" + self.URLdomain(site)
                for Path in Pathlist:
                    check = requests.get(url + Path, headers=self.headers, verify=False, timeout=15).content
                    if '-rw-r--r--' in check.decode():  
                        print('[>>] {} --> {}[Vuln]'.format(url, fg)) 
                        open('Shells.txt', 'a').write(url + Path + "\n")
                        break
                    else:
                        print('[x] {} --> {}[Not ShellS]'.format(url, fr))

            except:
                pass

    Control = EvaiLCode()

    def FlashKiss(site):
        try:
            Control.checker(site)
        except:
            pass

    # Set threads to 100 automatically
    mp = Pool(100)
    mp.map(FlashKiss, target)
    mp.close()
    mp.join()
    input("Check Shells.txt File")

except Exception as e:
    print(f"An error occurred: {e}")
