# walnuts: Tools For Api Test
<p align="center">
<a href="https://github.com/sunhetao/walnuts/" rel="nofollow">
<img src="https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg" data-canonical-src="https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg" alt="image" style="max-width:100%;">
</a>
<a href="https://pypi.org/project/walnuts/" rel="nofollow">
<img src="https://img.shields.io/pypi/v/walnuts.svg" alt="image" style="max-width:100%;">
</a>
</p>

api测试工具集，宗旨是不造轮子，尽可能多的集成、组装轮子，以及降低轮子的使用难度，让同学们集中精力把时间花在测试用例的设计上，完成领导们的任务，欢迎大家多提宝贵意见

> walnuts的意思是核桃，并不是因为我喜欢吃核桃，也不是因为这跟测试有什么关系，只因为我儿子的小名叫核桃而已

# 目录 

- [安装](#安装)
- [快速上手](#快速上手)
    - [生成测试项目](#生成测试项目)
    - [安装项目依赖](#安装项目依赖)
    - [修改报告配置](#修改报告配置)
        - [邮件报告](#邮件报告)
        - [钉钉通知](#钉钉通知)
    - [运行测试demo后端服务](#运行测试demo后端服务)
    - [运行测试](#运行测试)
- [使用说明](#使用说明)
    - [预备学习](#预备学习)
    - [API定义](#API定义)
        - [与使用requests方式对比](#与使用requests方式对比)
        - [一些请求示例](#一些请求示例)
        - [请求前、响应后钩子](#请求前、响应后钩子)
    - [配置文件说明](#配置文件说明)
    - [其它工具](#其它工具)
        - [易用的日期类-HumanDatetime](#易用的日期类-HumanDatetime)
- [TODO](#TODO)
- [联系](#联系)


# 安装
使用pip安装和更新
```shell script
pip install -U walnuts
```

# 快速上手
## 生成测试项目

> 注意：安装完成后，需要重新打开一个命令行才可以使用``walnuts``命令

```
E:\PycharmProjects>walnuts init
请输入项目名称,如order-api-test: user-api-test
开始创建user-api-test项目
开始渲染...
生成 .gitignore                       [√]
生成 .walnuts                         [√]
生成 api                              [√]
生成 app_for_test.py                  [√]
生成 common                           [√]
生成 config.yaml                      [√]
生成 db                               [√]
生成 README.md                        [√]
生成 report                           [√]
生成 requirements.txt                 [√]
生成 test_suites                      [√]
生成 __pycache__                      [√]
生成成功,请使用编辑器打开该项目

```

会生成如下项目

```
├── README.md               # 帮助文档
├── .gitignore              # 配置忽略不想被GIT管理的文件
├── .walnuts                # 项目根目录标识
├── app_for_test.py         # 演示使用的web服务文件
├── config.yaml             # 配置文件
├── requirements.txt        # 项目依赖文件
├── report                  # 测试报告存放文件夹
├── api                     # api定义包
│   ├── __init__.py
│   ├── demo.py
│   └── ...
├── common                  # 通用工具包
│   ├── __init__.py
│   ├── assert_tools.py
│   └── ...
├── db                      # db包
│   ├── __init__.py
│   └── ...
└── test_suites             # 测试用例包
    ├── __init__.py
    ├── test_book_list.py
    ├── test_login.py
    └── ...
```

## 安装项目依赖
进入到项目文件夹下，使用``pip install -r requirements.txt``命令安装项目依赖，过程如下所示

```shell script
E:\PycharmProjects>cd user-api-test

E:\PycharmProjects\user-api-test>pip install -r requirements.txt
Looking in indexes: https://pypi.douban.com/simple
Requirement already satisfied: walnuts in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from -r requirements.txt (line 1)) (0.0.2)
Requirement already satisfied: flask in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from -r requirements.txt (line 2)) (1.1.2)
Requirement already satisfied: flask_login in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from -r requirements.txt (line 3)) (0.5.0)
Requirement already satisfied: pytest in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from -r requirements.txt (line 4)) (5.4.3)
Requirement already satisfied: pytest-html in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from -r requirements.txt (line 5)) (2.1.1)
Requirement already satisfied: pyyaml in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from walnuts->-r requirements.txt (line 1)) (5.3.1)
Requirement already satisfied: requests in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from walnuts->-r requirements.txt (line 1)) (2.23.0)
Requirement already satisfied: jinja2 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from walnuts->-r requirements.txt (line 1)) (2.11.2)
Requirement already satisfied: click in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from walnuts->-r requirements.txt (line 1)) (7.1.2)
Requirement already satisfied: configobj in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from walnuts->-r requirements.txt (line 1)) (5.0.6)
Requirement already satisfied: itsdangerous>=0.24 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from flask->-r requirements.txt (line 2)) (1.1.0)
Requirement already satisfied: Werkzeug>=0.15 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from flask->-r requirements.txt (line 2)) (1.0.1)
Requirement already satisfied: colorama; sys_platform == "win32" in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (0.4.3)
Requirement already satisfied: wcwidth in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (0.1.9)
Requirement already satisfied: attrs>=17.4.0 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (19.3.0)
Requirement already satisfied: py>=1.5.0 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (1.8.2)
Requirement already satisfied: atomicwrites>=1.0; sys_platform == "win32" in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (1.4.0)
Requirement already satisfied: packaging in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (20.4)
Requirement already satisfied: pluggy<1.0,>=0.12 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (0.13.1)
Requirement already satisfied: more-itertools>=4.0.0 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest->-r requirements.txt (line 4)) (8.4.0)
Requirement already satisfied: pytest-metadata in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from pytest-html->-r requirements.txt (line 5)) (1.9.0)
Requirement already satisfied: idna<3,>=2.5 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from requests->walnuts->-r requirements.txt (line 1)) (2.9)
Requirement already satisfied: chardet<4,>=3.0.2 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from requests->walnuts->-r requirements.txt (line 1)) (3.0.4)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from requests->walnuts->-r requirements.txt (line 1)) (2020.4.5.1)
Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from requests->walnuts->-r requirements.txt (line 1)) (1.25.9)
Requirement already satisfied: MarkupSafe>=0.23 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from jinja2->walnuts->-r requirements.txt (line 1)) (1.1.1)
Requirement already satisfied: six in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from configobj->walnuts->-r requirements.txt (line 1)) (1.14.0)
Requirement already satisfied: pyparsing>=2.0.2 in c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages (from packaging->pytest->-r requirements.txt (line 4)) (2.4.7)
WARNING: You are using pip version 19.2.3, however version 20.1.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.

```

## 修改报告配置
### 邮件报告

找到项目根目录下的``config.yaml``文件，修改里面的邮件相关配置，``report.email``下的``email``和``password``是你用来发送测试报告邮件的账号和密码，``to_list``是接收的邮件列表，具体配置可以参考下面的配置

注意：需要开启**SMTP服务**，如果你开启了**授权码**的话，``password``需要填入授权码，而不是你的密码

> 如果yaml配置不太熟的话，可以参考阮一峰大佬的这篇入门教程，http://www.ruanyifeng.com/blog/2016/07/yaml.html

### 钉钉通知
配置钉钉通知的方式如下

1、打开要通知的钉钉群，打开群助手，点击添加机器人

![N7H5N9.png](https://s1.ax1x.com/2020/07/01/N7H5N9.png)

2、选择群机器人中的自定义

![N7b1DU.png](https://s1.ax1x.com/2020/07/01/N7b1DU.png)

3、输入机器人名字，勾选自定义关键词，关键词输入TEST（暂时只支持关键词配置），勾选协议，点击完成

![N7O5qK.png](https://s1.ax1x.com/2020/07/01/N7O5qK.png)

4、添加成功后，把webhook复制出来

![N7XFRs.png](https://s1.ax1x.com/2020/07/01/N7XFRs.png)

5、把webhook url配置到``report.dingtalk``下的``hook_url``处，如下面配置所示


```yaml
app:
  host: http://127.0.0.1:5000

user:
  account: admin@admin.com
  password: 111111

report:
  report_folder: report
  email:
    trigger: fail # 只在失败时发送
    email: xxxx@126.com
    password: xxxx
    to_list:
      - xxxx@.com
      - xxxx@qq.com
  dingtalk:
    trigger: fail # 只在失败时发送
    hook_url: https://oapi.dingtalk.com/robot/send?access_token=XXXX
```

## 运行测试demo后端服务
项目初始化后，会有一些示例，现在需要启动一下这些示例调用的接口的服务，这个跟我们的测试是没有关系的，执行过程如下：

```shell script
E:\PycharmProjects\user-api-test>python app_for_test.py
 * Serving Flask app "app_for_test" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

## 运行测试
在项目根目录下执行 ``walnuts run``命令，会执行测试，并在测试完成后自动发送邮件测试报告，过程如下：

```shell script
E:\PycharmProjects\order-api-test>walnuts run
========================================================================================================= test session starts =========================================================================================================
platform win32 -- Python 3.8.2, pytest-5.4.3, py-1.8.2, pluggy-0.13.1
rootdir: E:\PycharmProjects\order-api-test
plugins: html-2.1.1, metadata-1.9.0
collected 3 items                                                                                                                                                                                                                      

test_suites\test_book_list.py .                                                                                                                                                                                                  [ 33%]
test_suites\test_login.py ..                                                                                                                                                                                                     [100%]

========================================================================================================== warnings summary ===========================================================================================================
c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages\_pytest\junitxml.py:417
  c:\users\administrator\appdata\local\programs\python\python38\lib\site-packages\_pytest\junitxml.py:417: PytestDeprecationWarning: The 'junit_family' default value will change to 'xunit2' in pytest 6.0.
  Add 'junit_family=xunit1' to your pytest.ini file to keep the current format in future versions of pytest and silence this warning.
    _issue_warning_captured(deprecated.JUNIT_XML_DEFAULT_FAMILY, config.hook, 2)

-- Docs: https://docs.pytest.org/en/latest/warnings.html
------------------------------------------------------------------ generated xml file: E:\PycharmProjects\order-api-test\report\junit_report-2020-06-23-22-51-45.xml ------------------------------------------------------------------
-------------------------------------------------------------- generated html file: file://E:\PycharmProjects\order-api-test\report\html_report-2020-06-23-22-51-45.html --------------------------------------------------------------
==================================================================================================== 3 passed, 1 warning in 0.92s =====================================================================================================
邮件发送成功，请查收

```
### 邮件如下图所示（目前还比较简陋，后续会持续完善）

![avatar](https://s1.ax1x.com/2020/06/23/NaCIPI.png)

### 测试报告如下图所示，使用的是``pytest-html``的报告

![avatar](https://s1.ax1x.com/2020/06/23/NaP0OS.png)

### 钉钉通知如下图所示

![NHedzt.png](https://s1.ax1x.com/2020/07/01/NHedzt.png)

# 使用说明
## 预备学习
除了``python``之外，你还需要学习一下``requests``库和``pytest``的使用，我们的工具是基于这两个库的，相关资料如下 

- https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html
- https://docs.pytest.org/en/stable/

## API定义
- 这里对``requests``库进行了封装，使其更容易使用类组织HTTP请求，并在调用过程中打印相关日志
- 使用类组织时，该类下所定义的所有方法使用同一个``session``，这样就可以保存调用过程中设置的``cookie``，同时也可以通过``add_header``方法，给所有的请求添加请求头，可以很方便实现登录后设置``token``的功能
- 除url和请求方法已在``RequestMapping``装饰器中定义之外，使用``requests``时的其它参数均可传到``Requester``中，效果是一样的

> 这里需要理解一下session的概念，https://requests.readthedocs.io/en/master/user/advanced/#session-objects

### 与使用requests方式对比
``requests``已经很简单，很好用的，为什么还要封装呢？

``requests``的确非常好用，但它只是一个http请求库，如果用来做测试的话，势必要解决很多测试中遇到的问题，比如：

- 需要在每次发请求都打印出相关报文，每个请求里都需要写一遍
- 接口请求需要签名，每个请求里都需要单独写一遍
- 需要对请求响应后的结果做下初步断言，同样也需要在每个请求里写一遍
- ...

所以我们还需要封装，加以改造一下，改造完可以实现如下功能

- 集成打印报文功能
- 增加多层级请求前响应后回调功能
- 提取url和方法，使我们的api定义看起来更清晰
- 简化使用，隐藏session，一般操作不需要接触session
- 包装响应结果，使其更容易取值，如自动解析xml，自动集成json的objectpath取值功能 
- ...

下面是使用形式上的对比，具体功能我们后面再介绍

```python
import requests
from walnuts import RequestMapping, Method, Requester

# 使用requests
url = 'http://www.baidu.com'
params = {'a': 1, 'b': 2}
headers = {'a': '1', 'b': '2'}
data = {'a': 1, 'b': 2}
res = requests.post(url, params=params, headers=headers, data=data)

@RequestMapping(path='http://www.baidu.com', method=Method.POST)
def post_baidu():
    params = {'a': 1, 'b': 2}
    headers = {'a': '1', 'b': '2'}
    data = {'a': 1, 'b': 2}
    return Requester(params=params, headers=headers, data=data)
```

### 一些请求示例
```python
from walnuts import RequestMapping, add_header, Method, Requester, add_headers, get_session


@RequestMapping(path='http://httpbin.org')
class HTTPBin:
    """
    使用类组织http请求
    """

    @RequestMapping('/post', method=Method.POST)
    def post_form(self):
        """
        form表单格式请求示例
        """
        return Requester(data={'a': 1, 'b': 2})

    @RequestMapping('/post', method=Method.POST)
    def post_json(self):
        """
        json格式请求示例
        """
        return Requester(json={'a': 1, 'b': 2})

    @RequestMapping('/post', method=Method.POST)
    def with_header(self):
        """
        带headers示例
        """
        return Requester(headers={'a': '1', 'b': '2'})

    @RequestMapping('/{secret}', method=Method.POST)
    def path_var(self):
        """
        路径变量示例
        """
        return Requester(path_var={'secret': 'post'})

    @RequestMapping('http://www.baidu.com')
    def other_site(self):
        """
        请求组下面的其它站点
        """
        return Requester()

    def add_header_to_all(self):
        """
        调用此方法后，以后所有的请求都会带上{'walnuts': 'header'}这个header
        可以用此方法作登录后添加token的操作
        """
        add_header(self, 'walnuts', 'header')

    def add_headers_to_all(self):
        """
        调用此方法后，以后所有的请求都会带上这个方法所添加的headers
        """
        headers = {'a': 'a', 'b': 'b', 'c': 'c'}
        add_headers(self, headers)

    def get_request_session(self):
        """
        获取session的方式
        """
        return get_session(self)


@RequestMapping('http://httpbin.org/post', method=Method.POST)
def post_json():
    """
    使用函数组织
    """
    return Requester(json={'a': 1, 'b': 2})


if __name__ == '__main__':
    http_bin = HTTPBin()
    http_bin.add_header_to_all()
    http_bin.post_form().json()
    http_bin.post_json().json()
    http_bin.path_var().json()
    post_json()

```

### 请求前、响应后钩子
我们有时需要在http请求前做一些事情，比如计算签名，或者在http响应后增加补步响应断言等，``walnuts``提供了``BeforeRuqest``和``AfterResponse``两个装饰器，可以协助完成这个工作

这里提供3个级别，分别是``全局、类、方法``，模块加载完成后，会分别注册，当执行http请求里，会按照 ``全局 -> 类 -> 方法``的顺序依次执行，全局和类级别可定义多个回调函数，方法级别只能定义一个

``talk is cheap, show me the code``



```python
from pprint import pprint

from walnuts import RequestMapping, Requester, BeforeRequest, AfterResponse, Method, RequestObject, ResponseObject


@BeforeRequest
def global_hook_func1(request: RequestObject):
    """
    全局请求前回调函数1
    :param request: 请求对象，后面的RequestObject用来辅助IDE提示功能，该参数在请求前会自动注入，无需要自己调用
    """

    # 请求前给headers添加值
    request.headers['global_hook_func1'] = 'global_hook_func1'

    # 查看request对象内容
    pprint(request)

    # 获取编码后的url query参数
    print(request.get_encoded_params())

    # 获取json字符串，直接通过request.json获取到的是字典
    print(request.get_dumped_json())

    # 获取编码后的data参数，即form表单形式提交时的body数据
    print(request.get_encoded_data())


@BeforeRequest
def global_hook_func2(request: RequestObject):
    """
    全局请求前回调函数2
    """
    request.headers['global_hook_func2'] = 'global_hook_func2'


@AfterResponse
def global_response_hook_func(response: ResponseObject):
    """
    全局响应后回调函数
    :param response:响应对象，同requests的响应对象
    """
    print('断言响应状态码是200\n')
    assert response.status_code == 200


def post1_before_func(request: RequestObject):
    """
    给HTTPBin1 post1方法使用的回调函数
    """
    request.headers['post1_before_func'] = 'post1_before_func'


def post2_before_func(request: RequestObject):
    """
    给HTTPBin1 post2方法使用的回调函数
    """
    request.headers['post2_before_func'] = 'post2_before_func'


@RequestMapping('http://httpbin.org/')
class HTTPBin1:

    @BeforeRequest
    def class_hook_func(self, request: RequestObject):
        """
        类级别的请求前回调函数
        """
        request.headers['HTTPBin1_class_hook_func1'] = 'HTTPBin1_class_hook_func1'

    @RequestMapping(path='/post', method=Method.POST, before_request=post1_before_func)
    def post_1(self):
        """
        HTTPBin1 post_1
        """
        return Requester()

    @RequestMapping(path='/post', method=Method.POST, before_request=post2_before_func)
    def post_2(self):
        """
        HTTPBin1 post_2
        """
        return Requester()


@RequestMapping('http://httpbin.org/')
class HTTPBin2:

    @BeforeRequest
    def class_hook_func(self, request: RequestObject):
        """
        类级别的请求前回调函数
        """
        request.headers['HTTPBin2_class_hook_func1'] = 'HTTPBin2_class_hook_func1'

    @RequestMapping(path='/post', method=Method.POST)
    def post(self):
        """
        HTTPBin2 post
        """
        return Requester()


if __name__ == '__main__':
    HTTPBin1().post_1()
    HTTPBin1().post_2()
    HTTPBin2().post()

```

在如上示例中，HTTPBin1的post_1请求，会添加如下header
- ``global_hook_func1: global_hook_func1`` 全局级别
- ``global_hook_func2: global_hook_func2`` 全局级别
- ``HTTPBin1_class_hook_func1: HTTPBin1_class_hook_func1`` HTTPBin1类级别
- ``post1_before_func： post1_before_func HTTPBin`` post_1方法级别

HTTPBin1的post_2请求，会添加如下header
- ``global_hook_func1: global_hook_func1`` 全局级别
- ``global_hook_func2: global_hook_func2`` 全局级别
- ``HTTPBin1_class_hook_func1: HTTPBin1_class_hook_func1`` HTTPBin1类级别
- ``post2_before_func： post2_before_func HTTPBin`` post_2方法级别

HTTPBin2的post请求，会添加如下header
- ``global_hook_func1: global_hook_func1`` 全局级别
- ``global_hook_func2: global_hook_func2`` 全局级别
- ``HTTPBin2_class_hook_func1: HTTPBin2_class_hook_func1`` HTTPBin1类级别

同时，所以请求都会执行``global_response_hook_func``函数里定义的断方

> 需要注意的是，当同一级别有多个回调函数时，执行是按照加载的顺序，所以同一级别多个回调函数之前不要有关联，加载顺序有时并不是你看的的那样


## 配置文件说明
配置文件名约定为``config``，可以使用``ini``、``json``、``yaml``，优先级为：``yaml > json > ini``

如果是多环境的话，可以在后面加上环境名，如``config-test.yaml``，需要有``.walnuts``中写入test标识，测试环境的配置大于默认配置，如有同名参数，测试环境配置会覆盖默认环境配置

所有配置加载完之后会放到变量``v``里，可以通过``[]``或``()``取值，如下示例：

假设有配置如下
```yaml
app:
  host: http://127.0.0.1:5000

user:
  account: admin@admin.com
  password: 111111

```
则可通过如下代码获取配置

```python
from walnuts import v

host =v['app']['host'] # 通过字典方式取值
account = v['user.account'] # 通过[x.x]方式取值
password = v('user.password') # 通过(x.x)方式取值

```

## 其它工具
这里主要提供一些在测试中常用到的一些数据处理工具，不断完善中，欢迎提需求^_^

### 易用的日期类-HumanDatetime

```python
import time
from datetime import datetime, date

from walnuts import HumanDateTime

# 解析时间戳
print(repr(HumanDateTime(1490842267)))
print(HumanDateTime(1490842267000))
print(HumanDateTime(1490842267.11111))
print(HumanDateTime(1490842267111.01))

# 解析字符串格式日期
print(HumanDateTime('2017-02-02'))
print(HumanDateTime('Thu Mar 30 14:21:20 2017'))
print(HumanDateTime(time.ctime()))
print(HumanDateTime('2017-3-3'))
print(HumanDateTime('3/3/2016'))
print(HumanDateTime('2017-02-02 00:00:00'))

# 解析datetime或date类型时间
print(HumanDateTime(datetime(year=2018, month=11, day=30, hour=11)))
print(HumanDateTime(date(year=2018, month=11, day=30)))

# 增加减少时间
print(HumanDateTime('2017-02-02').add_day(1))
print(HumanDateTime('2017-02-02').sub_day(1))
print(HumanDateTime('2017-02-02').add_hour(1))
print(HumanDateTime('2017-02-02').sub_hour(1))
print(HumanDateTime('2017-02-02').add(days=1, hours=1, weeks=1, minutes=1, seconds=6))
print(HumanDateTime('2017-02-02').sub(days=1, hours=1, weeks=1, minutes=1, seconds=6))

# 转换为时间戳
print(HumanDateTime(1490842267.11111).timestamp_second)
print(HumanDateTime(1490842267.11111).timestamp_microsecond)
print(HumanDateTime('2017-02-02 12:12:12.1111').add_day(1).timestamp_microsecond)
print(HumanDateTime('2017-02-02 12:12:12 1111').add_day(1).timestamp_microsecond)

# 比较大小
print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:12:11 1111'))
print(HumanDateTime('2017-02-02 12:12:12 1111') < HumanDateTime('2017-02-02 12:13:11 1111'))
print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:11:11')
print(HumanDateTime('2017-02-02 12:12:12 1111') < '2017-02-02 12:13:11 1111')
print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:11 1111')
print(HumanDateTime('2017-02-02 12:12:12 1111') == '2017-02-02 12:13:12 1111')
print(HumanDateTime('2017-02-02 12:12:12 1111') <= '2017-02-02 12:13:11 1111')
print(HumanDateTime('2017-02-02 12:12:12 1111') >= '2017-02-02 12:13:11 1111')
print(HumanDateTime('2017-02-02 12:12:12 1111') != time.time())
print(HumanDateTime('2017-02-02 12:12:12 1111') <= time.time())
print(HumanDateTime('2017-02-02 12:12:12 1111') >= time.time())

# 约等于或者接近
print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:11 1111'))
print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111'))
print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:10 1111', offset=2))
print(HumanDateTime('2017-02-02 12:12:12 1111').approach('2017-02-02 12:12:14 1111', offset=2))

# 调用datetime的方法和属性
print(HumanDateTime('2017-02-02 12:12:12 1111').day)
print(HumanDateTime('2017-02-02 12:12:12 1111').year)
print(HumanDateTime('2017-02-02 12:12:12 1111').second)
print(HumanDateTime('2017-02-02 12:12:12 1111').date())

```


# TODO
- [ ] 数据库使用的封装
- [ ] 命令行工具的完善
- [ ] jenkins集成相关文档及脚本
- [ ] 数据解析相关工具封装
- [ ] 其它常用工具

# 联系
QQ群：563337437
  