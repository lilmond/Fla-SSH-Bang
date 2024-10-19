# Fla-SSH-Bang
Extremely super fast lightspeed SSH bruteforce tool written in Python.

![image](https://github.com/user-attachments/assets/a45ef85b-e9b7-4c2a-acf2-84d932df7186)

# Where to get proxies?
You can use my proxy list scraper here: https://github.com/lilmond/Proxal

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
Single host target
```
python flasshbang.py <target ip> -u root -P passlist_2023.txt -pp coolproxies.txt 
```

Multi-hosts
```
python flasshbang.py -M <host list file> -u root -P passlist_2023.txt -pp coolproxies.txt -o hacked_ssh.txt 
```
