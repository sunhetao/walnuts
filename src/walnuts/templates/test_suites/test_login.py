from walnuts import v
from api.demo import Demo


class TestLogin:
    def test_login_success(self):
        """
        测试登录成功场景
        """
        email = v['user.email']
        password = v['user.password']
        app = Demo()
        res = app.login(email, password).json()
        assert res['code'] == 10000
        assert res['msg'] == 'login success'

    def test_login_with_error_password(self):
        """
        测试使用错误的密码登录
        """
        email = v['user.email']
        password = '123456'
        app = Demo()
        res = app.login(email, password).json()
        assert res['code'] == 20000
        assert res['msg'] == 'login fail, password error'
