import socket
import sys
import threading

ports = range(0,65536)
open_ports = []

def check_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

ip = input('Please enter an IP for scanning: ').strip()

try:
    ip = socket.gethostbyname(ip)
except socket.gaierror:
    print('Domain resolution failed. Please try again with a valid IP address or domain.')
    sys.exit()

if not check_ip(ip):
    print('Not a valid IP address. Please try again.')
    sys.exit()

try:
    def connect_port(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print('Port is open:', port)
            open_ports.append(port)
        sock.close()

    all_threads = []
    for port in ports:
        response = threading.Thread(target=connect_port,args=(ip,port))
        response.start()
        all_threads.append(response)

    for response in all_threads:
        response.join()

    if open_ports:
        print('Open ports are:')
        print(sorted(open_ports))

    else:
        print('No open ports found.')
        sys.exit()

except KeyboardInterrupt:
    print('Connection refused..')
    exit(0)
