from vpol import VPNRules

if __name__ == '__main__':
    d = VPNRules("")
    d_conf =  "domains.txt"
    d.domains(d_conf)
    print("Tip: You can check indvidual IP addresses here https://ipinfo.io/ or use whois utility from console")
