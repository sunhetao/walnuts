import os

from .config_manager import PROJECT_DIR
from .utils import send_email, gen_junit_report


def run_test():
    os.system('pytest %s --junitxml=report.xml --html=report.html' % PROJECT_DIR)
    email_content = gen_junit_report(os.path.join(PROJECT_DIR, 'report.xml'))
    send_email('smtp.126.com', 'hgbac@126.com', 'hgbac123abc', ['hgbac@qq.com', 'hgbac@163.com'], '测试报告', email_content,
               os.path.join(PROJECT_DIR, 'report.html'))
