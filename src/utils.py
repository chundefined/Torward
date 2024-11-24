# utils.py

import os
import sys
import signal
import subprocess
import requests
from stem.control import Controller

def check_root():
    if os.geteuid() != 0:
        print("Please run as root using 'sudo'.")
        sys.exit(1)

def sigint_handler(signum, frame):
    print("\nInterrupted by user. Exiting...")
    sys.exit(0)

def get_tor_ip():
    try:
        proxies = {
            'http': 'socks5h://127.0.0.1:9040',
            'https': 'socks5h://127.0.0.1:9040',
        }
        response = requests.get("http://check.torproject.org/", proxies=proxies, timeout=10)
        if response.status_code == 200:
            if "Your IP address appears to be" in response.text:
                ip_start = response.text.find("Your IP address appears to be") + 31
                ip_end = response.text.find(".", ip_start) + 1
                return response.text[ip_start:ip_end].strip()
        return "Unable to determine Tor IP."
    except Exception as e:
        return f"Error: {e}"

def get_public_ip():
    try:
        ip = subprocess.getoutput('curl -s https://ipinfo.io/ip')
        return ip if ip else "Unknown"
    except Exception:
        return "Unknown"

def print_usage():
    print("""
        Torward usage:

        -s, --start       Start torward
        -r, --switch      Request new TOR exit node
        -x, --stop        Stop torward
        -h, --help        Show help
    """)
    sys.exit(0)
