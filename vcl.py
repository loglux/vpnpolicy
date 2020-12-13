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

static_lines = []
with open("static.csv", mode="r") as f:
    csv_lines = csv.reader(f)
    for line in csv_lines:
        if len(line) == 4:
            line = '<' + str(line[0]).strip() + '>' + str(line[1]).strip() + '>' + str(line[2]).strip() + '>' + str(line[3]).strip().upper()
            static_lines.append(line)
static_lines = ''.join(static_lines)

vpn_list = vpn_list + static_lines

vpn_list = "nvram set vpn_client2_clientlist=" + '"' + vpn_list + '"'

print(vpn_list)

os.system("nvram unset vpn_client2_clientlist")
os.system("nvram unset vpn_client_clientlist")
os.system("nvram unset vpn_client_clientlist2")
os.system(vpn_list)
#os.system("nvram commit")
#os.system("service restart_vpnclient2")



