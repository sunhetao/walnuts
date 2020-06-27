from .report import Report


def run_test():
    report = Report()
    report.execute_test().send_email().send_ding_talk_report()
