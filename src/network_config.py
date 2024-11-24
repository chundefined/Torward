# network_config.py

import os
import subprocess
from constants import TOR_USER, SYSCTL_CONF_PATH, SYSCTL_CONF_BACKUP_PATH

def disable_ipv6():
    print("Disabling IPv6 to prevent leaks...")
    if not os.path.exists(SYSCTL_CONF_BACKUP_PATH):
        os.system(f'cp {SYSCTL_CONF_PATH} {SYSCTL_CONF_BACKUP_PATH}')
    with open(SYSCTL_CONF_PATH, 'a') as sysctl_file:
        sysctl_file.write('\nnet.ipv6.conf.all.disable_ipv6 = 1')
        sysctl_file.write('\nnet.ipv6.conf.default.disable_ipv6 = 1')
    os.system('sysctl -p')
    print("IPv6 disabled.")

def enable_ipv6():
    print("Reactivating IPv6...")
    if os.path.exists(SYSCTL_CONF_BACKUP_PATH):
        os.system(f'mv {SYSCTL_CONF_BACKUP_PATH} {SYSCTL_CONF_PATH}')
        os.system('sysctl -p')
    print("IPv6 reactivated.")

def setup_iptables():
    print("Setting up iptables rules...")
    tor_uid = subprocess.getoutput(f'id -u {TOR_USER}')
    os.system(f"""
        # Flush existing rules
        iptables -F
        iptables -t nat -F

        # Set default policies
        iptables -P INPUT ACCEPT
        iptables -P FORWARD DROP
        iptables -P OUTPUT DROP

        # Allow loopback traffic
        iptables -A OUTPUT -o lo -j ACCEPT

        # Allow already established connections
        iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

        # Allow TOR user output
        iptables -A OUTPUT -m owner --uid-owner {tor_uid} -j ACCEPT

        # Exclude local networks from TOR
        iptables -A OUTPUT -d 127.0.0.0/8 -j ACCEPT
        iptables -A OUTPUT -d 192.168.0.0/16 -j ACCEPT
        iptables -A OUTPUT -d 10.0.0.0/8 -j ACCEPT
        iptables -A OUTPUT -d 172.16.0.0/12 -j ACCEPT

        # Redirect DNS requests to TOR
        iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
        iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

        # Redirect TCP traffic to TOR
        iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040

        # Allow traffic to TOR ports
        iptables -A OUTPUT -p tcp -m tcp --dport 9001 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 9030 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 9040 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 9050 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 9051 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 443 -j ACCEPT
        iptables -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT

        # Log and drop all other outgoing traffic
        iptables -A OUTPUT -j LOG --log-prefix "Dropped by Torward: "
        iptables -A OUTPUT -j DROP

        # IPv6 rules
        ip6tables -P OUTPUT DROP
        ip6tables -P INPUT DROP
        ip6tables -P FORWARD DROP
        ip6tables -F
    """)
    print("iptables rules configured.")

def flush_iptables():
    print("Cleaning up iptables rules...")
    os.system('iptables -F')
    os.system('iptables -t nat -F')
    os.system('iptables -t mangle -F')
    os.system('iptables -X')
    os.system('iptables -P INPUT ACCEPT')
    os.system('iptables -P OUTPUT ACCEPT')
    os.system('iptables -P FORWARD ACCEPT')
    os.system('ip6tables -F')
    os.system('ip6tables -X')
    os.system('ip6tables -P INPUT ACCEPT')
    os.system('ip6tables -P OUTPUT ACCEPT')
    os.system('ip6tables -P FORWARD ACCEPT')
    print("iptables rules cleaned.")
