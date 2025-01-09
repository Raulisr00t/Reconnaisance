import os
import sys
import subprocess
import requests
import socket
import colorama
from bs4 import BeautifulSoup
import re

def usage():
    print(colorama.Fore.RED + "[!] Usage: python3 PassiveSubRecon.py <domain>" + colorama.Style.RESET_ALL)
    sys.exit(1)

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

def install(package):
    if check_internet_connection():
        print(f"[i] Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"[!] Failed to install {package}: {e}")
            sys.exit(1)
    else:
        print(colorama.Fore.RED+"[-] Check Your Internet Connection Please [-]"+colorama.Style.RESET_ALL)
        sys.exit(1)

try:
    import bs4
    import re
    import colorama

except ImportError as e:
    print(f"[i] Missing library detected: {e.name}")
    install(e.name)

def scrap(domain):
    try:
        # Base URL for crt.sh
        base_url = "https://crt.sh"
        url = base_url + f"/?q={domain}"

        # Make the HTTP request
        print(f"[i] Fetching data from {url}")
        response = requests.get(url, timeout=25)
        response.raise_for_status()

        # Extract subdomains using regex
        print(colorama.Fore.LIGHTGREEN_EX + "[i] Extracting subdomains..." + colorama.Style.RESET_ALL)
        subdomains = set()
        regex = re.compile(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+' + re.escape(domain) + r'\b')
        matches = regex.findall(response.text)
        for match in matches:
            subdomains.add(match)

        # Output results
        if subdomains:
            print("[+] Found the following subdomains:")
            for subdomain in sorted(subdomains):
                print(colorama.Fore.CYAN + subdomain + colorama.Style.RESET_ALL)

        else:
            print(colorama.Fore.RED + "[-] No subdomains found." + colorama.Style.RESET_ALL)
    
    except Exception as e:
        print(colorama.Fore.RED + str(e) + colorama.Style.RESET_ALL)

def main():
    if len(sys.argv) < 2:
        usage()

    else:
        domain = sys.argv[1]
        scrap(domain)

if __name__ == "__main__":
    main()
