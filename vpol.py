import pydig
import re
import csv
import os

class VPN_Rules():
    def __init__(self, local_ip="0.0.0.0"):
        self.local_ip=local_ip
        self.pattern = """^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"""
        self.static_lines = []
        self.vpn_list = []
        #print("Hi")

    def domains(self):
        #print(self.local_ip)
        lines = filter(None, open("domains.txt", "r").read().splitlines())
        #vpn_list = []
        for d in lines:
            results = pydig.query(d, 'A')
            results = [item.replace('\r', '') for item in results]
            results = [x for x in results if re.match(self.pattern, x)]
            #print(results)
            for r in results:
                req = '<' + d[:10] + '>' + self.local_ip + '>' + r + '>VPN'
                self.vpn_list.append(req)
        print(self.vpn_list)

    def static(self):
        try:
    #        static_lines = []
            with open("static.csv", mode="r") as f:
                csv_lines = csv.reader(f)
                for line in csv_lines:
                    if len(line) == 4:
                        line = '<' + str(line[0]).strip()[:10] + '>' + str(line[1]).strip() + '>' + str(line[2]).strip() + '>' + str(line[3]).strip().upper()
                        self.static_lines.append(line)
            #return self.static_lines
            print(self.static_lines)
        except FileNotFoundError:
            pass

    def all_rules(self, seq=1):
        if self.static_lines:
            self.vpn_list = self.vpn_list + self.static_lines
        #print(self.vpn_list)
        self.vpn_list = ''.join(self.vpn_list)
        self.vpn_list = "nvram set vpn_client" + str(seq) + "_clientlist=" + '"' + self.vpn_list + '"'
        #print(vpn_list)

    def unset_nvram(self, num=''):
        for n in ['', 1, 2, 3, 4, 5]:
            client = "vpn_client" + str(num)
            list = "_clientlist"
            set = "nvram unset "
            box = set + client + list + str(n)
            print(box)
            #os.system(box)

    def set_nvram(self):
        print(self.vpn_list)
        #os.system(self.vpn_list)

if __name__ == '__main__':
    local = "192.168.10.0/24"
    rules = VPN_Rules()
    rules.domains()
    rules.static()
    rules.all_rules(2)
    rules.unset_nvram()
    rules.unset_nvram(2)
    rules.set_nvram()



"""
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
"""