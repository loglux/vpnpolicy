# vpnpolicy
## VPN Policy Rule Routing for AsusWRT Merlin
##domains.txt contains a list of domains
```domain1.com
domain2.com
```
##static.csv contains a list of static routes (don't need to be changed by the script) in csv format:
Description,Source IP,Destination IP,Iface
```
ADomain,0.0.0.0,194.200.22.87/26,VPN
```
