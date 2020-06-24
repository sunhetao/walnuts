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

## 修改配置

找到项目根目录下的``config.yaml``文件，修改里面的邮件相关配置，``report.email``下的``email``和``password``是你用来发送测试报告邮件的账号和密码，``to_list``是接收的邮件列表
> 如果yaml配置不太熟的话，可以参考阮一峰大佬的这篇入门教程，http://www.ruanyifeng.com/blog/2016/07/yaml.html

```yaml
app:
  host: http://127.0.0.1:5000

user:
  account: admin@admin.com
  password: 111111

report:
  report_folder: report
  email:
    email: xxxx@126.com
    password: xxxx
    to_list:
      - xxxx@.com
      - xxxx@qq.com
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
邮件如下图所示（目前还比较简陋，后续会持续完善）

![avatar](https://s1.ax1x.com/2020/06/23/NaCIPI.png)

测试报告如下图所示，使用的是``pytest-html``的报告

![avatar](https://s1.ax1x.com/2020/06/23/NaP0OS.png)

# 使用说明
## http请求
- 这里对``requests``库进行了封装，使其更容易使用类组织，并在调用过程中打印相关日志
- 使用类组织时，该类下所定义的所有方法使用同一个``session``，这样就可以保存调用过程中设置的``cookie``，同时也可以通过``add_header``方法，给所有的请求添加请求头，可以很方便实现登录后设置``token``的功能
- 除url和请求方法外，``requests``的其它方法均可传到``Requester``中，效果是一样的

示例如下：
```python
from walnuts import RequestMapping, add_header, Method, Requester


@RequestMapping(path='http://httpbin.org')
class HTTPBin:
    """
    使用类组织http请求
    """
    @RequestMapping('/post', method=Method.POST)
    def post_form(self):
        """
        form请求示例
        """
        return Requester(data={'a': 1, 'b': 2})

    @RequestMapping('/post', method=Method.POST)
    def post_json(self):
        """
        json请求示例
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
        pass

    def add_header_to_all(self):
        """
        调用此方法后，以后所有的请求都会带上这个headers
        可以用此方法作登录后添加token的操作
        """
        add_header(self, 'walnuts', 'header')

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
```

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

account = v['user.account'] # 通过[]取值
password = v('user.password') # 通过()取值

```


# TODO
- [ ] 数据库使用的封装
- [ ] 命令行工具的完善
- [ ] jenkins集成相关文档及脚本
- [ ] 数据解析相关工具封装
- [ ] 其它常用工具

# 联系
QQ群：563337437
  