import requests, json, base64, warnings, csv,os,glob
from urllib import parse

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def auto_rename_csv():
    target_name = 'ProtectIpList.csv'
    if os.path.exists(target_name):
        print(f"✅ 已存在 {target_name}，跳過重新命名")
        return

    csv_files = glob.glob("*.csv")
    if not csv_files:
        print("❌ 目錄中找不到任何 .csv 檔案！")
        exit(1)

    first_csv = csv_files[0]
    os.rename(first_csv, target_name)
    print(f"將檔案 {first_csv} 重新命名為 {target_name}")

def get_token():
    url = 'https://192.168.28.180:8001/api/connect/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    form_data = {
        "grant_type": "password",
        "scope": "offline_access",
        "username": "admin",
        "password": base64.b64encode(b'admin').decode()
    }
    data = parse.urlencode(form_data)
    r = requests.post(url, headers=headers, data=data, verify=False)
    r.raise_for_status()
    return 'Bearer ' + r.json()['access_token']

def get_ip_ids_from_protection_table(id):
    url = f'https://192.168.28.180:8001/api/Hosts/IpProtection/Table/{id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': get_token()
    }
    payload = {}

    response = requests.post(url, headers=headers, json=payload, verify=False)
    if response.ok:
        try:
            data = response.json()
            ids = [item.get("Id") for item in data if isinstance(item, dict) and "Id" in item]
            return ids
        except json.JSONDecodeError:
            return []
    else:
        return []

def call_delete_protect_ip(id):
    url = f'https://192.168.28.180:8001/api/Hosts/IpProtection/Delete/{id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': get_token()
    }
    payload = {}

    response = requests.post(url, headers=headers, json=payload, verify=False)
    print(f"DEBUG: DELETE API 回應狀態碼 {response.status_code}")
    print(f"DEBUG: DELETE API 回應內容 {response.text}")

    if response.ok:
        print(f"✅ 成功刪除保護 IP，ID: {id}")
    else:
        print(f"❌ 刪除失敗，ID: {id}，狀態碼: {response.status_code}")
        print(f"錯誤訊息: {response.text}")


if __name__ == "__main__":
    auto_rename_csv()
    try:
        with open('ProtectIpList.csv', mode='r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # 跳過標題列
            for row in csv_reader:
                ip = row[0]
                mac = row[1]
                hostid = row[2] 
                hostid2 = int(hostid)-5
                isprotectIP = row[3]
                if isprotectIP.strip().upper() == 'TRUE':

                    ids = get_ip_ids_from_protection_table(hostid2)
                    if isinstance(ids, list) and len(ids) > 0:
                            target_id = ids[0]
                            print(f"✅  成功刪除 HostID: {hostid}, IP: {ip}, MAC: {mac}")
                            
                            call_delete_protect_ip(target_id)
                    else:
                            print(f"⚠️  HostID: {hostid} 找不到可刪除的 ID")
        # os.remove('ProtectIpList.csv')
        print("已成功刪除 ProtectIpList.csv")
    except Exception as e:
        print("⚠️ 發生錯誤，未刪除 CSV：", e)
    input("✅ 所有操作完成，請按 Enter 鍵結束程式...")
