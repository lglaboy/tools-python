import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

IV = "2222222222222222"
KEY = "1111111111111111"


def para_string_byte_length(c):
    a = 0
    d = 0
    for v in c:
        a = ord(v)
        if a < 127:
            d = d + 1
        else:
            if 128 <= a <= 2047:
                d += 2
            else:
                if 2048 <= a <= 65535:
                    d += 3
                else:
                    d += 4
    return d


# 按照指定规则，拼接字符串
def combine_username_password(username, password):
    user_length = para_string_byte_length(username)
    password_length = len(password)
    o = ""
    b = ""
    if user_length < 10:
        o = "00" + str(user_length) + username
    elif user_length < 100:
        o = "0" + str(user_length) + username
    else:
        o = user_length + username

    if password_length < 10:
        b = "00" + str(password_length) + password
    elif password_length < 100:
        b = "0" + str(password_length) + password
    else:
        b = password_length + password

    return o + b


# 对用户名密码加密
def encrypt_user_password(username, password):
    s = combine_username_password(username, password)
    cipher = AES.new(KEY.encode("utf-8"), AES.MODE_CBC, IV.encode("utf-8"))
    m = cipher.encrypt(pad(s.encode("utf-8"), AES.block_size))
    return base64.b64encode(m).decode("utf-8")


def split_username_password(flag):
    user_length = int(flag[:3])
    user = flag[3 : 3 + user_length]
    password_length_start = 3 + user_length
    password_length_end = password_length_start + 3
    password_length = int(flag[password_length_start:password_length_end])

    password = flag[
        password_length_start + 3 : password_length_start + 3 + password_length
    ]

    return user, password


# 解密flag
def decrypt_user_password(flag):
    cipher = AES.new(KEY.encode("utf-8"), AES.MODE_CBC, IV.encode("utf-8"))
    m = unpad(cipher.decrypt(base64.b64decode(flag)), AES.block_size)

    return split_username_password(m)


# 示例使用
if __name__ == "__main__":
    data = encrypt_user_password("test", "password")
    print(data)
