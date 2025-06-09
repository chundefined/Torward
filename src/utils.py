# utils.py

import os
import sys
import re
import requests
import subprocess


def check_root():
    if os.geteuid() != 0:
        print("Please run as root using 'sudo'.")
        sys.exit(1)


def sigint_handler(signum, frame):
    print("\nInterrupted by user. Exiting...")
    sys.exit(0)


def get_tor_ip():
    try:
        # Use curl with icanhazip.com through the TOR proxy
        result = subprocess.run(
            ["curl", "-L", "--socks5", "127.0.0.1:9040",
             "https://icanhazip.com"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            ip = result.stdout.strip()
            if ip:
                return ip

        # Fallback in case the above fails
        result = subprocess.run(
            ["curl", "-L", "https://icanhazip.com"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            ip = result.stdout.strip()
            if ip:
                return ip

        return "Unable to determine Tor IP"
    except Exception as e:
        return f"Error determining Tor IP: {e}"


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text",
                                timeout=10)
        if response.status_code == 200:
            ip = response.text.strip()
            if re.match(r'^[\d\.]+$', ip):
                return ip
        return "Unable to determine public IP."
    except Exception as e:
        return f"Error fetching public IP: {e}"


def print_usage():
    print("Usage: sudo python3 torward.py [option]")
    print("Options:")
    print("  -s, --start    Start routing all traffic through TOR")
    print("  -r, --switch   Switch TOR identity (request new circuit)")
    print("  -x, --stop     Stop routing traffic through TOR")
    print("  -c, --status   Show current TOR status")
    print("  -h, --help     Print this help message")
    sys.exit(0)
