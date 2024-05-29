# Subdomain Enumeration Tool

This tool is designed for subdomain enumeration. It allows you to find valid subdomains for a given site by checking a list of potential subdomains. The tool uses multi-threading to perform the checks concurrently, speeding up the process.

## Features

- Multi-threaded subdomain enumeration using `ThreadPoolExecutor`
- Handles keyboard interrupts gracefully
- Displays HTTP headers of the target site
- Color-coded output using `colorama`
- Handles errors and exceptions robustly

## Requirements

- Python 3.7+
- `requests` library
- `colorama` library

You can install the required libraries using pip:

```sh
pip install requests colorama
Usage
Clone the repository:

git clone https://github.com/yourusername/subdomain-enumeration-tool.git
cd subdomain-enumeration-tool
Prepare a file with potential subdomains (one per line). By default, the tool looks for a file at C:\Users\Student\Desktop\student\dns.txt. You can modify the path in the script if needed.

Run the tool:


python subdomain_enumeration.py
Enter the URL of the site you want to enumerate subdomains for when prompted.
Example


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

Please enter a URL for subdomain enumeration: example.com
Date: Tue, 29 May 2024 12:34:56 GMT
Server: Apache/2.4.41 (Ubuntu)
...

Subdomain Found! www.example.com
Subdomain Found! mail.example.com
SUBDOMAIN Count: 2
Code Explanation
Imports and Global Variables

import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import sys, os
import signal
from colorama import Style, Fore

subdomain_count = 0
lock = threading.Lock()
requests: Used to make HTTP requests.
ThreadPoolExecutor: Used for concurrent execution of tasks.
threading: Provides threading support.
sys, os: Standard libraries for system operations.
signal: Used to handle signal interrupts.
colorama: Used for color-coded terminal output.
subdomain_count: Global variable to keep track of the number of subdomains found.
lock: A threading lock to manage concurrent access to shared resources.
Signal Handling

def signal_capture(sig, frame):
    try:
        print('\nCTRL^C detected by server..')
        sys.exit()
    except SystemExit:
        pass

signal.signal(signal.SIGINT, signal_capture)
signal_capture: Function to handle CTRL+C interrupts.
signal.signal: Registers the signal_capture function to handle SIGINT signals.
Subdomain Checking

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
check_word: Function to check if a subdomain exists.
requests.get: Makes an HTTP GET request to the subdomain.
allow_redirects=False: Prevents following redirects.
timeout=5: Sets a timeout for the request.
subdomain_count: Increments the count if a subdomain is found.
Concurrent Execution

def check_words(site, words):
    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(lambda word: check_word(word, site), words)

    print(f"SUBDOMAIN Count: {subdomain_count}")
check_words: Function to check multiple subdomains concurrently.
ThreadPoolExecutor(max_workers=500): Creates a thread pool with 500 workers.
executor.map: Maps the check_word function to the list of words.
Main Function
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

        path = r'C:\Users\Student\Desktop\student\dns.txt'
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
main: The main function that ties everything together.
Displays an ASCII art banner using colorama for color formatting.
Prompts the user to enter a URL for subdomain enumeration.
Checks if the URL starts with http:// or https://, if not, prepends https://.
Uses requests.head to fetch HTTP headers from the site and prints them.
Splits the URL to get the original domain.
Reads the potential subdomains from a file.
Calls check_words to start the subdomain enumeration.
Handling Errors
The code handles various errors such as file not found, network issues, and keyboard interrupts, ensuring the tool exits gracefully in case of any issues.
Handling Interrupts
The tool gracefully handles CTRL+C (SIGINT) by catching the signal and exiting cleanly.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please fork this repository and submit a pull request for any improvements.

Author
Raulisr00t
