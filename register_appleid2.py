# -*- coding: utf-8 -*-
import datetime
import json
import poplib
import random
import re
import time

import MySQLdb
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# from auto_register.ydm import use_ydm
# from testdir.zhptest.kill_z import restart_process
# from testdir.zhptest.mv_dir import mv_dir


def get_userinfo():
    mysql_config2 = {"host": "192.168.14.90",
                     "port": 3306,
                     'user': 'root',
                     "passwd": '123456',
                     "db": 'apple',
                     "charset": "utf8"}
    conn2 = MySQLdb.connect(**mysql_config2)
    cursor2 = conn2.cursor()
    cursor2.execute("select `email` , password from email order by id desc")
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
    server = imaplib.IMAP4_SSL("outlook.office365.com", 993)
    server.login(email_address, password)
    # 邮箱中的文件夹，默认为'INBOX'
    try:
        inbox = server.select("INBOX")
        typ, data = server.search(None, "ALL")
        msgList = data[0].split()
        latest = msgList[len(msgList) - 1]
        typ, datas = server.fetch(latest, '(RFC822)')
        # 使用utf-8解码
        msg_content = (b''.join(datas[0]).decode('utf-8')[2600:3200]).replace('\r\n', '')
        code = re.findall("x-ds-vetting-token: (.*?)X-DKIM_SIGN_REQUIRED", msg_content)[0]
        server.close()
        return code
    except Exception as e:
        print(e)
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


# 生成城市 邮编信息
def airs1():
    # al 对应的城市
    air = [
        {
            'air': 'Montgomery',
            'code': random.choice(['36101', '36125', '36130', '36135', '36140', '36142', '36177']),
            'mobile': random.choice(['(303) 699-6894', '330-574-0257', '7193807582', '330-574-0157', '330-574-0207',
                                     '330-524-0257', '(303) 699-6294', '7193807282'])
        },
        {
            'air': 'Huntsville',
            'code': random.choice(['35801', '35816', '35824', '35893', '35899']),
            'mobile': random.choice(['(303) 699-6894', '330-574-0257', '7193807582', '330-574-0157', '330-574-0207',
                                     '330-524-0257', '(303) 699-6294', '7193807282'])
        },
        {
            'air': 'Mobile',
            'code': random.choice(['36640', '36641', '36644', '36652', '36660', '36663', '36670', '36671', '36675']),
            'mobile': random.choice(['(303) 699-6894', '330-574-0257', '7193807582', '330-574-0157', '330-574-0207',
                                     '330-524-0257', '(303) 699-6294', '7193807282'])
        },
        {
            'air': 'Tuscaloosa',
            'code': random.choice(['35403', '35486', '35487']),
            'mobile': random.choice(['(303) 699-6894', '330-574-0257', '7193807582', '330-574-0157', '330-574-0207',
                                     '330-524-0257', '(303) 699-6294', '7193807282'])
        },
        {
            'air': 'Birmingham',
            'code': random.choice(
                ['35238', '35242', '35246', '35249', '35253', '35255', '35259', '35261', '35266']),
            'mobile': random.choice(['(303) 699-6894', '330-574-0257', '7193807582', '330-574-0157', '330-574-0207',
                                     '330-524-0257', '(303) 699-6294', '7193807282'])
        },
    ]
    info = random.choice(air)
    return info


