import os
import sys
from copy import deepcopy

from .utils import get_root_dir_and_env, format_json, DDict, WDict, ConfigFileParser

# 项目根目录标志文件名
PROJECT_DIR_FLAG_FILE_NAME = '.walnuts'

# 项目根路径和环境配置
PROJECT_DIR, ENV = get_root_dir_and_env(PROJECT_DIR_FLAG_FILE_NAME, sys.path[0])

if not PROJECT_DIR:
    raise ValueError('找不到项目根目录，请在项目根目录下新建".walnuts"文件')

# 默认使用环境变量里的配置
ENV = os.getenv('env', None) or ENV

# 配置文件名
CONFIG_FILE_NAME = 'config'


class ConfigManager:
    default_flag = 'default'
    yaml_suffix = 'yaml'
    ini_suffix = 'ini'
    json_suffix = 'json'

    def __init__(self, project_dir, config_file_name, env):
        self.project_dir = project_dir
        self.config_file_name = config_file_name
        self.env = env
        self.config = self.get_finally_config()

    def as_dict(self):
        return self.config

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
v = ConfigManager(PROJECT_DIR, CONFIG_FILE_NAME, ENV)

# 拿到配置的copy,避免修改v
wrapped_v = deepcopy(v.as_dict())

# wrapped_v包装后的dict是可以通过'.'来取值的
# d = {'a': {'b': {'c': 1}}}
# 通过包装后, '{a.b.c}'.format(a=wrapped_v(d['a'])) 可以格式化
for i in wrapped_v:
    wrapped_v[i] = DDict(wrapped_v[i])
