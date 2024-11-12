import string
import random
import xml.etree.ElementTree as ET


# 定义基础类，用于构造各个XML元素
class XMLElement:
    def __init__(self, tag, attributes=None, text=None):
        self.tag = tag
        self.attributes = attributes if attributes else {}
        self.children = []
        self.text = text

    def add_child(self, child):
        self.children.append(child)

    def to_xml(self):
        element = ET.Element(self.tag, self.attributes)
        if self.text:
            element.text = self.text
        for child in self.children:
            element.append(child.to_xml())
        return element


# 构造更复杂的类，例如 AuthorizationInfo 和 BindingInfo 等
class AuthorizationInfo(XMLElement):
    def __init__(self):
        super().__init__("AuthorizationInfo")
        self.add_child(XMLElement("AclNumber"))
        self.add_child(XMLElement("CallbackNumber"))
        self.add_child(XMLElement("IdleTimeout"))
        self.add_child(XMLElement("UserProfile"))
        self.add_child(XMLElement("VLANID"))
        self.add_child(XMLElement("SSLVPNPolicy"))


class BindingInfo(XMLElement):
    def __init__(self):
        super().__init__("BindingInfo")
        self.add_child(XMLElement("Interface"))
        self.add_child(XMLElement("Ipv4Address"))
        self.add_child(XMLElement("MacAddress"))
        self.add_child(XMLElement("VLANID"))


class ValidityDateTime(XMLElement):
    def __init__(self):
        super().__init__("ValidityDateTime")
        self.add_child(XMLElement("StartValidityDateTime"))
        self.add_child(XMLElement("EndValidityDateTime"))


# 定义 Account 类
class Account(XMLElement):
    def __init__(self):
        super().__init__("Account")
        self.add_child(XMLElement("Name"))
        self.add_child(XMLElement("UID"))
        self.add_child(XMLElement("Description"))
        self.add_child(XMLElement("GroupName"))
        self.add_child(XMLElement("ADVPN"))
        self.add_child(XMLElement("IKE"))
        self.add_child(XMLElement("IPoE"))
        self.add_child(XMLElement("LanAccess"))
        self.add_child(XMLElement("Portal"))
        self.add_child(XMLElement("PPP"))
        self.add_child(XMLElement("SSLVPN"))
        self.add_child(XMLElement("AccessLimit"))
        self.add_child(XMLElement("CurrentAccessNum"))
        self.add_child(AuthorizationInfo())
        self.add_child(BindingInfo())
        self.add_child(ValidityDateTime())


# 定义 Accounts 类
class Accounts(XMLElement):
    def __init__(self):
        super().__init__("Accounts")
        self.add_child(Account())


# 定义 Network 类
class Network(XMLElement):
    def __init__(self):
        super().__init__("Network")
        self.add_child(Accounts())
        self.add_child(IdentityGroups())


class IdentityGroups(XMLElement):
    def __init__(self):
        super().__init__("IdentityGroups")
        identity_group = XMLElement("IdentityGroup")
        identity_group.add_child(XMLElement("UserName"))
        identity_group.add_child(XMLElement("GroupName"))
        self.add_child(identity_group)


# 定义 UserAccounts 类
class UserAccounts(XMLElement):
    def __init__(self):
        super().__init__("UserAccounts")
        self.add_child(Network())
        self.add_child(UserGroups())
        self.add_child(UserGroup())
        self.add_child(Management())


class UserGroups(XMLElement):
    def __init__(self):
        super().__init__("UserGroups")
        group = XMLElement("Group")
        group.add_child(XMLElement("Name"))
        group.add_child(AuthorizationInfo())
        self.add_child(group)


class UserGroup(XMLElement):
    def __init__(self):
        super().__init__("UserGroup")
        identity_members = XMLElement("IdentityMembers")
        identity_member = XMLElement("IdentityMember")
        identity_member.add_child(XMLElement("GroupName"))
        identity_member.add_child(XMLElement("UserName"))
        identity_members.add_child(identity_member)
        self.add_child(identity_members)
        identity_groups = XMLElement("IdentityGroups")
        identity_group = XMLElement("IdentityGroup")
        identity_group.add_child(XMLElement("GroupName"))
        identity_group.add_child(XMLElement("IdentityGroup"))
        identity_groups.add_child(identity_group)
        self.add_child(identity_groups)


class Management(XMLElement):
    def __init__(self):
        super().__init__("Management")
        accounts = XMLElement("Accounts")
        account = XMLElement("Account")
        account.add_child(XMLElement("Name"))
        account.add_child(XMLElement("GroupName"))
        accounts.add_child(account)
        self.add_child(accounts)

        self.add_child(UserRoles())


class UserRoles(XMLElement):
    def __init__(self):
        super().__init__("UserRoles")
        user_role = XMLElement("UserRole")
        user_role.add_child(XMLElement("UserName"))
        user_role.add_child(XMLElement("RoleName"))
        self.add_child(user_role)


# 定义 Top 类
class Top(XMLElement):
    def __init__(self):
        attributes = {
            "xmlns": "http://www.h3c.com/netconf/data:1.0",
            "xmlns:web": "http://www.h3c.com/netconf/base:1.0",
            "xmlns:data": "http://www.h3c.com/netconf/data:1.0",
        }
        super().__init__(
            "top",
            attributes,
        )
        self.add_child(UserAccounts())
        self.add_child(Device())


