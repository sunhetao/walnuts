import os
import smtplib
import time

from click import echo, style

from .config_manager import v
from .report import send_email, gen_junit_report


class ReportConfig:

    def __init__(self):
        self.server = None
        self.email = None
        self.password = None
        self.to_list = None
        # self.subject = None
        self.debug_level = None
        self.report_folder = None

    def set_config(self):
        self.server = v['report.email.server']
        self.email = v['report.email.email']
        self.password = v['report.email.password']
        self.to_list = v['report.email.to_list']
        self.debug_level = v['report.email.debug_level'] or 0
        self.report_folder = v['report.report_folder'] or ''

        if not self.server and self.email:
            self.server = 'smtp.' + self.email.split('@')[-1]

    def need_send_report(self):
        return self.server and self.email and self.password and self.to_list


def execute_test(project_dir, junit_report_path, html_report_path):
    os.system('py.test "{project_dir}" -o junit_family=xunit2 '
              '--junitxml="{junit_report_path}" '
              '--html="{html_report_path}"  '
              '--self-contained-html'.format(project_dir=project_dir,
                                             junit_report_path=junit_report_path,
                                             html_report_path=html_report_path))


def run_test():
    # 获取项目信息
    project_dir = v.project_dir
    project_name = os.path.basename(project_dir)

    # 获取配置
    report_config = ReportConfig()
    report_config.set_config()

    # 设置junit报告和html报告名字
    random_report_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    junit_xml_report_path = os.path.join(project_dir, report_config.report_folder,
                                         'junit_report-%s.xml' % random_report_name)
    html_report_path = os.path.join(project_dir, report_config.report_folder,
                                    'html_report-%s.html' % random_report_name)

    # 执行测试
    execute_test(project_dir, junit_xml_report_path, html_report_path)

    # 判断是否发送邮件
    if not report_config.need_send_report():
        echo(style('不发送邮件，没有找到邮件配置或配置有错误', fg='red'))
        return

    # 发送邮件
    subject = '{project_name} test report {random_report_name}'.format(project_name=project_name,
                                                                       random_report_name=random_report_name)
    email_content = gen_junit_report(junit_xml_report_path)
    try:
        send_email(report_config.server,
                   report_config.email,
                   report_config.password,
                   report_config.to_list,
                   subject,
                   email_content,
                   html_report_path,
                   report_config.debug_level)
    except smtplib.SMTPAuthenticationError:
        echo(style('发送邮件失败，账户名或密码失败，请检查后重试', fg='red'))
        return

    echo(style('邮件发送成功，请查收', fg='green'))
