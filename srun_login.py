import msvcrt
import subprocess
import requests
import time
import re
import base64
from data import srun_xencode
from data import srun_base64
from data import srun_md5
from data import srun_sha1

header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
username = ''
password = ''
pwd_base64 = ''
url_login_page = "http://10.8.8.8/srun_portal_pc?ac_id=10&theme=pro"
url_get_challenge = "http://10.8.8.8/cgi-bin/get_challenge"
url_login_api = "http://10.8.8.8/cgi-bin/srun_portal"
n = '200'
vtype = '1'
ac_id = '10' # I-XG无线网使用5，有线网使用10
enc = "srun_bx1"
ts = ''
ip = ''
token = ''
info = ''
encrypted_info = ''
md5 = ''
encrypted_md5 = ''
chkstr = ''
encrypted_chkstr = ''
login_response = ''
login_result = ''

def login():
    global pwd_base64
    pwd_base64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    get_ip()
    get_token()
    get_login_response()

def get_ip():
    global ip
    global url_login_page
    response = requests.get(url_login_page, headers=header)
    ip = re.search(r'ip\s*:\s*"(\d+\.\d+\.\d+\.\d+)"', response.text).group(1)
    print("正在获取ip: " + ip)

def get_token():
    global ts
    global token
    timestamp_sec = time.time()
    timestamp_ms = int(timestamp_sec * 1000)
    ts = timestamp_ms
    params_get_challenge = {
        "callback": "jQuery1124014201194569325093_" + str(ts),
        "username": username,
        "ip": ip,
        "_": str(ts)
    }
    response = requests.get(url_get_challenge, params=params_get_challenge, headers=header)
    token = re.search('"challenge":"(.*?)"', response.text).group(1)
    print("正在获取Challenge: " + token)

def get_login_response():
    generate_encrypted_login_info()
    send_login_info()
    resolve_login_responce()
    print("登录结果：" + login_result)
    
def generate_encrypted_login_info():
    global info
    global encrypted_info
    global md5
    global encrypted_md5
    global chkstr
    global encrypted_chkstr
    info_params = {
        "username": username,
        "password": pwd_base64,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc,
    }
    info = re.sub("'",'"',str(info_params))
    info = re.sub(" ",'',info)
    encrypted_info = "{SRBX1}" + srun_base64.get_base64(srun_xencode.get_xencode(info, token))
    md5 = srun_md5.get_md5(pwd_base64, token)
    encrypted_md5 = "{MD5}" + md5
    chkstr = token + username
    chkstr += token + md5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + vtype
    chkstr += token + encrypted_info
    encrypted_chkstr = srun_sha1.get_sha1(chkstr)
    print("加密工作完成")
    
def send_login_info():
    global login_response
    login_info_params = {
        'callback': 'jQuery1124014201194569325093_' + str(ts),
        'action':'login',
        'username': username,
        'password': encrypted_md5,
        'os': "Windows 10",
        'name': 'Windows',
        'double_stack': 0,
        'chksum': encrypted_chkstr,
        'info': encrypted_info,
        'ac_id': ac_id,
        'ip': ip,
        'n': n,
        'type': vtype,
        '_': str(ts)
    }
    print("尝试登录中...")
    # print(login_info_params)
    login_response = requests.get(url_login_api, params=login_info_params, headers=header)
    # print("请求结果: " + login_response.text)

def resolve_login_responce():
    global login_result
    login_result = re.search('"res":"(.*?)"', login_response.text).group(1)
    if login_result == 'login_error' :
        login_result = re.search('"error_msg":"(.*?)"', login_response.text).group(1)
    if login_response.text.__contains__('ip_already_online_error'):
        login_result = '您已在线！'
  
# 断线重连代码
# def ping_baidu():
#     try:
#         subprocess.check_call(['ping', '-n', '1', '-w', '5000', 'baidu.com'])
#         return True
#     except subprocess.CalledProcessError:
#         return False

# 断线重连代码
# while True:
#     if not ping_baidu():
#         file_path = "data/accounts.txt"
#         with open(file_path, 'r') as file:
#             line = file.readline()
#             parts = line.strip().split()
#             if len(parts) == 3:
#                 username, password, ac_id = parts
#                 print("校园网断线重连中...")
#                 print("正在获取账号: " + username)
#                 print("正在获取ac_id: " + ac_id)
#                 login()
#     time.sleep(10)

# if __name__ == '__main__':
#     file_path = "data/accounts.txt"
#     with open(file_path, 'r') as file:
#         line = file.readline()
#         parts = line.strip().split()
#         if len(parts) == 3:
#             username, password, ac_id = parts
#             print("校园网自动登录中...")
#             print("正在获取账号: " + username)
#             print("正在获取ac_id: " + ac_id)
#             login()
#             print("按下任意键退出...")
#             msvcrt.getch()