from walnuts import RequestMapping, Method, Requester


@RequestMapping(path='{app.host}')
class Demo:

    @RequestMapping(path='/login', method=Method.POST)
    def login(self, account, password):
        """
        登录接口
        """
        data = {
            'account': account,
            'password': password
        }
        return Requester(data=data)

    @RequestMapping(path='/book/list')
    def get_book_list(self):
        return Requester()
