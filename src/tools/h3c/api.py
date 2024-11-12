import requests
from urllib.parse import urlparse, urljoin
import tools.h3c.utils as utils
import xml.etree.ElementTree as ET
import json
from prettytable import PrettyTable


requests.packages.urllib3.disable_warnings()
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "DEFAULT@SECLEVEL=1"


class H3C(object):
    def __init__(self, address, flag):
        self.address = self.get_base_url(address)
        self.host = urlparse(self.address).hostname
        self.flag = flag
        self.session_id = self.get_session_id()

    @staticmethod
    def get_base_url(address):
        o = urlparse(address)
        return f"{o.scheme}://{o.netloc}"

    def get_session_id(self):
        path = "/wnm/frame/login.php"
        payload = {
            "flag": self.flag,
            "ssl": "true",
            "host": self.host,
            "lang": "cn",
        }
        headers = {"Referer": self.address}

        real_url = urljoin(self.address, path)
        r = requests.post(real_url, data=payload, headers=headers, verify=False)
        r.encoding = "utf-8"
        data = r.json()

        # 检查是否正确返回
        if data.get("sessionid"):
            return data.get("sessionid")

        else:
            print("Error: 获取sessionid失败，请检查用户名或密码是否正确")
            print(json.dumps(data, ensure_ascii=False))
            exit(1)

    def post(self, path, xml, req_menu):
        headers = {"Referer": self.address}
        data = {"xml": xml, "req_menu": req_menu}
        cookies = {"sessionid": self.session_id, self.session_id: "true"}
        real_url = urljoin(self.address, path)

        response = requests.post(
            real_url, headers=headers, data=data, cookies=cookies, verify=False
        )
        response.encoding = "utf-8"

        return response

    def get_local_user(self):
        path = "/wnm/get.j"
        req_menu = "M_Resource/M_User/M_UserControl/M_LocalUser"

        rpc_xml = utils.get_user_list_data()
        response = self.post(path, rpc_xml, req_menu)

        data = json.loads(response.text)
        accounts = data.get("UserAccounts", {}).get("Network", {}).get("Accounts", None)
        if accounts is None:
            print("Error: Accounts 不存在")
            print(response.text)
            exit(1)
        table = PrettyTable()
        table.field_names = [
            "Name",
            "UID",
            "GroupName",
            "ADVPN",
            "IKE",
            "IPoE",
            "LanAccess",
            "Portal",
            "PPP",
            "SSLVPN",
        ]

        for user in accounts:
            table.add_row(
                [
                    user["Name"],
                    user["UID"],
                    user["GroupName"],
                    user["ADVPN"],
                    user["IKE"],
                    user["IPoE"],
                    user["LanAccess"],
                    user["Portal"],
                    user["PPP"],
                    user["SSLVPN"],
                ]
            )
        print(table)

    def create_local_user(self, name, password, sslvpn):
        path = "/wnm/set.j"
        req_menu = "M_Resource/M_User/M_UserControl/M_LocalUser"

        if password is None:
            # 生成8位随机密码
            password = utils.gen_password()

        params = {"name": name, "password": password, "sslvpn": sslvpn}
        root = utils.get_create_user_data(**params)
        rpc_xml = ET.tostring(root, encoding="unicode", method="xml")
        response = self.post(path, rpc_xml, req_menu)

        data = json.loads(response.text)
        status = data.get("ok", None)
        if status is None:
            print(f"Error: 用户: {name} 创建失败")
            print(response.text)
            exit(1)
        if status == "ok":
            print(f"用户: {name} 创建成功")
            print(f"用户: {name}")
            print(f"密码: {password}")
        else:
            print(f"用户: {name} 创建失败，返回状态未知 {status}")

    def delete_local_user(self, name):
        path = "/wnm/set.j"
        req_menu = "M_Resource/M_User/M_UserControl/M_LocalUser"

        params = {"name": name}
        root = utils.get_delete_user_data(**params)
        rpc_xml = ET.tostring(root, encoding="unicode", method="xml")
        response = self.post(path, rpc_xml, req_menu)

        data = json.loads(response.text)
        status = data.get("ok", None)
        if status is None:
            print(f"Error: 用户: {name} 删除失败")
            print(response.text)
            exit(1)
        if status == "ok":
            print(f"用户: {name} 删除成功")
        else:
            print(f"用户: {name} 删除失败，返回状态未知 {status}")
