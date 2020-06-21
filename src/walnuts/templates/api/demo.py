from walnuts import request_mapping, Method, Requester


@request_mapping(path='{app.host}')
class Demo:

    @request_mapping(path='/login', method=Method.POST)
    def login(self, email, password):
        """
        登录接口
        """
        data = {
            'email': email,
            'password': password
        }
        return Requester(data=data)

    @request_mapping(path='/book/list')
    def get_book_list(self):
        return Requester()
