from scapy.all import ARP, Ether, srp
import platform,json,subprocess


def GetIPv4MAC(dstip:str)->str | None:
    arprequest = Ether(src='00:e0:4c:68:5a:55',dst = 'ff:ff:ff:ff:ff:ff')\
        /ARP(op=1,hwsrc='00:e0:4c:68:5a:55', hwdst="00:00:00:00:00:00",psrc='192.168.28.3', pdst=dstip)
    result ,nums = srp(arprequest, retry=2,timeout=5,iface='乙太網路 2')
    return result[0][1][ARP].hwsrc if result else None

def arp_scan(target_ip_range):
    # 建立乙太封包 (Ether) + ARP 掃描
    arp = ARP(pdst=target_ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # 廣播封包
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=False,iface='乙太網路 2')[0]

    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })

    return devices
def write_json(data):
    with open('ARP.txt','w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)




if __name__ == "__main__":
    a = GetIPv4MAC('192.168.28.254')
    pass

    results = []
    devices = arp_scan("192.168.28.0/24")

    for dev in devices:       
        results.append(f'上線中MAC : {dev}')
        print(f"IP: {dev['ip']}    MAC: {dev['mac']}")

    write_json(results)