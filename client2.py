from vpol import VPN_Rules

if __name__ == '__main__':
    local = "0.0.0.0" # your local subnet or network node
    client = 2 # 1,2,3,4 or 5
    conf_path = ""
    d_conf = conf_path + "domains.txt"
    s_conf = conf_path + "static.csv"
    rules = VPN_Rules(local)
    rules.domains(d_conf)
    rules.static(s_conf)
    rules.all_rules(client)
    rules.unset_nvram()
    rules.unset_nvram(client)
    rules.set_nvram()
    rules.unset_nvram()
    #rules.nvram_commit()
    #rules.client_restart(client)