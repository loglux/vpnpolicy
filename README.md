# vpnpolicy (VPN Policy Rule Routing for AsusWRT Merlin)

## What does that script do?
This script creates VPN Policy rules for OpenVPN client in AsusWRT Merlin Firmware. It helps to obtain IP addresses that belong to the domains and save it in the router’s configuration. It also takes a new list of IP addresses, so you can use this script regularly, to keep the list of IPs fresh.

VPN client uses rules to redirect traffic for your device or network based on the destination IP addresses. Instead of pushing all traffic through the VPN, you can redirect it to VPN only if you need to get access to particular network resources. That gives your incredible flexibility using  VPN.

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

3. You need to install whois utility on your router
```
opkg install whois
```

4. You need to install Python
```
opkg install python3
```

5 You need to install python3-pip
```
opkg install python3-pip
```

6 You need to install pydig module
```
pip install pydig
```

## How to use the script

### Set variables
The main library is stored in file 'vpol.py'

You can create a separate file for each client ('client1.py', 'client2.py' etc) if you have more than 1 client set up.

'local' - IP address or set of addresses (192.168.0.10, 192.168.0.0/24 or just 0.0.0.0 for your entire local network.

'client' – a number of a VPN Client you’re using. You have five clients, so put the relevant number.

You can also put unique file names and path. 
    
    conf_path = ""
    
    d_conf = conf_path + "domains.txt"
    
    s_conf = conf_path + "static.csv"

You can comment out a domain using '#' symbol if you want to exclide them from the process.

Use '@' symbol at the begining if you want to grab subnets (xxx.xxx.xxx.xxx/xx) for the chosen domain. 

You can comment out 'rules.nvram_commit()' if you don’t want to save your rules in the router’s memory 

and comment out in 'rules.client_restart(client)' to prevent VPN client from restarting.

### Start

You can download the script in any way you think is convenient. The best one is using 'git clone' for this purpose.
```
opkg install git
```
And then download the script:
```
git clone https://github.com/loglux/vpnpolicy.git
```

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
NVRAM has 6 variables per client for storing VPN rules list. It was noticed that each variable could store up to 1024 symbols. However, the firmware split the list in chunks by 255 symbols. 255 * 6 = 1530. It very dubious that 100 rules can be stored in 1530 symbols. Approximately 100 rules can be a summary of the rules of all 5 clients. 
f course, it's done by FW designers to save space for NVRAM. For compatibility purpose, here 255 symbols limit has been left, which can be changed in set_nvram() function, adjusting 'n =' variable. Theoretically, it's possible to split a list of rules by 1024 symbols (1024 * 6 = 6144) but be aware of NVRAM capacity. 

In case if the list exceeds 1530 limit, it will be cut off at this point. 

The 'Description' field is limited to ten symbols, to save more space for rules. 
The script automatically cuts off all symbols that exceed this ten symbols limit.

## Useful references:
https://github.com/RMerl/asuswrt-merlin.ng/wiki/Policy-based-routing

https://github.com/RMerl/asuswrt-merlin.ng/wiki/User-scripts
