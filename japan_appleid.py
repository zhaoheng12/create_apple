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


def get_email():
    # 获取邮箱信息
    mysql_config2 = {"host": "192.168.14.90",
                     "port": 3306,
                     'user': 'root',
                     "passwd": '123456',
                     "db": 'apple',
                     "charset": "utf8"}
    conn2 = MySQLdb.connect(**mysql_config2)
    cursor2 = conn2.cursor()
    cursor2.execute("select `email` , password from email_japan order by id asc")
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
    except Exception as e:
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


def airs1():
    prelist = ["090", "080", "070"]
    mobile = random.choice(prelist) + "-" + "".join(random.choice("0123456789") for i in range(4)) + "-" + "".join(
        random.choice("0123456789") for i in range(4))
    air = [
        {
            'air': '大阪市',
            'code': '593-8324',
            'mobile': mobile
        },
        {
            'air': '堺市道',
            'code': '593-8324',
            'mobile': mobile
        },

        {
            'air': '池田市',
            'code': '503-0936',
            'mobile': mobile
        },
        {
            'air': '吹田市',
            'code': '564-0041',
            'mobile': mobile
        },
        {
            'air': '泉大津市',
            'code': '595-0054',
            'mobile': mobile
        },
    ]

    info = random.choice(air)
    return info