PC_UAS = [
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


# 注册苹果id
def register(email, passwd):
    last_name = ['Allison', 'acob', 'dfa', 'Michael', 'make', 'Ethan', 'nisang', 'Joshua', 'Qinshuy', 'Alexander',
                 'Ylsd',
                 'Anthony', 'andongni', 'William', 'Christopher', 'Jayden', 'jiedun', 'Andrew', 'ande', 'Smith',
                 'Yhans', 'Johnson', 'wlsia', 'Williams', 'bulang', 'Brown', 'qis', 'Jones', 'mile', 'Miller', 'dawisi',
                 'Davis', 'jiaxi', 'Garcia', 'Rodriguez',
                 'Wilson']
    name = ['Sophia', 'Emma', 'Aiden', 'Jacob', 'Ethan', 'Matthew', 'Nicholas', 'Jack', 'Joshua', ' Michael', 'Ryan',
            'Andrew',
            'Caden', 'Tyler', 'Dylan', 'Jaden', 'Logan', 'Caleb', 'Lucas', 'Joseph', 'Daniel', 'Christopher', 'Gavin',
            'Austin', 'Evan', 'Cameron', 'Luke', 'Christian', 'John', 'Samuel', 'Hunter', 'Elijah', 'Thomas', 'Emily',
            'Hailey', 'Abigail',
            'Lauren', 'Makenzie', 'Anna', 'Natalie', 'Katherine', 'Morgan', 'Julia', 'Jordan', ' Allison', 'Morgan',
            'Zoe', 'Rachel', 'Katherine', 'Isabel', 'Kyra',
            'Allison', 'Allison', 'acob', 'yagebu', 'Michael', 'makeer', 'Ethan', 'nisang', 'Joshua', 'qishuya',
            'Alexander', 'yelis',
            'Anthony', 'andongni', 'William', 'weila', 'Christopher', 'mair', 'Jayden', 'lis', 'Andrew']  # 名字
    work = ['作业员', '技术员', '工程师', '设计师', '管理员', '总务人员', '服务', '厨师', '服务员', '营销人员', '保安', '司机', '导游', '售票员', '调酒师', '营业员',
            '促销', '保姆', '健康', '医生', '护士', '药剂师', '营养师', '后勤', '健身教练', '按摩技师', '娱乐类', '演员', '导演', '制片', '经纪', '编剧', '场务',
            '音乐人']
    air = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delware', 'Florida',
           'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', '龙亭', '顺河回族', '鼓楼', '禹王台', '金明', '杞县', '通许', '尉氏', '开封',
           '兰考', '老城', '西工', '瀍河回族', '涧西', '吉利', '洛龙', '孟津', '新安', '栾川', '嵩县', '汝阳', '宜阳', '洛宁', '伊川', '偃师', '新华', '卫东',
           '石龙', '湛河', '宝丰', '叶县', '鲁山', '郏县', '舞钢', '汝州', '文峰', '北关', '殷都', '龙安', '安阳', '汤阴', '滑县', '缅因州', '新罕布什尔州',
           '佛蒙特州', '罗德岛州', '康涅狄格州', '马萨诸塞州', '纽黑文', '普罗维登斯', '曼彻斯特', '奥古斯丁', '纽约州', '宾夕法尼亚州', '新泽西州', '特拉华州', '马里兰州',
           '弗吉尼亚州', '西弗吉尼亚州费城', '纽约城', '匹兹堡', '里士满', '巴尔地摩', '华盛顿特区', '查尔斯顿', '布法罗', '弗吉尼亚比奇\n    ', '北卡罗来纳州', '南卡罗来纳州',
           '佐治亚州', '佛罗里达州', '密歇根州', '俄亥俄州', '印第安纳州', '伊利诺伊州', '肯塔基州', '田纳西州', '亚拉巴马州', '密西西比州', '阿肯色州', '路易斯安那州']
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
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(u_lan)
    # 启用无痕模式
    chrome_options.add_argument('--incognito')
    # 禁用js
    chrome_options.add_argument('--disable-javascript')
    chrome_options.add_argument('accept-encoding="gzip, deflate, br"')
    # chrome_options.add_argument('--proxy-server=http://192.168.14.40:3128')
    url = "https://appleid.apple.com/account#!&page=create"
    # driver = webdriver.Chrome(executable_path="D:\\Documents\Downloads\Chrome-bin\chromedriver.exe", chrome_options=chrome_options)
    driver = webdriver.Chrome(
        executable_path="C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe",
        chrome_options=chrome_options)
    # 获取网页cookie
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    try:
        driver.get(url)
        time.sleep(20)
    except:
        driver.refresh()  # 刷新页面
        time.sleep(30)
    # 将窗口调整最大
    # driver.maximize_window()
    time.sleep(30)
    # 验证码截图
    try:
        driver.find_element_by_xpath(
            '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[1]/div/idms-captcha/'
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
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[1]/div/div/last-name-input/div/idms-textbox'
                '/idms-error-wrapper/div/div/input').send_keys(random.choice(last_name))
            time.sleep(2)
            # 姓名
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/full-name/div[2]/div/div/first-name-input/div/id'
                'ms-textbox/idms-error-wrapper/div/div/input').send_keys(random.choice(name))
            time.sleep(2)
            # 下拉框选择 国家
            Select(driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/idms-dropdown/div/idms-er'
                'ror-wrapper/div/div/select')).select_by_value('USA')

            time.sleep(1.5)
            # 日期
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[2]/div/div[3]/div/wc-birthday/div/div/d'
                'iv/div/masked-date/idms-error-wrapper/div/div/input').send_keys(date_birth)
            time.sleep(1.5)

            # 邮箱
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[1]/div/account-name/div/div/email-input/div/idms-textbox/idms-error-wrapper/div/'
                'div/input').send_keys(email)

            time.sleep(1.5)
            # 密码
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/new-password/div/div/password-input/d'
                'iv/input').send_keys(passwd)

            time.sleep(1.5)
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[3]/div/div[2]/div/confirm-password/div/div/confirm-password-input/div/idms-textbox/idms'
                '-error-wrapper/div/div/input').send_keys(passwd)

            time.sleep(1.5)
            # 问题1
            Select(driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[1]/security-question/div/div[1]/idms-dropdown/div/idms-error'
                '-wrapper/div/div/select')).select_by_value('130')
            time.sleep(2)
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[1]/security-answer/div/idms-textbox/idms-error-wrapper/div/div/input') \
                .send_keys(answer1)
            time.sleep(2)
            # 问题2
            Select(driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-question/div/div[1]'
                '/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('136')

            time.sleep(2)
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[2]/security-answer/div/idms-'
                'textbox/idms-error-wrapper/div/div/input').send_keys(answer2)

            time.sleep(2)
            # 问题3
            Select(driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[3]/security-questi'
                'on/div/div[1]/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value('142')
            time.sleep(1.5)
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[4]/div/div/div/security-questions-answers/div/div[3]/security-answer/div/idms-textbox/'
                'idms-error-wrapper/div/div/input').send_keys(answer3)

            time.sleep(2)
            # 图片识别
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[7]/div/create-captcha/div/div/div/div/div[2]/div/div[1]/captcha-input/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
                    ym_info)
            except:
                driver.find_element_by_xpath(
                    '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/div/div[2]/div/div/div[6]/div/create-captcha/div/div/div/div/div[2]/div/div[1]/captcha-input/div/idms-textbox/idms-error-wrapper/div/div/'

                    'input').send_keys(ym_info)
            time.sleep(3)
            driver.find_element_by_xpath(
                '/html/body/div[2]/aid-web/div[2]/div[2]/div/create-app/aid-create/idms-flow/div/div/div/idms-step/div/div/'

                'div/div[3]/idms-toolbar/div/div/div/button').click()
            time.sleep(25)
            # 读取邮箱信息 填写验证码
            try:
                code = recv_email_by_pop3(email, passwd)
            except:
                code = recv_email_by_pop3(email, passwd)
            else:
                code = code
            print('code:', code)
            if code:
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[1]/input').send_keys(
                    code[0])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[2]/input').send_keys(
                    code[1])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[3]/input').send_keys(
                    code[2])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[4]/input').send_keys(
                    code[3])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[5]/input').send_keys(
                    code[4])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[2]/div/div/div[2]/security-code/div/idms-error-wrapper/div/div/div/div[6]/input').send_keys(
                    code[5])
                time.sleep(1.5)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div/div[1]/step-verify-code/idms-step/div/div/div/div[3]/idms-toolbar/div/div[1]/div/button[1]').click()
                time.sleep(50)
                driver.implicitly_wait(50)
                # 完善发货信息
                air_info = airs1()
                airs = air_info.get('air')
                code = air_info.get('code')
                mobile = air_info.get('mobile')
                # 街道地址
                jiedao = ['3625 Mt Holly Hntrsvl Rd Ste 406', '590 Boggs School RD', '500 L St, Ste 400',
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
                driver.implicitly_wait(40)
                try:
                    print('编辑。。。。.')
                    time.sleep(50)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                 '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    time.sleep(35)
                    driver.implicitly_wait(35)
                    try:
                        driver.find_element_by_xpath(
                            '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.find_element_by_xpath(
                            "/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div[3]/div[2]/button").click()

                time.sleep(15)
                # 街道地址
                print('#######################')
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/idms-textbox/idms-error-wrapper/div/div/i'
                        'nput').send_keys(random.choice(jiedao))
                except:
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                 '/div/div[2]/div[3]/button').click()
                    time.sleep(6)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[2]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
                        random.choice(jiedao))

                time.sleep(3)
                # 单元
                driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[3]/div/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
                    random.choice(homes))
                time.sleep(2)
                # 城市
                driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[4]/div/div/div/idms-textbox/idms-e'
                    'rror-wrapper/div/div/input').send_keys(airs)
                time.sleep(2)
                # 州  AL
                Select(driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[5]/div/div/div/idms-dropdown/div/idms-error-wrapper/div/div/select')).select_by_value(
                    'AL')
                time.sleep(2)
                # 邮编
                driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[6]/div/div/div/idms-textbox/idms-error'
                    '-wrapper/div/div/input').send_keys(code)
                time.sleep(2)
                # 电话
                driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[7]/div/idms-textbox/idms-error-wrapper/div/div/input').send_keys(
                    mobile)
                time.sleep(3)
                # 拷贝
                driver.implicitly_wait(10)
                driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[2]/div/label/span').click()
                time.sleep(10)
                info = driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[1]/shipping-address/div/section/idms-address/div/div/div[7]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute(
                    'value')
                if info:
                    # 保存
                    print('拷贝成功。。。。。。。')
                    driver.implicitly_wait(17)
                    time.sleep(5)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button[1]').click()
                else:
                    # 尝试再次拷贝保存
                    time.sleep(5)
                    driver.implicitly_wait(10)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[2]/div/label/span').click()
                    driver.implicitly_wait(17)
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button[1]').click()
                driver.implicitly_wait(15)
                time.sleep(9)
                # 查看是否保存成功
                # 编辑
                try:
                    print('保存后再次编辑查看信息。。。。.')
                    time.sleep(30)
                    driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                 '/div/div[2]/div[3]/button').click()
                except Exception as e:
                    print(e)
                    print('--------')
                    driver.refresh()  # 刷新页面
                    driver.implicitly_wait(35)
                    time.sleep(30)
                    try:
                        driver.find_element_by_xpath(
                            '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[3]/button').click()
                    except:
                        driver.find_element_by_xpath('/html/body/div[1]/manage/div/div/aid-payment/section[2]'
                                                     '/div/div[2]/div[3]/button').click()
                        # driver.find_element_by_xpath("/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div[3]/div[2]/button").click()

                time.sleep(3)
                print('*****************')
                driver.implicitly_wait(10)
                # 获取编辑信息：
                # 付款邮编
                email_info1 = driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[1]/div[1]/payment-method-edit/div/div[2]/billing-address/section/idms-address/div/div/div[6]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute(
                    'value')

                time.sleep(1)
                # 发货邮编
                email_info2 = driver.find_element_by_xpath(
                    '/html/body/div[1]/manage/div/div/aid-payment/section[2]/div/div[2]/div[2]/accordion/div/div/div[1]/div/div[2]/div[3]/div/div[1]/shipping-address/div/section/idms-address/div/div/div[7]/div/div/div/idms-textbox/idms-error-wrapper/div/div/input').get_attribute(
                    'value')
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
                    print(json_data)
                    print(email)
                    print(passwd)
                    json_data = json.dumps(json_data)
                    # try:
                    #     # state  激活状态0 注册编辑信息  1 激活
                    #     cursor2.execute("insert into apple(apple_id,passwd,json_data,state) values(%s,%s,%s,%s)",
                    #                     (str(email), passwd, json_data, 0))
                    #     conn2.commit()
                    #     print('ok')
                    # except Exception as e:
                    #     print(e)
                    #     pass
                    time.sleep(3)
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
        '''
        ipsethrugy@outlook.com----nUi44eTz
neaustorya@outlook.com----3l004OIG
mclefegqsq@outlook.com----SaA0394z
        '''
        # NikaiGilanalH@aol.com----gT2xf772m----iixlcvbcmifgjpiy

        info = [

                {'email': 'tishergjabp@hotmail.com', 'passwd': '0Ea30MFk'},
                {'email': 'tasulrmna@hotmail.com', 'passwd': 'XvB125GN'},
                {'email': 'thoosmettkvq@hotmail.com', 'passwd': 'X1r28sjK'},
                {'email': 'thypoughcarvi@hotmail.com', 'passwd': '1PB61gwj'}

                ]

        for i in info:
            email = i.get('email')
            passwd = i.get('passwd')
            try:
                start_time = int(time.time())
                register(email, passwd)
                # restart_process()
                print('注册需要时间%s' % (int(time.time() - start_time)))
            except Exception as e:
                print(e)
                pass
            time.sleep(200)
