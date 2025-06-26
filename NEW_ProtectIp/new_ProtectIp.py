import requests, json, base64, csv,warnings,os,glob
from urllib import parse

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def GetLoginToken():
    baseurl = 'https://192.168.28.180:8001'
    path = '/api/connect/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    form_data = {
        "grant_type": 'password',
        'scope': 'offline_access',
        'username': 'admin',
        'password': base64.b64encode('admin'.encode('UTF-8'))
    }
    data = parse.urlencode(form_data)
    r = requests.post(baseurl + path, headers=headers, data=data, verify=False)
    r = json.loads(r.text)
    token = 'Bearer ' + r['access_token']
    return token


def get_unprotected_hosts():
    url = 'https://192.168.28.180:8001/api/Hosts/Ipv4'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': GetLoginToken()
    }

    payload = {
        "skip": 0,
        "take": 1000,
        "filter": {
            "logic": "and",
            "filters": []
        }
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    if response.status_code != 200:
        print(f"API 請求失敗: {response.status_code}")
        return

    data = response.json()
    items = data.get('Data') or data.get('Items') or []

    for item in items:
        ip_info = item.get('IpInfo', {})
        mac_info = item.get('MacInfo', {})
        is_protected = ip_info.get('IsProtected')
        is_Online = ip_info.get('IsOnline')
        Is_AssignByDhcp = ip_info.get('IsAssignByDhcp')
        mac = mac_info.get('Mac')

        if ((is_protected is False and mac)and is_Online is True) and Is_AssignByDhcp is True:
            ip = ip_info.get('Ip', '未知IP')
            host_id = str(item.get('HostId', '未知ID'))
            ProtectIpWithMac(host_id, ip, mac)


def ProtectIpWithMac(HostId: str, IPS: str, MAC: str):
    url = "https://192.168.28.180:8001/api/Hosts/ProtectIpWithMac"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": GetLoginToken()
    }

    payload = {
        "HostId": HostId,
        "IP": IPS,
        "MAC": MAC,
        "IpCustomField": {},
        "MacCustomField": {}
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    if response.ok:
        print(f"✅ 成功綁定 HostID: {HostId}, IP: {IPS}, MAC: {MAC}")
    else:
        print(f"❌ 綁定失敗 HostID: {HostId}, 狀態碼: {response.status_code}")
        print(f"錯誤訊息: {response.text}")


# 執行
get_unprotected_hosts()
