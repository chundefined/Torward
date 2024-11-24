# tor_control.py

import os
import time
from stem import Signal
from stem.control import Controller
from constants import (TORRC_CONFIG, TORRC_PATH, RESOLV_CONF_ENTRY,
                       RESOLV_CONF_PATH, RESOLV_CONF_BACKUP_PATH, TOR_USER,
                       TOR_SERVICE_NAME, SYSCTL_CONF_PATH,
                       SYSCTL_CONF_BACKUP_PATH)
from network_config import disable_ipv6, enable_ipv6, setup_iptables, flush_iptables
from utils import get_tor_ip, get_public_ip

def backup_resolv_conf():
    if os.path.exists(RESOLV_CONF_PATH):
        os.system(f'cp {RESOLV_CONF_PATH} {RESOLV_CONF_BACKUP_PATH}')
        print("Backup of resolv.conf created.")
    else:
        print("No resolv.conf found to backup.")


def restore_resolv_conf():
    if os.path.exists(RESOLV_CONF_BACKUP_PATH):
        os.system(f'mv {RESOLV_CONF_BACKUP_PATH} {RESOLV_CONF_PATH}')

def configure_torrc():
    with open(TORRC_PATH, 'w') as torrc_file:
        torrc_file.write(TORRC_CONFIG)
    print("Torrc file configured.")
    os.system(f'chown {TOR_USER}:{TOR_USER} {TORRC_PATH}')
    os.system(f'chmod 600 {TORRC_PATH}')

def configure_resolv_conf():
    backup_resolv_conf()
    if RESOLV_CONF_ENTRY not in open(RESOLV_CONF_PATH).read():
        with open(RESOLV_CONF_PATH, 'w') as resolv_file:
            resolv_file.write(RESOLV_CONF_ENTRY)
        print("resolv.conf file configured.")

def start_tor_service():
    print("Configuring TOR service to use custom configuration...")
    # Stop any running TOR services
    os.system(f'systemctl stop {TOR_SERVICE_NAME}')
    os.system('systemctl stop tor@default.service')
    os.system('systemctl disable tor@default.service')
    # Create override directory if it doesn't exist
    os.system('mkdir -p /etc/systemd/system/tor.service.d/')
    with open('/etc/systemd/system/tor.service.d/override.conf', 'w') as f:
        f.write(f'''
            [Service]
            ExecStart=
            ExecStart=/usr/bin/tor -f {TORRC_PATH}
            ''')
    os.system('systemctl daemon-reload')
    print("Starting TOR service with custom configuration...")
    os.system(f'systemctl start {TOR_SERVICE_NAME}')
    time.sleep(5)
    # Check if TOR service started 
    status = os.system(f'systemctl is-active --quiet {TOR_SERVICE_NAME}')
    if status != 0:
        print("Failed to start TOR service. Please check the TOR logs for details.")
        exit(1)

def stop_tor_service():
    print("Stopping TOR service...")
    os.system(f'systemctl stop {TOR_SERVICE_NAME}')
    os.system('systemctl stop tor@default.service')
    # Kill any remaining TOR processes
    os.system('pkill -f tor')
    # Remove the override configuration
    os.system('rm -f /etc/systemd/system/tor.service.d/override.conf')
    os.system('systemctl daemon-reload')

def request_new_tor_circuit():
    print("Requesting new TOR circuit...")
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(cookie_path='/run/tor/control.authcookie')
            controller.signal(Signal.NEWNYM)
        time.sleep(5)
        print("New TOR circuit established.")
        current_ip = get_tor_ip()
        print(f"New TOR IP: {current_ip}")
    except Exception as e:
        print(f"Error requesting new TOR circuit: {e}")

def start_torward():
    print("Starting Torward...")
    disable_ipv6()
    configure_torrc()
    configure_resolv_conf()
    start_tor_service()
    time.sleep(10)
    setup_iptables()
    #current_ip = get_tor_ip()
    #print(f"Current TOR IP: {current_ip}")

def stop_torward():
    print("Stopping Torward...")
    flush_iptables()
    restore_resolv_conf()
    enable_ipv6()
    stop_tor_service()
    print("Restarting NetworkManager...")
    os.system('systemctl restart NetworkManager')
    time.sleep(8) 
    current_ip = get_public_ip()
    print(f"Current IP: {current_ip}")