# 定义 Device 类
class Device(XMLElement):
    def __init__(self):
        super().__init__("Device")
        base = XMLElement("Base")
        base.add_child(XMLElement("LocalTime"))
        clock_protocol = XMLElement("ClockProtocol")
        clock_protocol.add_child(XMLElement("MDCID"))
        clock_protocol.add_child(XMLElement("Protocol"))
        base.add_child(clock_protocol)
        time_zone = XMLElement("TimeZone")
        time_zone.add_child(XMLElement("Zone"))
        time_zone.add_child(XMLElement("ZoneName"))
        base.add_child(time_zone)
        base.add_child(XMLElement("HostName"))
        self.add_child(base)


# 定义 Filter 类
class Filter(XMLElement):
    def __init__(self):
        super().__init__("filter", {"type": "subtree"})
        self.add_child(Top())


# 定义 Get 类
class Get(XMLElement):
    def __init__(self):
        super().__init__("get")
        self.add_child(Filter())


# 定义 RPC 类
class RPC(XMLElement):
    def __init__(self, message_id, get=None):
        super().__init__(
            "rpc",
            {
                "message-id": message_id,
                "xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
                "xmlns:web": "urn:ietf:params:xml:ns:netconf:base:1.0",
            },
        )
        if get:
            self.add_child(Get())


def get_user_list_data(message_id="101"):
    """
    生成获取用户列表xml
    :param message_id:
    :return:
    """
    r = RPC(message_id, get=True)
    data = ET.tostring(r.to_xml(), encoding="unicode", method="xml")
    return data


def get_network_user(
    username=None, enable_state=None, check_samechar=None, check_username=None
) -> ET.Element:
    """

    :param username:
    :param enable_state:
    :param check_samechar:
    :param check_username:
    :return:
    """
    network_user = ET.Element("NetworkUser")
    if username is not None:
        u = ET.SubElement(network_user, "UserName")
        u.text = username
    if enable_state is not None:
        e_s = ET.SubElement(network_user, "EnableState")
        e_s.text = enable_state
    if check_samechar is not None:
        c_s = ET.SubElement(network_user, "CheckSameChar")
        c_s.text = check_samechar
    if check_username is not None:
        c_u = ET.SubElement(network_user, "CheckUserName")
        c_u.text = check_username
    return network_user


def get_account(**kwargs):
    """
    为具有可选字段的帐户创建 XML 元素。

    :param kwargs: 帐户字段的可选关键字参数。
    - name: str, Account name
    - password: str, Account password
    - advpn: str, ADVPN
    - ike: str, IKE
    - ipoe: str, IPoE
    - lanaccess: str, LanAccess
    - portal: str, Portal
    - ppp: str, PPP
    - sslvpn: str, SSLVPN
    :return: ET.Element，表示帐户的 XML 元素。
    """
    account = ET.Element("Account")
    fields = [
        "Name",
        "Password",
        "ADVPN",
        "IKE",
        "IPoE",
        "LanAccess",
        "Portal",
        "PPP",
        "SSLVPN",
    ]

    for field in fields:
        value = kwargs.get(field.lower())
        if value is not None:
            sub_element = ET.SubElement(account, field)
            if isinstance(value, bool):
                value = str(value).lower()
            sub_element.text = value
    return account


def get_create_user_data(**kwargs):
    # 创建根元素
    root = ET.Element(
        "rpc",
        attrib={
            "message-id": "101",
            "xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
            "xmlns:web": "urn:ietf:params:xml:ns:netconf:base:1.0",
        },
    )

    edit_config = ET.SubElement(root, "edit-config")
    target = ET.SubElement(edit_config, "target")
    running = ET.SubElement(target, "running")

    config = ET.SubElement(edit_config, "config")

    top = ET.SubElement(
        config,
        "top",
        {
            "xmlns": "http://www.h3c.com/netconf/config:1.0",
            "web:operation": "create",
        },
    )

    user_accounts = ET.SubElement(top, "UserAccounts")
    network = ET.SubElement(user_accounts, "Network")
    accounts = ET.SubElement(network, "Accounts")
    accounts.append(get_account(**kwargs))

    # 生成 XML 字符串
    # xml_str = ET.tostring(root, encoding="unicode", method="xml")
    #
    # return xml_str
    return root


def get_delete_user_data(**kwargs):
    root = get_create_user_data(**kwargs)
    for top in root.iter("top"):
        top.set("web:operation", "remove")
    return root


def gen_password(length=8):
    """
    从大写字母，小写字母，数字，特殊字符中，生成指定长度随机密码

    :param length: 密码长度
    :return: 密码
    """
    special = " ~`!@#$%^&*()_+-={}|[]\\:;\"'<>,./"
    chars = string.ascii_letters + string.digits + special
    # 得出的结果中字符会有重复的
    return "".join([random.choice(chars) for i in range(length)])
    # 得出的结果中字符不会重复
    # return "".join(random.sample(chars, length))


if __name__ == "__main__":
    # # 构造完整的 XML 结构
    # rpc = RPC("101", edit_config=True)
    #
    # # 输出 XML 字符串
    # rpc_xml = ET.tostring(rpc.to_xml(), encoding="unicode", method="xml")
    #
    # print(rpc_xml)
    for i in range(10):
        print(gen_password())
