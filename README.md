# walnuts: Tools For Api Test
<p align="center">
<a href="https://github.com/sunhetao/walnuts/" rel="nofollow">
<img src="https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg" data-canonical-src="https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg" alt="image" style="max-width:100%;">
</a>
<a href="https://pypi.org/project/walnuts/" rel="nofollow">
<img src="https://img.shields.io/pypi/v/walnuts.svg" alt="image" style="max-width:100%;">
</a>
</p>

api测试工具集，欢迎大家多提宝贵意见

PS:walnuts的意思是核桃，并不是因为我喜欢吃核桃，也不是因为这跟测试有什么关系，只因为我儿子的小名叫核桃而已



# 安装
使用pip安装和更新
```shell script
pip install -U walnuts
```

# 一个简单的示例
```python
from walnuts import group, request_mapping, add_header, Method, Requester


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

if __name__ == '__main__':
    http_bin = HTTPBin()
    http_bin.add_header_to_all()
    http_bin.post_form().json()
    http_bin.post_json().json()
    http_bin.path_var().json()
```



