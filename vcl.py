import pydig
import re
import csv
import os

local_ip="0.0.0.0"
pattern = """^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"""

lines = filter(None, open("domains.txt", "r").read().splitlines())
vpn_list = []
for d in lines:
    results = pydig.query(d, 'A')
#    results = [item.replace('\r', '') for item in results]
    results = [x for x in results if re.match(pattern, x)]
    #print(results)
    for r in results:
        req = '<' + d[:10] + '>' + local_ip + '>' + r + '>VPN'
        vpn_list.append(req)

try:
    static_lines = []
    with open("static.csv", mode="r") as f:
        csv_lines = csv.reader(f)
        for line in csv_lines:
            if len(line) == 4:
                line = '<' + str(line[0]).strip()[:10] + '>' + str(line[1]).strip() + '>' + str(line[2]).strip() + '>' + str(line[3]).strip().upper()
                static_lines.append(line)
except FileNotFoundError:
    pass

if static_lines:
    vpn_list = vpn_list + static_lines
#print(vpn_list)
vpn_list = ''.join(vpn_list)
vpn_list = "nvram set vpn_client1_clientlist=" + '"' + vpn_list + '"'
#print(vpn_list)

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
#os.system("nvram unset vpn_client3_clientlist5")

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
#os.system("service restart_vpnclient2")