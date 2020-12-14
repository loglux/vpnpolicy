"""
https://www.snbforums.com/threads/low-nvram-despite-factory-defaulting-etc.38573/#post-318633
vpn_client_clientlist
This is a temporary variable that gets filled 
whenever you change settings through the webui. 
The web server then copies it to the appropriate instance (client1, client2, etc...).

Rules:
https://github.com/RMerl/asuswrt-merlin.ng/wiki/Policy-based-routing
https://x3mtek.com/policy-rule-routing-on-asuswrt-merlin-firmware/
"""

import pydig
import csv
import os

local_ip="192.168.10.0/24"

lines = filter(None, open("./domains.txt", "r").read().splitlines())
vpn_list = []
for d in lines:
    results = pydig.query(d, 'A')
    for r in results:
        req = '<' + d + '>' + local_ip + '>' + r + '>VPN'
        vpn_list.append(req)
vpn_list = ''.join(vpn_list)

try:
    static_lines = []
    with open("static.csv", mode="r") as f:
        csv_lines = csv.reader(f)
        for line in csv_lines:
            if len(line) == 4:
                line = '<' + str(line[0]).strip() + '>' + str(line[1]).strip() + '>' + str(line[2]).strip() + '>' + str(line[3]).strip().upper()
                static_lines.append(line)
    static_lines = ''.join(static_lines)
except FileNotFoundError:
    pass

if static_lines:
    vpn_list = vpn_list + static_lines
vpn_list = "nvram set vpn_client1_clientlist=" + '"' + vpn_list + '"'

print(vpn_list)

#for n in range(6):
#    vpn_client = "nvram get vpn_client1_clientlist" + str(n)
#    print(n)
#    os.system(vpn_client)
 

os.system("nvram unset vpn_client_clientlist")
os.system("nvram unset vpn_client_clientlist1")
os.system("nvram unset vpn_client_clientlist2")
os.system("nvram unset vpn_client_clientlist3")
os.system("nvram unset vpn_client_clientlist4")
os.system("nvram unset vpn_client_clientlist5")

os.system("nvram unset vpn_client1_clientlist")
os.system("nvram unset vpn_client1_clientlist1")
os.system("nvram unset vpn_client1_clientlist2")
os.system("nvram unset vpn_client1_clientlist3")
os.system("nvram unset vpn_client1_clientlist4")
os.system("nvram unset vpn_client1_clientlist5")

#################

#os.system("nvram unset vpn_client2_clientlist")
#os.system("nvram unset vpn_client2_clientlist1")
#os.system("nvram unset vpn_client2_clientlist2")
#os.system("nvram unset vpn_client2_clientlist3")
#os.system("nvram unset vpn_client2_clientlist4")
#os.system("nvram unset vpn_client2_clientlist5")


#os.system("nvram unset vpn_client3_clientlist")
#os.system("nvram unset vpn_client3_clientlist1")
#os.system("nvram unset vpn_client3_clientlist2")
#os.system("nvram unset vpn_client3_clientlist3")
#os.system("nvram unset vpn_client3_clientlist4")
#os.system("nvram unset vpn_client31_clientlist5")

#os.system("nvram unset vpn_client4_clientlist")
#os.system("nvram unset vpn_client4_clientlist1")
#os.system("nvram unset vpn_client4_clientlist2")
#os.system("nvram unset vpn_client4_clientlist3")
#os.system("nvram unset vpn_client4_clientlist4")
#os.system("nvram unset vpn_client4_clientlist5")

#os.system("nvram unset vpn_client5_clientlist")
#os.system("nvram unset vpn_client5_clientlist1")
#os.system("nvram unset vpn_client5_clientlist2")
#os.system("nvram unset vpn_client5_clientlist3")
#os.system("nvram unset vpn_client5_clientlist4")
#os.system("nvram unset vpn_client5_clientlist5")

########################

os.system(vpn_list)
#os.system("nvram commit")
#os.system("service restart_vpnclient1")



