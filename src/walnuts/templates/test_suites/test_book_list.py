from walnuts import v
from api.demo import Demo
from common.assert_tools import if_list_equal


class TestBookList:

    def setup(self):
        account = v['user.account']
        password = v['user.password']
        self.app = Demo()
        self.app.login(account, password)

    def test_get_book_list(self):
        res = self.app.get_book_list()._json()
        assert if_list_equal(['python', 'java', 'javascript', 'go'], res['data'])