# 注册苹果id
def register(email, passwd):
    last_name = ['Allison', 'acob', 'dfa', 'Michael', 'make', 'Ethan', 'nisang', 'Joshua', 'Qinshuy', 'Alexander',
                 'Ylsd',
                 'Anthony', 'andongni', 'William', 'Christopher', 'Jayden', 'jiedun', 'Andrew', 'ande', 'Smith',
                 'Yhans', 'Johnson', 'wlsia', 'Williams', 'bulang', 'Brown', 'qis', 'Jones', 'mile', 'Miller', 'dawisi',
                 'Davis', 'jiaxi', 'Garcia', 'Rodriguez',
                 'Wilson']

    name = ['Caden', 'Tyler', 'Dylan', 'Jaden', 'Logan', 'Caleb', 'Lucas', 'Joseph', 'Daniel', 'Christopher', 'Gavin',
            'Austin', 'Evan', 'Cameron', 'Luke', 'Christian', 'John', 'Samuel','Lauren',  'Katherine','Julia', 'Jordan',  'Morgan','Zoe', 'Rachel', 'Katherine',  'Kyra','Allison', 'acob', 'yagebu', 'Michael', 'Ethan',  'Joshua',
         'yelis','Anthony', 'andongni', 'weila', 'Christopher', 'mair', 'Jayden', 'lis', 'Andrew','Sophia', 'Emma', 'Aiden', 'Jacob', 'Ethan', 'Matthew']

    work = ['作业员', '技术员', '工程师', '设计师', '管理员', '总务人员', '服务', '厨师', '服务员', '营销人员', '保安', '司机', '导游', '售票员', '调酒师', '营业员',
            '促销', '保姆', '健康', '医生', '护士', '药剂师', '营养师', '后勤', '健身教练', '按摩技师', '娱乐类', '演员', '导演', '制片', '经纪', '编剧', '场务',
            '音乐人']
    air = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delware', 'Florida',
            'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', '龙亭', '顺河回族', '鼓楼', '禹王台', '金明', '杞县', '通许', '尉氏',
            '开封',
            '福井市', '甲府市', '长野市', '岐阜市', '静冈市', '名古屋市', '津市自', '大津市', '京都市', '嵩县', '汝阳', '宜阳', '洛宁', '伊川', '偃师', '新华',
            '卫东',
            '石龙', '湛河', '宝丰', '叶县', '鲁山', '郏县', '舞钢', '汝州', '文峰', '北关', '殷都', '龙安', '安阳', '汤阴', '滑县', '缅因州', '新罕布什尔州',
            '佛蒙特州', '札幌市', '青森市,', '盛冈市', '仙台市', '秋田市', '山形市', '福岛市', '水户市', '宇都宫市', '前桥市', '埼来玉市', '千叶市', '新宿区', '横滨市',
            '新潟市', '富山市', '金泽市']
    date_birth = random.choice(create_assist_date())  # 日期
    email = email
    passwd = passwd
    answer1 = random.choice(name)
    answer2 = random.choice(work)
    answer3 = random.choice(air)
    chrome_options = webdriver.ChromeOptions()
    u_a = 'user-agent=' + random.choice(PC_UAS)
    u_lan = 'accept-language: zh-CN,zh;q=0.9'
    chrome_options.add_argument(u_a)
    # webdriver  被识别出来优化
    chrome_options.add_argument('--incognito')
    # 禁用js
    chrome_options.add_argument('--disable-javascript')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(u_lan)
    chrome_options.add_argument('accept-encoding="gzip, deflate, br"')
    # chrome_options.add_argument('--proxy-server=http://192.168.14.40:3131')
    url = "https://appleid.apple.com/account#!&page=create"
    # driver = webdriver.Chrome(executable_path="C:\\Users\ceshi\Desktop\chrome\Chrome-bin\chromedriver.exe",
    #                           chrome_options=chrome_options)
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome(
        executable_path="C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe",
        chrome_options=chrome_options)
    driver.set_script_timeout(50)

    driver.set_script_timeout(60)
    driver.get(url)
    time.sleep(30)
    # 将窗口调整最大
    driver.maximize_window()
    time.sleep(30)
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
        # mysql_config2 = {"host": "192.168.14.90",
        #                  "port": 3306,
        #                  'user': 'root',
        #                  "passwd": '123456',
        #                  "db": 'apple',
        #                  "charset": "utf8"}
        # conn2 = MySQLdb.connect(**mysql_config2)
        # cursor2 = conn2.cursor()
        time.sleep(5)
        try:
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[1]/div/div/last-name-input/div/idms-textbox'
                                         '/idms-error-wrapper/div/div/input').send_keys(random.choice(last_name))
            time.sleep(2)
            # 姓名
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[2]/div/div/first-name-input/div/id'
                                         'ms-textbox/idms-error-wrapper/div/div/input').send_keys(random.choice(name))
            time.sleep(3)
            # 下拉框选择 国家
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/idms-dropdown/div/idms-er'
                                                'ror-wrapper/div/div/select')).select_by_value('JPN')

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
            time.sleep(2)
            # 问题2
            Select(driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-question/div/div[1]'
                                                '/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('136')

            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-answer/div/idms-'
                                                'textbox/idms-error-wrapper/div/div/input').send_keys(answer2)

            time.sleep(2)
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
            time.sleep(30)
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
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[4]/input').send_keys(code[3])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[5]/input').send_keys(code[4])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[6]/input').send_keys(code[5])
                time.sleep(2.5)
                driver.find_element_by_xpath('/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[3]/idms-toolbar/div/div[1]/div/button[1]').click()
                time.sleep(80)
                driver.implicitly_wait(50)
                driver.set_script_timeout(50)
                driver.set_page_load_timeout(80)
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[3]/idms-toolbar/div/div[1]/div/button[1]').click()
                    time.sleep(10)
                except:
                    pass
                # 完善发货信息
                air_info = airs1()
                airs = air_info.get('air')
                code = air_info.get('code')
                mobile = air_info.get('mobile')
                # 街道地址
                street = ['3625 Mt Holly Hntrsvl Rd Ste 406', '590 Boggs School RD', '500 L St, Ste 400',
                          '590 Boggs School RD',
                          '580 Boggs School RD',
                          '1431 Eagle Drive', '1432 Eagle Drive', '1421 Eagle Drive', '1231 Eagle Drive',
                          '510 L St, Ste 400',
                          '3621 Mt Holly Hntrsvl Rd Ste 406']
                # 单元
                homes = ['Unit 3, Building 2 145', '135#', 'Unit 2, Building 2 145', 'Unit 2, Building 2 145',
                         'Unit 1, Building 5 145', 'Unit 3, Building 2 145',
                         'Unit 3, Building 2 201', '139#', '21#', '456#']
                # 编辑按钮
                driver.implicitly_wait(20)
                try:
                    print('编辑。。。。.')
                    time.sleep(60)
                    driver.set_script_timeout(50)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                               '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    time.sleep(35)
                    driver.set_script_timeout(50)
                    driver.implicitly_wait(35)
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div[3]/div[2]/button").click()

                time.sleep(15)
                # 邮编
                print('============')
                try:
                    driver.set_script_timeout(50)
                    driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/div/idms-textbox/idms-error-wrapper"
                                                 "/div/div/input").send_keys(code)
                except:
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                 '/div/div[2]/div[3]/button').click()
                    time.sleep(6)
                    driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/div/idms-textbox/idms-error-wrapper"
                                                 "/div/div/input").send_keys(
                        random.choice(code))

                # 省
                Select(driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[3]/div/div/div/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value(
                    '大阪府')

                time.sleep(3)
                # 城市
                driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[4]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input").send_keys(airs)
                time.sleep(3)
                # 街道
                driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[5]/div/div/idms-textbox/idms-error-wrapper/div/d"
                                             "iv/input").send_keys(random.choice(street))
                time.sleep(3)

                # 单元
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[6]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(random.choice(homes))
                time.sleep(2)
                # 区号
                driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/"
                                             "div[2]/billing-address/section/idms-address/div/div/div[7]/div/div/div[1]/idms-tex"
                                             "tbox/idms-error-wrapper/div/div/input").send_keys('6')
                # 电话
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[7]/div/div/div[2]/idms-textbox/idms-error-wrapper/div/div/input').send_keys(mobile)
                time.sleep(3)
                # 拷贝
                driver.implicitly_wait(10)
                driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[2]/div/label/span').click()
                time.sleep(10)
                info = driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[7]/div/div/div[2]/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')
                if info:
                    driver.set_script_timeout(60)
                    # 保存
                    print('拷贝成功。。。。。。。')
                    driver.implicitly_wait(137)
                    time.sleep(5)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button[1]').click()
                    time.sleep(90)
                    driver.implicitly_wait(45)
                    print('保存中')
                    driver.set_script_timeout(50)
                else:
                    # 尝试再次拷贝保存
                    time.sleep(5)
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
                    driver.set_script_timeout(50)
                    print('保存后再次编辑查看信息。。。。.')
                    time.sleep(35)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                               '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    driver.implicitly_wait(35)
                    time.sleep(50)
                    try:
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.refresh()  # 刷新页面
                        driver.implicitly_wait(35)
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                     '/div/div[2]/div[3]/button').click()

                time.sleep(13)
                print('*****************')
                driver.implicitly_wait(10)
                # 获取编辑信息：
                # 付款邮编
                email_info1 = driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')

                time.sleep(1)
                # 发货邮编
                email_info2 = driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[1]/shipping-address/div/section/idms-address/div/div/div[3]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute('value')
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
                    print(json_data)
                    print(email,passwd)
                    # try:
                    #     # state  激活状态0 注册编辑信息  1 激活
                    #     cursor2.execute("insert into apple_japan(apple_id,passwd,json_data,state) values(%s,%s,%s,%s)", (str(email), passwd,json_data,0))
                    #     conn2.commit()
                    #     print('ok')
                    # except Exception as e:
                    #     print(e)
                    #     pass
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

        info = [{'email': 'tetatmkspn@outlook.com', 'passwd': 'IEa53cIk'}, {'email': 'deausexyx@outlook.com', 'passwd': '2rL37guT'}, {'email': 'nickeaathx@outlook.com', 'passwd': 'wbG552Bl'}, {'email': 'shuheecrrgl@outlook.com', 'passwd': 'SWq73DUG'}, {'email': 'theteethokngng@outlook.com', 'passwd': 'ouP25vzf'}, {'email': 'thycaikf@outlook.com', 'passwd': '2Am886mR'}, {'email': 'nethitywwpeo@outlook.com', 'passwd': 'CH324Bbo'}, {'email': 'smapsesdeeb@outlook.com', 'passwd': 'SGq838IJ'}, {'email': 'naracrfaib@outlook.com', 'passwd': '7WB25Et3'}, {'email': 'neasmoskikoobx@outlook.com', 'passwd': '2pO30lXr'}, {'email': 'towhoskiiwepn@outlook.com', 'passwd': 'mQa64ShU'}, {'email': 'weyneaukwhd@outlook.com', 'passwd': 'uxW36PMi'}, {'email': 'ceteighwhgr@outlook.com', 'passwd': 'zsE21I8z'}, {'email': 'deseshudjl@outlook.com', 'passwd': 'Otk26K3V'}, {'email': 'dasekneseom@outlook.com', 'passwd': '0rH03ulK'}, {'email': 'lasaevdoom@outlook.com', 'passwd': 'Wou16FIO'}, {'email': 'slesaisi@outlook.com', 'passwd': 'Qe181x1L'}, {'email': 'thalosuuylp@outlook.com', 'passwd': 'H9u87x3g'}, {'email': 'lasetobvxw@outlook.com', 'passwd': '6CC81sLm'}, {'email': 'mcshabeiew@outlook.com', 'passwd': '0k332L9K'}, {'email': 'teaulijxpr@outlook.com', 'passwd': 'A0a10oMT'}, {'email': 'noseendesfaioo@outlook.com', 'passwd': '46O23DjD'}, {'email': 'peausoushdrx@outlook.com', 'passwd': 'aWy52k4x'}, {'email': 'smoatanilp@outlook.com', 'passwd': 'Hxx67uvu'}, {'email': 'seshelhtbif@outlook.com', 'passwd': '0Oy65qhQ'}, {'email': 'feshebmeut@outlook.com', 'passwd': 'ONk47fBu'}, {'email': 'shesayrgjck@outlook.com', 'passwd': '1UN58Vkb'}, {'email': 'lathictbel@outlook.com', 'passwd': 'jhK55WTA'}, {'email': 'mcsothedihw@outlook.com', 'passwd': 'Oo445pMa'}, {'email': 'smecithgufmw@outlook.com', 'passwd': '28e34Mdw'}, {'email': 'tutheasonmvomht@outlook.com', 'passwd': 'jp443weD'}, {'email': 'tisaraslbryoi@outlook.com', 'passwd': '6Vo84POb'}, {'email': 'syteygnbhei@outlook.com', 'passwd': '1S767wYt'}, {'email': 'sheneyifqfb@hotmail.com', 'passwd': 'zfL14Y8L'}, {'email': 'voagesoneupea@hotmail.com', 'passwd': 'P5q25iGj'}, {'email': 'shoonithqjof@hotmail.com', 'passwd': 'fg841uuP'}, {'email': 'sheaslokrxql@hotmail.com', 'passwd': 'ibU56X6W'}, {'email': 'tesitohf@hotmail.com', 'passwd': 'zeH45Hyd'}, {'email': 'dahisleylbaaji@hotmail.com', 'passwd': 'Fqe37KA1'}, {'email': 'thaytulkqyga@hotmail.com', 'passwd': 'PX285aIu'}, {'email': 'mcritejklia@hotmail.com', 'passwd': 'ywc18zT8'}, {'email': 'teaselqsixwf@hotmail.com', 'passwd': 'S6B462rx'}, {'email': 'misethaefajnp@hotmail.com', 'passwd': 'Qni16GIT'}, {'email': 'thesatysunrcb@hotmail.com', 'passwd': 'MUc77Umg'}, {'email': 'tenyhoughjov@hotmail.com', 'passwd': 'Wl975vXO'}, {'email': 'slasoohrbak@hotmail.com', 'passwd': 'daB4075w'}, {'email': 'thousatqxqlf@hotmail.com', 'passwd': 'u4O23hol'}, {'email': 'sesheewwdii@hotmail.com', 'passwd': 'icH30Jjm'}, {'email': 'seytoughthongdl@hotmail.com', 'passwd': 'VqH52fmh'}, {'email': 'shosoughvcelws@hotmail.com', 'passwd': 'kJO57Hhn'}, {'email': 'sloalouyesl@hotmail.com', 'passwd': 'AP981PiU'}, {'email': 'shenaydcng@hotmail.com', 'passwd': 'Mrp766Xm'}]

        for i in info:
            email = i.get('email')
            passwd = i.get('passwd')
            try:
                start_time = int(time.time())
                register(email, passwd)
                restart_process()
                print('注册需要时间%s' % (int(time.time() - start_time)))
            except Exception as e:
                print(e)
                pass
            time.sleep(500)

