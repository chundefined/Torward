[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)

[![License](https://img.shields.io/badge/License-MIT-lightgrey)](https://github.com/Sh4rk0-666/BaphoDashBoard/blob/master/LICENSE)
[![Twitter](https://img.shields.io/badge/Twitter-%40Chungo__0-%231da1f2)](https://twitter.com/Chungo_0/)
[![Patreon](https://img.shields.io/badge/chundefined-Patreon-critical)](https://www.patreon.com/chundefined)


# Torward

Torward is an improved version based on the torghost-gn and darktor scripts, designed to enhance anonymity on the Internet. The tool prevents data leaks and forces all traffic from our computer to be routed exclusively through the Tor network, providing a high level of privacy in our connections.


## Installation

```bash
   git clone https://github.com/chundefined/Torward.git
```

```bash
   cd Torward
```

```bash
   chmod +x install.sh
```

```bash
   ./install.sh
```

## Security Enhancements

This version includes several key security improvements to protect your identity and ensure better network configuration:

1. **IPv6 Leak Prevention**  
   IPv6 is now disabled to prevent any potential IP leaks. All traffic is forced through the Tor network by modifying system IPv6 settings in `network_config.py`.

2. **Enhanced iptables Rules**  
   Strict iptables rules are implemented to ensure only Tor traffic is allowed. Non-Tor traffic is blocked, DNS queries are routed through Tor, and only essential connections to Tor ports are permitted. Additionally, IPv6 traffic is blocked to prevent leaks.

3. **Tor Configuration Adjustments**  
   The `darktorrc` file has been updated to enforce that all traffic, including DNS queries, is routed through Tor, improving anonymity.


## TODO

- Get the IP from the last Tor exit node: Currently, the script does not display the IP of the last Tor exit node in the console. This can be achieved by using Tor's API to get the public IP of the exit node.
- Better error handling: Ensure that the tool properly handles errors, such as Tor disconnection or network issues.
