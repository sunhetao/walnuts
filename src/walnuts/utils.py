import json
import os
import smtplib
import traceback
from collections import UserDict
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial

from configobj import ConfigObj
from jinja2 import Template
from lxml import etree
from yaml import load, dump
from yaml import Loader, Dumper


def format_json(content):
    if isinstance(content, (str, bytes)):
        try:
            content = json.loads(content)
        finally:
            return content

    result = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')). \
        encode('latin-1').decode('unicode_escape')

    return result


def get_root_dir_and_env(flag_file_name, cur_dir):
    if os.path.isfile(cur_dir):
        cur_dir = os.path.dirname(cur_dir)
    if flag_file_name in os.listdir(cur_dir):
        with open(os.path.join(cur_dir, flag_file_name)) as f:
            return cur_dir, f.read().strip()

    up_dir = os.path.dirname(cur_dir)
    if up_dir == cur_dir:
        return None, None
    return get_root_dir_and_env(flag_file_name, up_dir)


class WDict(UserDict):
    """
    It's hard to name！！！
    注意：正常使用key中不能再出现 "."，否则会被拆分掉，如a['a.b.c']等于a['a']['b']['c']
    示例：> d = {'a': {'b': 'c': 1}}
         > print(WDict(**d)['a.b.c']) # -> 1
    """

    def __getitem__(self, item: str):
        key_list = item.split('.')
        content = self.data
        for key in key_list:
            key = int(key) if str.isdigit(key) else key
            try:
                content = content[key]
            except (KeyError, IndexError):
                return None
        return content


class DDict:
    """
    It's hard to name！！！
    示例: > d = {'a': {'b': 'c': 1}}
         > print(d.a.b.c) # 1
    """

    def __init__(self, d):
        self.__d = d

    def __getattr__(self, item):
        try:
            return DDict(self.__d[item])
        except TypeError:
            raise ValueError('找不到%s配置，请检查' % item)

    def __str__(self):
        return str(self.__d)


class ConfigFileParser:
    def __init__(self, suffix, file_path):
        if not isinstance(file_path, str):
            raise ValueError('file_path error, is not a valid str')

        if not os.path.isfile(file_path):
            raise ValueError('file_path error, is not a valid file path')

        self.file_path = file_path
        self.content = None
        self.parser = self.get_parser(suffix)

        try:
            with open(self.file_path, encoding='utf-8') as f:
                self.content = self.parser(f) or {}
        except Exception:
            traceback.print_exc()
            raise ValueError('%s is not a valid %s file' % (file_path, suffix))

    @staticmethod
    def get_parser(suffix):
        if suffix == 'yaml':
            return partial(load, Loader=Loader)
        elif suffix == 'json':
            return json.load
        elif suffix == 'ini':
            return ConfigObj
        else:
            raise ValueError('不支持的配置文件类型')

    def as_dict(self):
        return self.content


def send_email(server, email, password, to_list, subject, content, attach_path):
    """
    发送邮件
    :param server:邮件服务器
    :param email: 发送者邮件地址
    :param password: 邮箱密码
    :param to_list: 发送地址列表
    :param subject: 主题
    :param content: 发送邮件内容
    :param attach_path: 发送邮件附件
    """
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = ','.join(to_list)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    if attach_path:
        with open(attach_path, 'rb') as f:
            file_name = os.path.basename(attach_path)
            mime = MIMEBase('html', 'html', filename=file_name)
            mime.add_header('Content-Disposition', 'attachment', filename=file_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)

    server = smtplib.SMTP(server, 25)
    server.set_debuglevel(1)
    server.login(email, password)
    server.sendmail(email, to_list, msg.as_string())
    server.quit()


def parse_test_result_xml(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    test_suite = root[0]
    test_cases_pack_map = {}

    for test_case in test_suite:
        success, failed, skipped = 0, 0, 0
        package = test_case.get('classname')
        if len(test_case) > 0:
            tag = test_case[0].tag
            if tag == 'skipped':
                skipped += 1
            else:
                failed += 1
        else:
            success = 1

        if package not in test_cases_pack_map:
            test_cases_pack_map[package] = {
                'success': 0,
                'failed': 0,
                'skipped': 0,
                'test_cases': []
            }
        test_cases_pack_map[package]['success'] += success
        test_cases_pack_map[package]['failed'] += failed
        test_cases_pack_map[package]['skipped'] += skipped
        test_cases_pack_map[package]['test_cases'].append({
            'success': success,
            'failed': failed,
            'skipped': skipped,
            'package': package,
            'file': test_case.get('file'),
            'line': test_case.get('line'),
            'name': test_case.get('name'),
            'case': '.'.join((test_case.get('classname'), test_case.get('name'))),
            'time': test_case.get('time'),
        })

    return {
        'test_packages': test_cases_pack_map
    }


def gen_junit_report(junit_xml_path):
    email_report_template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_report_template.html')
    test_result = parse_test_result_xml(junit_xml_path)
    with open(email_report_template_path) as f:
        content = Template(f.read()).render(**test_result)
    return content
