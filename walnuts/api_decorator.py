import inspect
from copy import deepcopy
from functools import wraps, partial
from urllib.parse import urljoin

from requests import Session

from walnuts.config_manager import wrapped_v
from walnuts.utils import format_json


class Method:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def group(cls=None, path=''):
    if cls is None:
        return partial(group, path=path)

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not isinstance(cls, type):
            raise ValueError('group装饰器只能作用于类')
        obj = cls(*args, **kwargs)
        obj.path = path.format(**wrapped_v)
        obj.session = Session()
        return obj

    return wrapper


def request_mapping(path='', method=Method.GET):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            requester = func(*args, **kwargs) or Requester()
            func_args = inspect.getfullargspec(func).args
            if len(func_args) > 0 and func_args[0] == 'self':
                self = args[0]
                requester.base_path = getattr(self, 'path', '')
                requester.session = getattr(self, 'session', Session())
            else:
                requester.base_path = ''
                requester.session = Session()
            requester.func = func
            requester.path = path
            requester.method = method
            return requester

        return wrapper

    return decorate


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

    def __request(self):
        self.__prepare_request()
        self.res = self.session.request(self.method, self.url, **self.kwargs)
        self.__log()

    def __getattr__(self, item):
        if not self.res:
            self.__request()
        return getattr(self.res, item)

    @property
    def content(self):
        self.__request()
        return self.res.content

    def json(self):
        self.__request()
        return self.res.json()


def add_header(self, key, value):
    session = getattr(self, 'session', None)
    if not session:
        raise ValueError('add_header需要配合group装饰器使用')
    session.headers[key] = value


def add_headers(self, headers):
    session = getattr(self, 'session', None)
    if not session:
        raise ValueError('add_headers需要配合group装饰器使用')
    session.headers.update(headers)
