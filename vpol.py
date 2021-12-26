import pydig
import re
import csv
import os


class VPNRules:
    def __init__(self, local_ip="", name_length=20, client=1):
        self.local_ip = local_ip
        self.ip_regex = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[" \
                        "0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
        self.cidr_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)'
        self.vpn_list = []
        self.client = client
        self.format_rule = "<{}>{}>{}>{}>{}"
        self.interface = "OVPN{}".format(str(self.client))
        self.name_length = name_length
        self.rule_list = "/jffs/openvpn/vpndirector_rulelist"
        #self.rule_list = "vpndirector_rulelist"
        # print(self.intereface)

    def domains(self, d_conf):
        if self.local_ip == "0.0.0.0":
            self.local_ip = ""
        lines = filter(None, open(d_conf, "r").read().splitlines())
        for line in lines:
            if not line.startswith('#'):
                d = line.replace('@', '').strip()
                results = pydig.query(d, 'A')
                results = [item.replace('\r', '') for item in results]
                results = [x for x in results if re.match(self.ip_regex, x)]
                print(f"{d} IP: {str(results)}")
                if line.startswith('@'):
                    subnets = []
                    for ip in results:
                        net = os.popen(f"whois {ip} | grep 'route\|CIDR'").read()
                        result = re.findall(self.cidr_regex, net)
                        subnets.extend(result)
                    unique_subnets = []
                    [unique_subnets.append(n) for n in subnets if n not in unique_subnets]
                    print(f"{d} Subnets: {unique_subnets}")
                    for s in unique_subnets:
                        subnet = self.format_rule.format(1, d[:self.name_length], self.local_ip, s, self.interface)
                        self.vpn_list.append(subnet)
                else:
                    for r in results:
                        ip_address = self.format_rule.format(1, d[:self.name_length], self.local_ip, r, self.interface)
                        self.vpn_list.append(ip_address)

    def static(self, s_conf):
        try:
            with open(s_conf, mode="r") as f:
                csv_lines = csv.reader(f)
                for line in csv_lines:
                    if len(line) == 4:
                        enable = 1
                        name = 0
                        lan = 1
                        wan = 2
                        interface = 3
                    elif len(line) == 5:
                        if line[0] == 0 or 1:
                            enable = line[0]
                        else:
                            enable = 1
                        name = 1
                        lan = 2
                        wan = 3
                        interface = 4
                    if line[lan].strip() == "0.0.0.0":
                        line[lan] = ""
                    if line[wan].strip() == "0.0.0.0":
                        line[wan] = ""
                    line = self.format_rule.format(enable,
                        str(line[name]).strip()[:self.name_length],
                                                   str(line[lan]).strip(),
                                                   str(line[wan]).strip(),
                                                   str(line[interface]).strip().upper() + str(self.client))
                    self.vpn_list.append(line)
        except FileNotFoundError:
            pass

    def all_rules(self, d_conf="domains.txt", s_conf="static.csv"):
        self.domains(d_conf)
        self.static(s_conf)
        self.vpn_list = ''.join(self.vpn_list)

    # Not sure is it needed at all
    def save_rules(self):
        with open('vpndirector_rulelist.txt', 'w') as f:
            f.writelines(self.vpn_list)

    def create_rules(self):
        try:
            with open(self.rule_list, mode="r+") as f:
                rules = f.read()
                # print(rules)
                int_pattern = "<[1,0]>[a-zA-Z.0-9-]*>({})?>({})?>OVPN{}"\
                    .format(self.cidr_regex, self.cidr_regex, self.client)
                # print(int_pattern)
                updated_rules = re.sub(int_pattern, '', rules)
                # print(updated_rules)
                self.vpn_list = self.vpn_list + updated_rules
                # print(self.vpn_list)
        except FileNotFoundError:
            print("Creating a new vpndirector_" + "rulelist file...")
            pass
        with open(self.rule_list, mode="w") as f:
            f.write(self.vpn_list)

    def clear_all(self):
        try:
            with open(self.rule_list, mode="r+") as f:
                f.truncate(0)
        except FileNotFoundError:
            pass

    def client_restart(self):
        service_restart = "service restart_vpnclient" + str(self.client)
        print(service_restart)
        os.system(service_restart)

if __name__ == '__main__':
    client = 2  # a client's number (from 1 to 5)
    # your local subnet or network node, you can leave it black for entire LAN
    # local = ""
    # name_length = 20
    # local= "" and name_lenght=20 by default
    # you can rewrite name_length, and local
    # rules = VPNRules(local, name_length, client)
    rules = VPNRules(client=client)
    conf_path = ""
    d_conf = conf_path + "domains.txt"
    s_conf = conf_path + "static.csv"
    rules.all_rules(d_conf, s_conf)
    # conf_path, d_conf and s_cpnf are not compulsory,
    # especially, if you put these files into the same directory
    # domains.txt and static.cvs are used by default,
    # so you can use this method without arguments:
    # rules.all_rules()
    rules.create_rules()
    rules.client_restart()


