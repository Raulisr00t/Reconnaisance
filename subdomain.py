import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import sys,os
import signal
from colorama import Style, Fore

subdomain_count = 0
lock = threading.Lock()

def signal_capture(sig, frame):
    try:
        print('\nCTRL^C detected by server..')
        sys.exit()
    except SystemExit:
        pass

signal.signal(signal.SIGINT, signal_capture)

def check_word(word, site):
    global subdomain_count
    try:
        request = requests.get(f"https://{word}.{site}", allow_redirects=False, timeout=5)
        if request.status_code < 400:
            with lock:
                subdomain_count += 1
                print(f"Subdomain Found! {word}.{site}")
    except requests.RequestException:
        pass 

def check_words(site, words):
    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(lambda word: check_word(word, site), words)

    print(f"SUBDOMAIN Count: {subdomain_count}")

def main():
    try:
        print(Fore.GREEN + r'''
     \          |  | | |          | |   
      \\        | |__| | __ _  ___| | __
       \\       |  __  |/ _` |/ __| |/ /
        >\/7    | |  | | (_| | (__|   < 
    _.-(6'  \   |_|  |_|\__,_|\___|_|\_|
   (=___._/` \         _   _          
        )  \ |        | | | |         
       /   / |        | |_| |__   ___ 
      /    > /        | __| '_ \ / _ \
     j    < _\        | |_| | | |  __/
 _.-' :      ``.       \__|_| |_|\___|
 \ r=._\        `.
<`\\_  \         .`-.          _____  _                  _   _ 
 \ r-7  `-. ._  ' .  `\       |  __ \| |                | | | |
  \`,      `-.`7  7)   )      | |__) | | __ _ _ __   ___| |_| |
   \/         \|  \'  / `->   |  ___/| |/ _` | '_ \ / _ \ __| |
              ||    .'        | |    | | (_| | | | |  __/ |_|_|
               \\  (          |_|    |_|\__,_|_| |_|\___|\__(_)
                >\  >
            ,.-' >.'
           <.'_.''
             <'                     -----------------------> BY Raulisr00t!
          ''' + Style.RESET_ALL
        )
        site = input("Please enter a URL for subdomain enumeration: ").strip()
        if not site.startswith(('http://', 'https://')):
            site = 'https://' + site

        resp = requests.head(site, allow_redirects=False, verify=True)
        if resp.status_code < 400:
            for header, value in resp.headers.items():
                print(f"{header}: {value}")
        else:
            print("Error: Unable to connect to the site.")
            return

        original = site.split('://')[1]

        path = r'<Your subdomain.txt path>'
        if not os.path.exists(path):
            print(f"Error: The file {path} does not exist.")
            return

        with open(path, 'r') as f:
            words = [line.strip() for line in f.readlines()]

        check_words(original, words)

    except (EOFError, KeyboardInterrupt):
        print("Process stopped by user..")
        sys.exit()
    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit()

if __name__ == "__main__":
    main()
