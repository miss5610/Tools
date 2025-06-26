
import platform,json,subprocess,re,ARP, Ether, srp
from scapy.all import ARP, Ether, srp

def read_iplist(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]
    
def ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    result = subprocess.run(['ping',param,'1',ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return result.returncode == 0

def get_arp_ip_mac_list():
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    output = result.stdout
    ip_mac_dict = {}

    for line in output.splitlines():
        # 排除表頭或空行
        if 'Internet Address' in line or line.strip() == '':
            continue

        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            mac = parts[1]
            if re.match(r'\d+\.\d+\.\d+\.\d+', ip) and re.match(r'([0-9a-f]{2}[-:]){5}[0-9a-f]{2}', mac, re.IGNORECASE):
                ip_mac_dict[ip] = mac

    return ip_mac_dict

def write_json(data):
    with open('Ping','w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def main():
    iplist = read_iplist('iplist.txt')
    arp_dict = get_arp_ip_mac_list()
    results = []
    for ip in iplist:
        success = ping(ip)
        status = '上線中' if success else '離線中'
        mac = arp_dict.get(ip,'null')
        results.append({
            'ip' : ip ,
            'status' : status,
            'mac' : mac,
            'success' : success
        })
        print(f'{ip} {status}，MAC : {mac}')
    write_json(results)

if __name__ == '__main__':
    main()