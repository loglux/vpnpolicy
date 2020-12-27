from vpol import VPNRules

if __name__ == '__main__':
    local = "0.0.0.0" # your local subnet or network node
    client = 2 # 1,2,3,4 or 5
    conf_path = ""
    d_conf = conf_path + "domains.txt"
    s_conf = conf_path + "static.csv"
    rules = VPNRules(local)
    rules.all_rules(d_conf, s_conf)
    rules.unset_nvram()
    rules.unset_nvram(client)
    rules.set_nvram(client)
    rules.unset_nvram()
    # rules.nvram_commit()
    # rules.client_restart(client)