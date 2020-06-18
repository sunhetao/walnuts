from walnuts import group, request_mapping, add_header, add_headers, Method, Requester


@group(path='http://httpbin.org')
class HTTPBin:

    @request_mapping('/post', method=Method.POST)
    def post_form(self):
        """
        form请求示例
        """
        return Requester(data={'a': 1, 'b': 2})

    @request_mapping('/post', method=Method.POST)
    def post_json(self):
        """
        json请求示例
        """
        return Requester(json={'a': 1, 'b': 2})

    @request_mapping('/post', method=Method.POST)
    def with_header(self):
        """
        带headers示例
        """
        return Requester(headers={'a': '1', 'b': '2'})

    @request_mapping('/{secret}', method=Method.POST)
    def path_var(self):
        """
        路径变量示例
        """
        return Requester(path_var={'secret': 'post'})

    @request_mapping('http://www.baidu.com')
    def other_site(self):
        """
        请求组下面的其它站点
        """
        pass

    def add_header_to_all(self):
        """
        调用此方法后，以后所有的请求都会带上这个headers
        可以用此方法作登录后添加token的操作
        """
        add_header(self, 'walnuts', 'header')


@request_mapping('http://www.baidu.com')
def request_baidu():
    """
    单函数写法
    """
    return Requester()


class Baidu:
    """
    不带group的写法，这种方式，类下的方法不再使用同一个session
    """

    @request_mapping('http://www.baidu.com')
    def request_baidu(self):
        return Requester()


if __name__ == '__main__':
    http_bin = HTTPBin()
    http_bin.add_header_to_all()
    http_bin.post_form().json()
    http_bin.post_json().json()
    http_bin.path_var().json()
    http_bin.other_site().content
    request_baidu().content
