from scapy.all import ARP, Ether, srp

#'00:e0:4c:68:5a:55' 'ff:ff:ff:ff:ff:ff' "00:00:00:00:00:00"

def getIPV4MAC(src,psrc,dstip:str):
    arprequest = Ether(src=src,dst='ff:ff:ff:ff:ff:ff') \
        / ARP(op=1,hwsrc=src,hwdst='00:00:00:00:00:00',psrc=psrc,pdst=dstip)
    result , nums = srp(arprequest, retry=2, timeout =5,iface='乙太網路 2')
    return result[0][1][ARP].hwsrc if result else None


for i in range(10):
    # 計算遞增的 IP 和 MAC 尾數
    current_ip = f"{'192.168.28.'}{(1 + i) % 256}"
    current_mac_suffix = (0xbc + i) % 256
    fake_mac = f"{"12:34:56:78:9a"}:{current_mac_suffix:02x}" # 188 (十六進位 bc)

    a = getIPV4MAC(fake_mac,current_ip,'192.168.28.172')
