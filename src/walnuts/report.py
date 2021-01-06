import os
import smtplib
import time
import xml.etree.ElementTree as ET
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from click import echo, style
from jinja2 import Template
import requests

from .exceptions import SendDingTalkFailException
from .config_manager import v, EmailReportConfig, DingTalkReportConfig


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

    server = smtplib.SMTP_SSL(server, 465)
    server.set_debuglevel(debug_level)
    server.login(email, password)
    server.sendmail(email, to_list, msg.as_string())
    server.quit()


def send_ding_talk_msg(hook_url, project_name, test_result):
    """
    发送钉钉消息
    :param project_name: 项目名称
    :param hook_url: 回调地址
    :param test_result: 测试结果
    """
    pass_pic_url = "https://s1.ax1x.com/2020/06/25/NwjUG6.png"
    fail_pic_url = "https://s1.ax1x.com/2020/06/27/NyoprQ.png"

    msg = {
        "msgtype": "link",
        "link": {
            "title": "%s TEST %s" % (project_name.upper(), test_result['test_result']),
            "text": "总用例数：%s\n"
                    "失败用例：%s\n"
                    "运行耗时：%ss" % (test_result['total_case_num'],
                                  test_result['total_failed_case_num'] + test_result['total_error_case_num'],
                                  test_result['run_duration_time']),
            "picUrl": pass_pic_url if test_result['test_result'] == 'SUCCESS' else fail_pic_url,
            "messageUrl": "http://"
        }
    }
    res = requests.post(hook_url, json=msg).json()
    if res['errcode'] > 0:
        raise SendDingTalkFailException('发送钉钉消息失败，失败原因：%s' % res['errmsg'])


def parse_test_result_xml(file_path):
    """
    解析junit xml文件
    :param file_path: junit xml文件路径
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    test_suite = root[0]

    # 按包分类测试运行结果
    test_cases_module_result = {}

    # 运行用例总数
    total_case_num = test_suite.get('tests')

    # 运行失败总数
    total_failed_case_num = test_suite.get('failures')

    # 运行错误总数
    total_error_case_num = test_suite.get('errors')

    # 运行跳过的总数
    total_skipped_case_num = test_suite.get('skipped')

    # 运行日期
    run_date = test_suite.get('timestamp').replace('T', ' ')

    # 运行耗时，单位是秒
    run_duration_time = test_suite.get('time')

    # 测试结果
    test_result = 'SUCCESS'

    for test_case in test_suite:
        success, failed, error, skipped = 0, 0, 0, 0
        module_name = test_case.get('classname')

        # 判断test case是否有子节点，如有，判断是跳过还是失败，然后计算相应数量
        if len(test_case) > 0:
            tag = test_case[0].tag
            if tag == 'skipped':
                skipped += 1
            elif tag == 'failure':
                test_result = 'FAILURE'
                failed += 1
            elif tag == 'error':
                test_result = 'FAILURE'
                error += 1
        else:
            success = 1

        # 如果模块名不在结果集里则初始化
        if module_name not in test_cases_module_result:
            test_cases_module_result[module_name] = {
                'success': 0,
                'failed': 0,
                'error': 0,
                'skipped': 0,
                'test_cases': []
            }
        test_cases_module_result[module_name]['success'] += success
        test_cases_module_result[module_name]['failed'] += failed
        test_cases_module_result[module_name]['error'] += error
        test_cases_module_result[module_name]['skipped'] += skipped
        test_cases_module_result[module_name]['test_cases'].append({
            'success': success,
            'failed': failed,
            'error': error,
            'skipped': skipped,
            'package': module_name,
            'case': '.'.join((test_case.get('classname'), test_case.get('name'))),
            'time': test_case.get('time'),
        })

    return {
        'test_result': test_result,
        'total_case_num': int(total_case_num),
        'total_failed_case_num': int(total_failed_case_num),
        'total_error_case_num': int(total_error_case_num),
        'total_skipped_case_num': int(total_skipped_case_num),
        'run_date': run_date,
        'run_duration_time': run_duration_time,
        'test_modules': test_cases_module_result
    }


def gen_email_report(project_name, test_result):
    """
    通过解析junit xml报告得到的测试结果，渲染报告模板，然后输出字符串
    """
    email_report_template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_report_template.html')
    with open(email_report_template_path, encoding='utf-8') as f:
        content = Template(f.read()).render(project_name=project_name, **test_result)
    return content


class Report:
    def __init__(self):
        # 获取项目信息
        self.project_dir = v.project_dir
        self.project_name = os.path.basename(self.project_dir)
        self.report_folder = v['report.report_folder'] or ''

        # 设置junit报告和html报告名字
        self.random_report_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.junit_xml_report_path = os.path.join(self.project_dir, self.report_folder,
                                                  'junit_report-%s.xml' % self.random_report_name)
        self.html_report_path = os.path.join(self.project_dir, self.report_folder,
                                             'html_report-%s.html' % self.random_report_name)

        self.test_result = None

    def execute_test(self):
        os.system('py.test "{project_dir}" -o junit_family=xunit2 '
                  '--junitxml="{junit_report_path}" '
                  '--html="{html_report_path}"  '
                  '--self-contained-html'.format(project_dir=self.project_dir,
                                                 junit_report_path=self.junit_xml_report_path,
                                                 html_report_path=self.html_report_path))

        self.test_result = parse_test_result_xml(self.junit_xml_report_path)
        return self

    def send_email(self):
        # 获取配置
        report_config = EmailReportConfig()
        report_config.set_config()

        # 判断是否发送邮件
        if not report_config.need_send_report(self.test_result['test_result']):
            echo(style('不发送邮件，配置不触发或配置有错误', fg='red'))
            return self

        # 发送邮件
        subject = '{project_name} test report {random_report_name}'.format(project_name=self.project_name,
                                                                           random_report_name=self.random_report_name)
        email_content = gen_email_report(self.project_name, self.test_result)
        try:
            send_email(report_config.server,
                       report_config.email,
                       report_config.password,
                       report_config.to_list,
                       subject,
                       email_content,
                       self.html_report_path,
                       report_config.debug_level)
        except smtplib.SMTPAuthenticationError:
            echo(style('发送邮件失败，账户名或密码失败，请检查后重试', fg='red'))
            return self

        echo(style('邮件发送成功，请查收', fg='green'))
        return self

    def send_ding_talk_report(self):
        # 获取配置
        report_config = DingTalkReportConfig()
        report_config.set_config()

        # 判断是否发送钉钉报告
        if not report_config.need_send_report(self.test_result['test_result']):
            echo(style('不发送钉钉报告，配置不触发或没有找到钉钉配置', fg='red'))
            return self
        try:
            send_ding_talk_msg(report_config.hook_url, self.project_name, self.test_result)
        except SendDingTalkFailException as e:
            echo(style('发送钉钉消息失败，[%s]，请检查后重试' % e, fg='red'))
            return self

        echo(style('钉钉消息发送成功，请查收', fg='green'))
        return self
