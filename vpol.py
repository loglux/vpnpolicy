import pydig
import re
import csv
import os


class VPNRules:
    def __init__(self, local_ip):
        self.local_ip = local_ip
        self.pattern = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[" \
                       "0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
        self.static_lines = []
        self.vpn_list = []
        self.cidr_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)'

    def domains(self, d_conf):
        if self.local_ip == "0.0.0.0":
            self.local_ip = ""
        lines = filter(None, open(d_conf, "r").read().splitlines())
        for line in lines:
            all_subs = []
            if not line.startswith('#'):
                d = line.replace('@', '').strip()
                results = pydig.query(d, 'A')
                results = [item.replace('\r', '') for item in results]
                results = [x for x in results if re.match(self.pattern, x)]
                print(f"{d} IP: {str(results)}")
                if line.startswith('@'):
                    subnets = []
                    for ip in results:
                        net = os.popen(f"whois {ip} | grep 'route\|CIDR'").read()
                        result = re.findall(self.cidr_regex, net)
                        subnets.extend(result)
                    results = []
                    [results.append(n) for n in subnets if n not in results]
                    print(f"{d} Subnets: {results}")
                    for s in results:
                        subnet = f"<{d[:10]}>{self.local_ip}>{s}>VPN"
                        all_subs.append(subnet)
                else:
                    for r in results:
                        req = f"<{d[:10]}>{self.local_ip}>{r}>VPN"
                        self.vpn_list.append(req)
                self.vpn_list.extend(all_subs)

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
                        line = f'<{str(line[0]).strip()[:10]}>{str(line[1]).strip()}>{str(line[2]).strip()}' \
                               f'>{str(line[3]).strip().upper()}'
                        self.static_lines.append(line)
        except FileNotFoundError:
            pass

    def all_rules(self):
        if self.static_lines:
            self.vpn_list.extend(self.static_lines)
        self.vpn_list = ''.join(self.vpn_list)

    @staticmethod
    def unset_nvram(num=''):
        for n in ['', 1, 2, 3, 4, 5]:
            box = f"nvram_unset vpn_client{str(num)}_clientlist{str(n)}"
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
            vpn_list = f'nvram set vpn_client{str(seq)}_{str(x["list"])}="{str(x["content"])}"'
            print(vpn_list)
            os.system(vpn_list)

    @staticmethod
    def nvram_commit():
        # print("nvram commit")
        os.system("nvram commit")

    @staticmethod
    def client_restart(clnum=1):
        service_restart = "service restart_client" + str(clnum)
        # print(service_restart)
        os.system(service_restart)


if __name__ == '__main__':
    local = ""  # your local subnet or network node
    client = 2  # 1,2,3,4 or 5
    conf_path = ""
    d_conf = conf_path + "domains.txt"
    s_conf = conf_path + "static.csv"
    rules = VPNRules(local)
    rules.domains(d_conf)
    rules.static(s_conf)
    rules.all_rules()
    rules.unset_nvram()
    rules.unset_nvram(client)
    rules.set_nvram(client)
    rules.unset_nvram()
    # rules.nvram_commit()
    # rules.client_restart(client)
