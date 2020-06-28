import builtins
import inspect
from collections import OrderedDict
from functools import wraps
from urllib.parse import urljoin

from requests import Session

from .config_manager import v
from .utils import format_json

hook_func_dict = dict()


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
                obj.path = path.format(**v.wrapped_v)
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
                requester.api_obj = self
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


# 请求前处理函数名称
BEFORE_REQUEST_FUNC_NAME = 'before_request_func'

# 响应后处理函数名称
AFTER_RESPONSE_FUNC_NAME = 'after_response_func'


def register_func(func_name, func: Method):
    """
    注册函数，如果函数属于类，则添加到类变量中，否则则添加到全局变量中
    """
    func_qualname_tuple = func.__qualname__.split('.')
    if len(func_qualname_tuple) > 1:
        func_key = '.'.join([func.__module__, func_qualname_tuple[0], func_name])
        hook_func_dict[func_key] = func
    else:
        hook_func_dict[func_name] = func


def before_request(func):
    """
    注册请求前处理钩子
    """
    register_func(BEFORE_REQUEST_FUNC_NAME, func)
    return func


def after_response(func):
    """
    注册响应处理钩子
    """
    register_func(AFTER_RESPONSE_FUNC_NAME, func)
    return func


def get_class_registered_func(cls, func_name):
    """
    获取注册在类上的回调函数
    """
    func_key = '.'.join([cls.__module__, cls.__class__.__name__, func_name])
    return hook_func_dict.get(func_key, None)


def get_global_registered_func(func_name):
    """
    获取全局注册的回调函数
    """
    return hook_func_dict.get(func_name, None)


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


class RequestParams:
    def __init__(self, method, url, params, headers, data, _json, others):
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.data = data
        self.json = _json
        self.others = others

    def __repr__(self):
        return format_json(self.__dict__)

    def __str__(self):
        return self.__repr__()


class Requester:

    def __init__(self, **kwargs):
        # api类对象
        self.api_obj = None

        # 该requester实例所在的方法或函数
        self.func = None

        # 请求session
        self.session = None

        # 请求基础路径
        self.base_path = ''

        # 请求路径
        self.path = ''

        # 请求方法
        self.method = ''

        # 请求url
        self.url = ''

        # 请求的其它参数字典
        self.kwargs = kwargs

        # url query参数
        self.params = None

        # headers
        self.headers = None

        # form表单请求参数，格式为字典
        self.data = None

        # json请求参数，格式为字典
        self._json = None

        # 请求参数对象
        self.request_params = None

        # 响应结果
        self.res = None

    @staticmethod
    def fixation_order(d):
        """
        固定参数顺序，以防在传参过程中变掉，导致验签等失败
        """
        o = OrderedDict()
        for i in d:
            o[i] = d[i]
        return o

    def __prepare_session(self):
        self.session = self.session or Session()

    def __prepare_url(self):
        if self.path.startswith('http'):
            self.url = self.path
        else:
            self.url = urljoin(self.base_path, self.path)

        pv = self.kwargs.pop('path_var', {})
        self.url = self.url.format(**pv)

    def __prepare_params(self):
        self.params = self.fixation_order(self.kwargs.pop('params', {}))

    def __prepare_headers(self):
        self.headers = self.kwargs.pop('headers', {})
        self.headers.update(self.session.headers)
        self.headers = self.fixation_order(self.headers)

    def __prepare_data(self):
        self.data = self.fixation_order(self.kwargs.pop('data', {}))

    def __prepare_json(self):
        self._json = self.fixation_order(self.kwargs.pop('json', {}))

    def __prepare_request_params(self):
        self.request_params = RequestParams(
            method=self.method,
            url=self.url,
            params=self.params,
            headers=self.headers,
            data=self.data,
            _json=self._json,
            others=self.kwargs
        )

    def __prepare_request(self):
        self.__prepare_session()
        self.__prepare_url()
        self.__prepare_params()
        self.__prepare_headers()
        self.__prepare_data()
        self.__prepare_json()
        self.__prepare_request_params()

    def __process_before_request(self):
        before_request_class_func = get_class_registered_func(self.api_obj, BEFORE_REQUEST_FUNC_NAME)
        before_request_global_func = get_global_registered_func(BEFORE_REQUEST_FUNC_NAME)

        # 如果hook函数在类里，需要传入类实例
        # 传入的参数为RequestParams实例
        if before_request_class_func:
            before_request_class_func(self.api_obj, self.request_params)
        elif before_request_global_func:
            before_request_global_func(self.request_params)
        else:
            pass

    def __process_log(self):
        print('\n******************************************************')
        print('1、请求url:\n%s\n' % self.res.request.url)
        print('2、api描述:\n%s\n' % (self.func.__doc__ or self.func.__name__).strip())
        print('3、请求headers:\n%s\n' % format_json(dict(self.res.request.headers)))
        print('4、请求body:\n%s\n' % format_json(self.res.request.body))
        print('5、响应结果:\n%s\n' % format_json(self.res.content))

    def do(self):
        self.__prepare_request()
        self.__process_before_request()
        self.res = self.session.request(self.method, self.url,
                                        data=self.data,
                                        headers=self.headers,
                                        json=self._json,
                                        params=self.params,
                                        **self.kwargs)
        self.__process_log()

    def __getattr__(self, item):
        return getattr(self.res, item)

    @property
    def content(self):
        return self.res.content

    def json(self):
        return self.res.json()
