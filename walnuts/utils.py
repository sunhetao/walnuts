import json
import os
import traceback
from collections import UserDict
from functools import partial

from configobj import ConfigObj
from yaml import load, dump
from yaml import Loader, Dumper


def format_json(content):
    if isinstance(content, (str, bytes)):
        try:
            content = json.loads(content)
        finally:
            return content

    result = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')). \
        encode('latin-1').decode('unicode_escape')

    return result


def get_root_dir_and_env(flag_file_name, cur_dir):
    if flag_file_name in os.listdir(cur_dir):
        with open(os.path.join(cur_dir, flag_file_name)) as f:
            return cur_dir, f.read().strip()

    up_dir = os.path.dirname(cur_dir)
    if up_dir == cur_dir:
        return None, None
    return get_root_dir_and_env(flag_file_name, up_dir)


class WDict(UserDict):
    """
    It's hard to name！！！
    注意：正常使用key中不能再出现 "."，否则会被拆分掉，如a['a.b.c']等于a['a']['b']['c']
    示例：> d = {'a': {'b': 'c': 1}}
         > print(WDict(**d)['a.b.c']) # -> 1
    """

    def __getitem__(self, item: str):
        key_list = item.split('.')
        content = self.data
        for key in key_list:
            key = int(key) if str.isdigit(key) else key
            try:
                content = content[key]
            except (KeyError, IndexError):
                return None
        return content


class DDict:
    """
    It's hard to name！！！
    示例: > d = {'a': {'b': 'c': 1}}
         > print(d.a.b.c) # 1
    """

    def __init__(self, d):
        self.__d = d

    def __getattr__(self, item):
        try:
            return DDict(self.__d[item])
        except TypeError:
            raise ValueError('找不到%s配置，请检查' % item)

    def __str__(self):
        return str(self.__d)


class ConfigFileParser:
    def __init__(self, suffix, file_path):
        if not isinstance(file_path, str):
            raise ValueError('file_path error, is not a valid str')

        if not os.path.isfile(file_path):
            raise ValueError('file_path error, is not a valid file path')

        self.file_path = file_path
        self.content = None
        self.parser = self.get_parser(suffix)

        try:
            with open(self.file_path, encoding='utf-8') as f:
                self.content = self.parser(f) or {}
        except Exception:
            traceback.print_exc()
            raise ValueError('%s is not a valid %s file' % (file_path, suffix))

    @staticmethod
    def get_parser(suffix):
        if suffix == 'yaml':
            return partial(load, Loader=Loader)
        elif suffix == 'json':
            return json.load
        elif suffix == 'ini':
            return ConfigObj
        else:
            raise ValueError('不支持的配置文件类型')

    def as_dict(self):
        return self.content
