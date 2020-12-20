# vpnpolicy (VPN Policy Rule Routing for AsusWRT Merlin)

## What does that script do?
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
## Where can you find domains?
Some resources like online cinema theatres have not just more than 1 IP address but also more than one domain.
Turn on ‘Web History’ option at the router’s page ‘Adaptive QoS – Web History’. Here you can see domains are used by your computer or media player.

## Reqiurements

1. You need to install Entware on your router


2. You need to install bind-tools or bind-dig on your router
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

### Set variables
local - IP address or set of addresses (192.168.0.10, 192.168.0.0/24 or just 0.0.0.0 for your entire local network.

client – a number of a VPN Client you’re using. You have five clients, so chose the relevant number.

You can also put an unique file names and path. 
    
    conf_path = ""
    
    d_conf = conf_path + "domains.txt"
    
    s_conf = conf_path + "static.csv"
    

You can comment out rules.nvram_commit() if you don’t want to save your rules in the router’s memory 

and comment out in rules.client_restart(client) to prevent VPN client from restarting.

### Start
The main library is stored in file vpol.py

You can create a separate file for each client (client1.py, client2.py etc) if you have more than 1 client set up.

Execute the script 
```
python client1.py
```

### If you want to start it every time along with VPN client start/restart
Put a reference to the script into '/jffs/scripts/openvpn-event'. 
In that case you must comment out rules.client_restart(client) to avoid a loop.
```
#rules.client_restart(client)
```
Inside of the openvpn-event put a command to start the script:
```
#!/bin/sh
python /path_to_your_script/client1.py
```
And don't forget to make the openvpn-event executable
```
chmod a+rx /jffs/scripts/openvpn-event
```

## Known limitations
It's possible to save up 20 rules in one nvram variable.
This scrpts saves rules into first variable vpn_client_clientlist of possible six.
It's planned in future to split rules by sets of 20 and save them into 6 nvram variables to get full capacity.
Currently only up to 20 rules per client are possible.

The 'Description' field is limited to ten symbols, to save more space for rules. 
The script automatically cuts off all symbols that exceed this ten symbols limit.

## Useful references:
https://github.com/RMerl/asuswrt-merlin.ng/wiki/Policy-based-routing

https://github.com/RMerl/asuswrt-merlin.ng/wiki/User-scripts
