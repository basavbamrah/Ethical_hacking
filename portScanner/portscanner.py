import socket
from IPy import IP


def scan(target):
    converted_ip=check_ip(target)
    print('\n' + '[- 0 Scanning Target]' +str(target))
    for port in range(20,30):                           # give range(start,stop)
        scan_port(converted_ip, port)


def check_ip(ip):
    try:
        IP(ip)
        return(ip)
    except ValueError:
        return socket.gethostbyname(ip)                                       # gets IP for given domain


def get_banner(sock):
    return sock.recv(1024)                                                    # receives information from port



def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(2.0)
        sock.connect((ipaddress, port))                                               # establish connection with port
        try:
            banner=get_banner(sock)
            print('[+] Open Port' + str(port) + ' : ' +str(banner.decode()))            # prints the services running in the open port (if any)
            
        except:
            print('[+] Open Port' +str(port))
    except:
        
        pass




if __name__ == '__main__':

    targets = input('[+] Enter Target/s to get Scan: (split multiple target with ,)')   # input ip or domain to scan separated with " , "
    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))
    else:
        scan(targets)


