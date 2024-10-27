# Fla-SSH-Bang
Lightspeed fast SSH bruteforce tool.

This tool is best combined with [Turbo](https://github.com/lilmond/Turbo)

Watch flasshbang2 at play here: [Hacking Thousands of SSH Servers Worldwide | Untargeted Reverse Brute-Force Attack](https://www.youtube.com/watch?v=ABVO17C8G64)

Discord: https://discord.com/invite/Bnf3e8pkyj

![image](https://github.com/user-attachments/assets/a62ef38e-06c8-4b41-8a0e-dcfd0739e2a5)

300 threads preview. Watch the demonstration on YT where I used 500 threads to see how fast it can actually go.

https://github.com/user-attachments/assets/e14f2745-7e81-4263-b7ee-30626cf1ef2e

# Where to get proxies?
You may use my proxy list scraper here (Proxal): https://github.com/lilmond/Proxal

# Installation
For Linux platforms. Execute the commands below. You may copy and paste and execute them all at once.
```
git clone https://github.com/lilmond/flasshbang
cd flasshbang
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Usage

## Examples
Single host target
```
python3 flasshbang.py <target ip> -u root -P samples/pass_list.txt -pp samples/good_proxies.txt 
```

Multi-hosts
```
python3 flasshbang.py -M <host list file> -u root -P samples/pass_list.txt -pp samples/good_proxies.txt -o hacked_ssh.txt 
```

# Help
```

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
                        Visit  https://github.com/lilmond for more free hacking tools! :3

usage: flasshbang.py [-h] [-p PORT] [-u USERNAME] -P PASSLIST -pp PROXY_LIST [-t THREADS] [-T THREADS_MULTI]
                     [-M HOST_LIST] [-o OUTPUT]
                     [hostname]

Fla-SSH-Bang! Inspired by vanhauser's hydra (also shoutout to him for creating that wonderful tool!). Super fast SSH
bruteforce tool powered by proxies that who knows where they came from. Written in Python! Number 1 language in the
world!

positional arguments:
  hostname              Target IP address.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Target port. Default is set to 22.
  -u USERNAME, --username USERNAME
                        SSH user to attack. The default is set to root.
  -P PASSLIST, --passlist PASSLIST
                        Your favorite password list from SecLists!
  -pp PROXY_LIST, --proxy-list PROXY_LIST
                        Not the size of your penis, but the longer your proxy list is, the better!
  -t THREADS, --threads THREADS
                        Threads, idk how to explain what threads are. But the default is set to 10! The more threads,
                        the faster!
  -T THREADS_MULTI, --threads-multi THREADS_MULTI
                        Threads for multi hosts. The default is 3
  -M HOST_LIST, --host-list HOST_LIST
                        File list of hosts to attack.
  -o OUTPUT, --output OUTPUT
                        Success logins output file.
```
