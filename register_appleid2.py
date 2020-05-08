# -*- coding: utf-8 -*-
import datetime
import poplib
import random
import re

import MySQLdb
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# from auto_register.ydm import use_ydm
# from testdir.zhptest.kill_z import restart_process
# from testdir.zhptest.mv_dir import mv_dir

PC_UAS = [
    "Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 V1_AND_SQ_5.3.1_196_YYB_D QQ/5.3.1.2335 NetType/WIFI",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36",


]


import json
import time
import requests

class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'
    username = 'zhp123'
    password = 'zhp123456'
    appid = '1'
    appkey = '22cc5376925e9387a23cf797cb9ba745'

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if cid > 0:
            for i in range(0, timeout):
                result = self.result(cid)
                if result != '':
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if response:
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb')
        res = requests.post(url, files=files, data=fields)
        return res.text


def use_ydm(filename):
    apiurl = 'http://api.yundama.com/api.php'
    username = 'zhp123'
    password = 'zhp123456'
    appid = '1'
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    code_type = 1005  # 验证码类型
    timeout = 60  # 超时时间，秒
    yundama = YDMHttp(username, password, appid, appkey)  # 初始化
    balance = yundama.balance()  # 查询余额
    print('您的题分余额为{}'.format(balance))
    cid, result = yundama.decode(filename, code_type, timeout)  # 开始识别
    print('识别结果为{}'.format(result))
    return result

import psutil
def restart_process():
    pids = psutil.pids()
    for pid in pids:
        try:
            process = psutil.Process(pid=pid)
            command = " ".join(process.cmdline())
            command = command.lower()
            if "chromedriver.exe" in command or "chrome.exe" in command:
                process.kill()
                process.send_signal(9)
                print(pid)
        except:
            pass
        time.sleep(1.5)

import os
import shutil

def mv_dir():
    delList = []
    delDir = b"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
    delList = os.listdir(delDir)
    for f in delList:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)

def get_email():
    mysql_config2 = {"host": "192.168.14.90",
                     "port": 3306,
                     'user': 'root',
                     "passwd": '123456',
                     "db": 'apple',
                     "charset": "utf8"}
    conn2 = MySQLdb.connect(**mysql_config2)
    cursor2 = conn2.cursor()
    cursor2.execute("select `email` , password from email order by id asc")
    info = cursor2.fetchall()
    data = []
    for email, password in info:
        data.append({
            'email': email,
            'passwd': password
        })
    return data


# 读取邮件信息获取验证码
def recv_email_by_pop3(email_address, password):
    import imaplib
    # 这里的服务器根据需要选择
    server = imaplib.IMAP4_SSL("outlook.office365.com",993)
    server.login(email_address, password)
    # 邮箱中的文件夹，默认为'INBOX'
    try:
        inbox = server.select("INBOX")
        typ, data = server.search(None, "ALL")
        msgList = data[0].split()
        latest = msgList[len(msgList) - 1]
        typ, datas = server.fetch(latest, '(RFC822)')
            # 使用utf-8解码
        msg_content = (b''.join(datas[0]).decode('utf-8')[2600:3200]).replace('\r\n','')
        code = re.findall("x-ds-vetting-token: (.*?)X-DKIM_SIGN_REQUIRED", msg_content)[0]
        server.close()
        return code
    except:
        inbox = server.select("Junk")
        typ, data = server.search(None, "ALL")
        msgList = data[0].split()
        latest = msgList[len(msgList) - 1]
        typ, datas = server.fetch(latest, '(RFC822)')
        # 使用utf-8解码
        msg_content = (b''.join(datas[0]).decode('utf-8')[2600:3200]).replace('\r\n', '')
        code = re.findall("x-ds-vetting-token: (.*?)X-DKIM_SIGN_REQUIRED", msg_content)[0]
        server.close()
        return code




# 生成出生日期
def create_assist_date():
    datestart = "1970-06-28"
    dateend = '2000-06-28'
    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y%m%d'))
    return date_list


