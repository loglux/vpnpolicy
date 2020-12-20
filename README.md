# vpnpolicy (VPN Policy Rule Routing for AsusWRT Merlin)

## What that script does?
This script creates VPN Policy rules for OpenVPN client in AsusWRT Merlin Firmware. It helps to obtain IP addresses that belong to the domains and save it in the router’s configuration. It also takes a new list of IP addresses, so you can use this script regularly, to keep the list of IPs fresh.

VPN client uses that rules to redirect traffic for your device or network based on the destination IP addresses. Instead of pushing all traffic through the VPN, you can redirect it to VPN only if you need to get access to particular network resources. That gives your incredible flexibility using  VPN.

It takes domain names from file domains.txt and obtains IP addresses.
File domains.txt contains a list of domains
```
domain1.com
domain2.com
```
Also, it’s possible to use static IP records.
File static.csv contains a list of static routes (that don’t need to be changed by the script) in CSV format:
Description,Source IP,Destination IP,Iface
```
ADomain,0.0.0.0,194.200.22.87/26,VPN
```
## Where you can find domains?
Some resources like online cinema theatres have not just more than 1 IP address but also more than one domain.
Turn on ‘Web History’ option at the router’s page ‘Adaptive QoS – Web History’. Here you can see domains are used by your computer or media player.

## Reqiurements

1. You need to install Entwire on your router


2. You need to install bnd-tools or bnd-dig on your router
```
opkg install bind-tools
```

3. You need to install Python
```
opkg install python3
```

4 You need to install python3-pip
```
opkg install python3-pip
```

5 You need to install pydig module
```
pip install pydig
```

## How to use the script
local - IP address or set of addresses (192.168.0.10, 192.168.0.0/24 or just 0.0.0.0 fur your entire local network.

client – a number of a VPN Client you’re using. You have five clients, so chose the relevant number.

You can comment on rules.nvram_commit() if you don’t want to save your rules in the router’s memory and comment rules.client_restart(client) to prevent VPN client from restarting.

Execute the script 
```
python vpol.py
```
