from vpol import VPNRules

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