def get_user():
    # 获取用户信息
    mysql_config2 = {"host": "192.168.14.90",
                         "port": 3306,
                         'user': 'root',
                         "passwd": '123456',
                         "db": 'apple',
                         "charset": "utf8"}
    conn2 = MySQLdb.connect(**mysql_config2)
    cursor2 = conn2.cursor()
    cursor2.execute("select last_name,`name`,`work`,air,street,home,phone,air1 from user_info order by id asc")
    info = cursor2.fetchall()
    return info

# 注册苹果id
def register(email, passwd):
    date_birth = random.choice(create_assist_date())  # 日期
    email = email
    passwd = passwd
    user_info = get_user()
    name = json.loads(user_info[0][1])
    answer1 = random.choice(name)
    work = json.loads(user_info[0][2])
    answer2 = random.choice(work)
    air = json.loads(user_info[0][3])
    answer3 = random.choice(air)
    last_name = json.loads(user_info[0][0])

    chrome_options = webdriver.ChromeOptions()
    u_a = 'user-agent=' + random.choice(PC_UAS)
    u_lan = 'accept-language: zh-CN,zh;q=0.9'
    chrome_options.add_argument(u_lan)
    chrome_options.add_argument(u_a)
    chrome_options.add_argument('accept-encoding="gzip, deflate, br"')
    # webdriver  被识别出来优化
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 启用无痕模式
    chrome_options.add_argument('--incognito')
    # 禁用js
    chrome_options.add_argument('--disable-javascript')
    # chrome_options.add_argument('--proxy-server=http://192.168.14.40:3131')
    url = "https://appleid.apple.com/account#!&page=create"
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="C:\\Users\ceshi\Desktop\chrome\Chrome-bin\chromedriver.exe",
    #                           chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path="C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe", chrome_options=chrome_options)
    driver.set_script_timeout(50)
    try:
        driver.get(url)
        time.sleep(20)
    except:
        driver.refresh()  # 刷新页面
        time.sleep(30)
    # 将窗口调整最大
    driver.maximize_window()
    time.sleep(35)
    # 验证码截图
    try:
        driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[1]/div/idms-captcha/'
                                 'div/div/img').screenshot('dm.png')
    except:
        driver.refresh()  # 刷新页面
        driver.implicitly_wait(35)
        driver.find_element_by_xpath(
            '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[1]/div/idms-captcha/'
            'div/div/img').screenshot('dm.png')

    # 识别验证码的图片
    time.sleep(11)
    ym_info = use_ydm('dm.png')
    if 'DDDD' in str(ym_info):
        # 重新截图
        driver.find_element_by_xpath(
            '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[1]/div/idms-captcha/'
            'div/div/img').screenshot('dm.png')
        # 识别验证码的图片
        ym_info = use_ydm('dm.png')
        time.sleep(11)
    print(email, passwd)
    if ym_info and 'DDDD' not in str(ym_info):
        # 姓氏
        mysql_config2 = {"host": "192.168.14.90",
                         "port": 3306,
                         'user': 'root',
                         "passwd": '123456',
                         "db": 'apple',
                         "charset": "utf8"}
        conn2 = MySQLdb.connect(**mysql_config2)
        cursor2 = conn2.cursor()
        time.sleep(5)
        try:
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[1]/div/div/last-name-input/div/idms-textbox'
                                         '/idms-error-wrapper/div/div/input').send_keys(random.choice(last_name))
            time.sleep(2)
            # 姓名
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[2]/div/div/first-name-input/div/id'
                                         'ms-textbox/idms-error-wrapper/div/div/input').send_keys(random.choice(name))
            time.sleep(2)
            # 下拉框选择 国家
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/idms-dropdown/div/idms-er'
                                                'ror-wrapper/div/div/select')).select_by_value('USA')

            time.sleep(2.5)
            # 日期
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[3]/div/wc-birthday/div/div/d'
                                         'iv/div/masked-date/idms-error-wrapper/div/div/input').send_keys(date_birth)
            time.sleep(2.5)

            # 邮箱
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[1]/div/account-name/div/div/email-input/div/idms-textbox/idms-error-wrapper/div/'
                                         'div/input').send_keys(email)

            time.sleep(2.5)
            # 密码
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/new-password/div/div/password-input/d'
                                         'iv/input').send_keys(passwd)

            time.sleep(2.5)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/confirm-password/div/div/confirm-password-input/div/idms-textbox/idms'
                                         '-error-wrapper/div/div/input').send_keys(passwd)

            time.sleep(2.5)
            # 问题1
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[1]/security-question/div/div[1]/idms-dropdown/div/idms-error'
                                                '-wrapper/div/div/select')).select_by_value('130')
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[1]/security-answer/div/idms-textbox/idms-error-wrapper/div/div/input')\
                .send_keys(answer1)
            time.sleep(3)
            # 问题2
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-question/div/div[1]'
                                                '/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('136')

            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-answer/div/idms-'
                                                'textbox/idms-error-wrapper/div/div/input').send_keys(answer2)

            time.sleep(3)
            # 问题3
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[3]/security-questi'
                                                'on/div/div[1]/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('142')
            time.sleep(2.5)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[3]/security-answer/div/idms-textbox/'
                                         'idms-error-wrapper/div/div/input').send_keys(answer3)

            time.sleep(2)
            # 图片识别
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[2]/div/div[1]/captcha-input/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(ym_info)
            except:
                driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[6]/div/create-captcha/div/div/div/div/div[2]/div/div[1]/captcha-input/div/idms-textbox/idms-error-wrapper/div/div/'
            
                                         'input').send_keys(ym_info)
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/'
            
                                         'div/div[3]/idms-toolbar/div/div/div/button').click()
            time.sleep(40)
            driver.implicitly_wait(45)
            # 读取邮箱信息 填写验证码
            try:
                code = recv_email_by_pop3(email, passwd)
            except:
                code = recv_email_by_pop3(email, passwd)
            else:
                code = code
            print('code:', code)
            if code:
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[1]/input').send_keys(code[0])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[2]/input').send_keys(code[1])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[3]/input').send_keys(code[2])
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[4]/input').send_keys(code[3])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[5]/input').send_keys(code[4])
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[6]/input').send_keys(code[5])
                time.sleep(1.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[3]/idms-toolbar/div/div[1]/div/button[1]').click()
                time.sleep(70)
                driver.implicitly_wait(50)
                driver.set_script_timeout(70)
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[3]/idms-toolbar/div/div[1]/div/button[1]').click()
                    time.sleep(10)
                except:
                    pass
                # 完善发货信息
                street = json.loads(user_info[0][4])
                homes = json.loads(user_info[0][5])
                air = json.loads(user_info[0][7])
                air = random.choice(air)
                air1 = air.get('air')
                code = random.choice(air.get('code'))
                mobile = random.choice(air.get('mobile'))
                # 编辑按钮
                driver.implicitly_wait(40)
                try:
                    print('编辑。。。。.')
                    time.sleep(60)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                               '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    time.sleep(35)
                    driver.implicitly_wait(35)
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div[3]/div[2]/button").click()

                time.sleep(15)
                # 街道地址
                print('#######################')
                try:
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/idms-textbox/idms-error-wrapper/div/div/i'
                                                 'nput').send_keys(random.choice(street))
                except:
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                 '/div/div[2]/div[3]/button').click()
                    time.sleep(6)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
                        random.choice(street))

                time.sleep(3)
                # 单元
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[3]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(random.choice(homes))
                time.sleep(2.5)
                # 城市
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[4]/div/div/div/idms-textbox/idms-e'
                    'rror-wrapper/div/div/input').send_keys(air1)
                time.sleep(2)
                # 州  AL
                Select(driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[5]/div/div/div/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('AL')
                time.sleep(3)
                # 邮编
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[6]/div/div/div/idms-textbox/idms-error'
                    '-wrapper/div/div/input').send_keys(code)
                time.sleep(3)
                # 电话
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[7]/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(mobile)
                time.sleep(3)
                # 拷贝
                driver.implicitly_wait(10)
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[2]/div/label/span').click()
                time.sleep(10)
                info = driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[1]/shipping-address/div/section/idms-address/div/div/div[7]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')
                if info:
                    # 保存
                    print('拷贝成功。。。。。。。')
                    driver.implicitly_wait(45)
                    time.sleep(5)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button[1]').click()
                    time.sleep(80)
                    driver.implicitly_wait(45)
                    print('保存中')
                    driver.set_script_timeout(70)
                else:
                    # 尝试再次拷贝保存
                    time.sleep(15)
                    driver.implicitly_wait(10)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[2]/div/label/span').click()
                    driver.implicitly_wait(17)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button[1]').click()
                driver.implicitly_wait(15)
                time.sleep(9)
                # 查看是否保存成功
                # 编辑
                try:
                    print('保存后再次编辑查看信息。。。。.')
                    time.sleep(45)
                    driver.set_script_timeout(70)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                               '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    driver.implicitly_wait(35)
                    time.sleep(40)
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.refresh()  # 刷新页面
                        driver.implicitly_wait(35)
                        driver.find_element_by_xpath(
                            '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                        # driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div[3]/div[2]/button").click()

                time.sleep(13)
                driver.set_page_load_timeout(50)
                print('*****************')
                driver.implicitly_wait(10)
                # 获取编辑信息：
                # 付款邮编
                email_info1 = driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[6]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')

                time.sleep(1)
                # 发货邮编
                email_info2 = driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[1]/shipping-address/div/section/idms-address/div/div/div[7]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')
                if email_info1 and email_info2:
                    print(email_info1)
                    print(email_info2)
                    # 编辑信息保存成功
                    json_data = {
                        'problem1': '你少年时代最好的朋友叫什么名字？',
                        'answer1': answer1,
                        'problem2': '你的理想工作是什么？',
                        'answer2': answer2,
                        'problem3': '你的父母是在哪里认识的？',
                        'answer3': answer3,
                    }
                    json_data = json.dumps(json_data)
                    try:
                        # state  激活状态0 注册编辑信息  1 激活
                        cursor2.execute("insert into apple(apple_id,passwd,json_data,state) values(%s,%s,%s,%s)", (str(email), passwd,json_data,0))
                        conn2.commit()
                        print('ok')
                    except Exception as e:
                        print(e)
                        pass
                    time.sleep(3)
            driver.delete_all_cookies()
            time.sleep(5)
            driver.close()
            driver.quit()

        except Exception as e:
            print(e)
            driver.close()
            driver.quit()
    else:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    while 1:
        info = get_email()
        mysql_config2 = {"host": "192.168.14.90",
                         "port": 3306,
                         'user': 'root',
                         "passwd": '123456',
                         "db": 'apple',
                         "charset": "utf8"}
        conn2 = MySQLdb.connect(**mysql_config2)
        cursor2 = conn2.cursor()
        cursor2.execute("select apple_id from apple order by id desc")
        a_id = cursor2.fetchall()
        except_num = []
        id_num = []
        for i in info:
            email = i.get('email')
            passwd = i.get('passwd')
            if str(email) in str(a_id):
                pass
            else:
                print(email, passwd)
                try:
                    id_num.append(passwd)
                    start_time = int(time.time())
                    register(email, passwd)
                    restart_process()
                    mv_dir()
                    print('注册需要时间%s' % (int(time.time() - start_time)))
                except Exception as e:
                    print(e)
                    except_num.append(str(e))
                    pass
                time.sleep(300)
                if len(except_num) > 5 and len(id_num) > 10:
                    # 异常超过 5次 办个小时运行一次
                    print('出现异常，1个小时再运行')
                    except_num.clear()
                    id_num.clear()
                    time.sleep(3600)
