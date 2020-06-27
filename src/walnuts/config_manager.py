import abc
import os
from copy import deepcopy

from .utils import get_root_dir, format_json, DDict, WDict, ConfigFileParser

# 项目根目录标志文件名
PROJECT_DIR_FLAG_FILE_NAME = '.walnuts'

# 配置文件名
CONFIG_FILE_NAME = 'config'


class ConfigManager:
    default_flag = 'default'
    yaml_suffix = 'yaml'
    ini_suffix = 'ini'
    json_suffix = 'json'

    def __init__(self, config_file_name):
        self._project_dir = None
        self.config_file_name = config_file_name
        self._env = None
        self._config = None
        self._wrapped_v = None

    def as_dict(self):
        return self.config

    @property
    def project_dir(self):
        if not self._project_dir:
            self._project_dir = get_root_dir(PROJECT_DIR_FLAG_FILE_NAME, os.getcwd())

        return self._project_dir

    @property
    def env(self):
        if not self._env:
            with open(os.path.join(self.project_dir, PROJECT_DIR_FLAG_FILE_NAME), encoding='utf-8') as f:
                env = f.read()
            self._env = os.getenv('env', None) or env
        return self._env

    @property
    def config(self):
        if not self._config:
            self._config = self.get_finally_config()
        return self._config

    @property
    def wrapped_v(self):
        if not self._wrapped_v:
            # 拿到配置的copy,避免修改v
            self._wrapped_v = deepcopy(self.config)

            # wrapped_v包装后的dict是可以通过'.'来取值的
            # d = {'a': {'b': {'c': 1}}}
            # 通过包装后, '{a.b.c}'.format(a=wrapped_v(d['a'])) 可以格式化
            for i in self._wrapped_v:
                self._wrapped_v[i] = DDict(self._wrapped_v[i])

        return self._wrapped_v

    def get_file_path(self, suffix, env):
        """
        根据文件后缀和环境获取配置文件完整路径
        """
        file_list = [f.lower() for f in os.listdir(self.project_dir)]
        if env == self.default_flag:
            file_name = '%s.%s' % (self.config_file_name, suffix)
        else:
            file_name = '%s-%s.%s' % (self.config_file_name, env, suffix)
        return os.path.join(self.project_dir, file_name) if file_name in file_list else None

    def get_config_by_suffix_and_env(self, suffix, env):
        """
        根据文件后缀和环境定位配置文件，然后解析并返回
        """
        if not env:
            return {}
        file_path = self.get_file_path(suffix, env)
        return ConfigFileParser(suffix, file_path).as_dict() if file_path else {}

    def get_finally_config(self):
        """
        获取最终配置，加载优先级 yaml > json > ini
        自定义的配置 > default环境配置
        """
        config = {}

        for env in (self.default_flag, self.env):
            for suffix in (self.ini_suffix, self.json_suffix, self.yaml_suffix):
                config.update(self.get_config_by_suffix_and_env(suffix, env))

        return config

    def __getitem__(self, item):
        """
        WDict包装后，支持 d['a.b.c'] 方式取值
        """
        return WDict(**self.config)[item]

    def __call__(self, item):
        """
        支持d('a.b.c')格式取值
        """
        return self[item]

    def __repr__(self):
        return format_json(self.config)

    def __str__(self):
        return repr(self)


# 配置管理器，使用方式如下：
# v['a']['b']['c'] 或者 v['a.b.c'] 再或者 v('a.b.c')
v = ConfigManager(CONFIG_FILE_NAME)


class ReportConfig(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_config(self):
        pass

    @abc.abstractmethod
    def need_send_report(self):
        pass


class EmailReportConfig(ReportConfig):

    def __init__(self):
        self.server = None
        self.email = None
        self.password = None
        self.to_list = None
        # self.subject = None
        self.debug_level = None
        self.report_folder = None

    def set_config(self):
        self.server = v['report.email.server']
        self.email = v['report.email.email']
        self.password = v['report.email.password']
        self.to_list = v['report.email.to_list']
        self.debug_level = v['report.email.debug_level'] or 0
        self.report_folder = v['report.report_folder'] or ''

        if not self.server and self.email:
            self.server = 'smtp.' + self.email.split('@')[-1]

    def need_send_report(self):
        return self.server and self.email and self.password and self.to_list


class DingTalkReportConfig(ReportConfig):

    def __init__(self):
        self.hook_url = None

    def set_config(self):
        self.hook_url = v['report.dingtalk.hook_url']

    def need_send_report(self):
        return self.hook_url
