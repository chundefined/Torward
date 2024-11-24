# constants.py

VERSION = "2.0"

TORRC_CONFIG = """
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 9040
DNSPort 5353
ControlPort 9051
CookieAuthentication 1
CookieAuthFileGroupReadable 1
RunAsDaemon 1
Log notice file /var/log/tor/notices.log
"""

RESOLV_CONF_ENTRY = 'nameserver 127.0.0.1'

TORRC_PATH = '/etc/tor/torwardrc'
RESOLV_CONF_PATH = '/etc/resolv.conf'
RESOLV_CONF_BACKUP_PATH = '/etc/resolv.conf.bak'

TOR_USER = 'debian-tor'
TOR_SERVICE_NAME = 'tor'

SYSCTL_CONF_PATH = '/etc/sysctl.conf'
SYSCTL_CONF_BACKUP_PATH = '/etc/sysctl.conf.bak'
