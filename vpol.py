import pydig
import re
import csv
import os

class VPN_Rules():
    def __init__(self, local_ip):
        self.local_ip=local_ip
        self.pattern = """^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"""
        self.static_lines = []
        self.vpn_list = []

    def domains(self, d_conf):
        lines = filter(None, open(d_conf, "r").read().splitlines())
        for d in lines:
            results = pydig.query(d, 'A')
            results = [item.replace('\r', '') for item in results]
            results = [x for x in results if re.match(self.pattern, x)]
            if self.local_ip == "0.0.0.0":
                self.local_ip = ""
            for r in results:
                req = '<' + d[:10] + '>' + self.local_ip + '>' + r + '>VPN'
                self.vpn_list.append(req)
        print(self.vpn_list)

    def static(self, s_conf):
        try:
            with open(s_conf, mode="r") as f:
                csv_lines = csv.reader(f)
                for line in csv_lines:
                    if len(line) == 4:
                        if line[1].strip() == "0.0.0.0":
                            line[1] = ""
                        if line[2].strip() == "0.0.0.0":
                            line[2] = ""
                        line = '<' + str(line[0]).strip()[:10] + '>' + str(line[1]).strip() + '>' + str(line[2]).strip() + '>' + str(line[3]).strip().upper()
                        self.static_lines.append(line)
            print(self.static_lines)
        except FileNotFoundError:
            pass

    def all_rules(self):
        if self.static_lines:
            self.vpn_list = self.vpn_list + self.static_lines
        self.vpn_list = ''.join(self.vpn_list)

    def unset_nvram(self, num=''):
        for n in ['', 1, 2, 3, 4, 5]:
            client = "vpn_client" + str(num)
            list = "_clientlist"
            set = "nvram unset "
            box = set + client + list + str(n)
            print(box)
            os.system(box)

    def set_nvram(self, seq=1):
        n = 255
        chunks = [self.vpn_list[i:i + n] for i in range(0, len(self.vpn_list), n)]
        all_lists = []
        try:
            all_lists = [{"list": "clientlist", "content": chunks[0]}]
            all_lists = all_lists + [{"list": "clientlist1", "content": chunks[1]}]
            all_lists = all_lists + [{"list": "clientlist2", "content": chunks[2]}]
            all_lists = all_lists + [{"list": "clientlist3", "content": chunks[3]}]
            all_lists = all_lists + [{"list": "clientlist4", "content": chunks[4]}]
            all_lists = all_lists + [{"list": "clientlist5", "content": chunks[5]}]
        except IndexError:
            pass
        for x in all_lists:
            vpn_list = "nvram set vpn_client" + str(seq) + "_" + str(x["list"]) + "=" + '"' + str(
                x["content"]) + '"'
            print(vpn_list)
            os.system(vpn_list)

    def nvram_commit(self):
        os.system("nvram commit")

    def client_restart(self, clnum=1):
        service_restart = "service restart_client" + str(clnum)
        print(service_restart)
        os.system(service_restart)

if __name__ == '__main__':
    local = "" # your local subnet or network node
    client = 2 # 1,2,3,4 or 5
    conf_path = ""
    d_conf = conf_path + "domains.txt"
    s_conf = conf_path + "static.csv"
    rules = VPN_Rules(local)
    rules.domains(d_conf)
    rules.static(s_conf)
    rules.all_rules()
    rules.unset_nvram()
    rules.unset_nvram(client)
    rules.set_nvram(client)
    rules.unset_nvram()
    #rules.nvram_commit()
    #rules.client_restart(client)
