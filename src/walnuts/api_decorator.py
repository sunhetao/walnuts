import inspect
from functools import wraps
from urllib.parse import urljoin

from requests import Session

from .config_manager import wrapped_v
from .utils import format_json


class Method:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def request_mapping(path='', method=Method.GET):
    def decorate(cls_or_func):
        @wraps(cls_or_func)
        def wrapper_cls(*args, **kwargs):
            cls = cls_or_func
            obj = cls(*args, **kwargs)
            try:
                obj.path = path.format(**wrapped_v)
            except KeyError as e:
                raise ValueError('%s格式化时发生错误,找不到%s配置,请检查' % (path, e))
            obj.session = Session()
            return obj

        @wraps(cls_or_func)
        def wrapper_func(*args, **kwargs):
            func = cls_or_func
            requester = func(*args, **kwargs) or Requester()
            func_args = inspect.getfullargspec(func).args
            if len(func_args) > 0 and func_args[0] == 'self':
                self = args[0]
                requester.base_path = getattr(self, 'path', '')
                requester.session = getattr(self, 'session', Session())
            requester.func = func
            requester.path = path
            requester.method = method
            requester.do()
            return requester

        if isinstance(cls_or_func, type):
            return wrapper_cls
        else:
            return wrapper_func

    return decorate


def add_header(self, key, value):
    session = getattr(self, 'session', None)
    if not session:
        raise ValueError('add_header需在api类上添加RequestMapping装饰器后可使用')
    session.headers[key] = value


def add_headers(self, headers):
    session = getattr(self, 'session', None)
    if not session:
        raise ValueError('add_headers需在api类上添加RequestMapping装饰器后可使用')
    session.headers.update(headers)


def get_session(self) -> Session:
    return getattr(self, 'session', None)


class Requester:
    def __init__(self, **kwargs):
        self.func = None
        self.session = None
        self.base_path = ''
        self.path = ''
        self.method = ''
        self.kwargs = kwargs
        self.res = None
        self.url = ''

    def __assemble_url(self):
        if self.path.startswith('http'):
            self.url = self.path
        else:
            self.url = urljoin(self.base_path, self.path)

        pv = self.kwargs.pop('path_var', {})
        self.url = self.url.format(**pv)

    def __prepare_request(self):
        self.__assemble_url()

    def __log(self):
        print('\n******************************************************')
        print('1、请求url:\n%s\n' % self.res.request.url)
        print('2、api描述:\n%s\n' % (self.func.__doc__ or self.func.__name__).strip())
        print('3、请求headers:\n%s\n' % format_json(dict(self.res.request.headers)))
        print('4、请求body:\n%s\n' % format_json(self.res.request.body))
        print('5、响应结果:\n%s\n' % format_json(self.res.content))

    def do(self):
        self.__prepare_request()
        self.res = (self.session or Session()).request(self.method, self.url, **self.kwargs)
        self.__log()

    def __getattr__(self, item):
        return getattr(self.res, item)

    @property
    def content(self):
        return self.res.content

    def json(self):
        return self.res.json()
