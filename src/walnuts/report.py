import os
import smtplib
import xml.etree.ElementTree as ET
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template


def send_email(server, email, password, to_list, subject, content, attach_path, debug_level=0):
    """
    发送邮件
    :param server:邮件服务器
    :param email: 发送者邮件地址
    :param password: 邮箱密码
    :param to_list: 发送地址列表
    :param subject: 主题
    :param content: 发送邮件内容
    :param attach_path: 发送邮件附件
    :param debug_level: 发送邮件debug级别,默认为0
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
    server.set_debuglevel(debug_level)
    server.login(email, password)
    server.sendmail(email, to_list, msg.as_string())
    server.quit()


def parse_test_result_xml(file_path):
    tree = ET.parse(file_path)
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
