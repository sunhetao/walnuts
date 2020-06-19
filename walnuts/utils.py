import json
import os
import traceback
from collections import UserDict

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


def get_root_dir(cur_dir):
    if '.walnuts' in os.listdir(cur_dir):
        return cur_dir
    up_dir = os.path.dirname(cur_dir)
    if up_dir == cur_dir:
        return None
    return get_root_dir(up_dir)


class WDict(UserDict):
    """
    It's hard to name！！！
    注意：正常使用key中不能再出现 "."，否则会被拆分掉，如a['a.b.c']等于a['a']['b']['c']
    示例：> d = {'a': {'b': 'c': 1}}
         > print(WDict(**d)['a.b.c']) # 1
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


class YamlWrapper:
    def __init__(self, file_path):
        if not isinstance(file_path, str):
            raise ValueError('file_path error, is not a valid str')

        if not os.path.isfile(file_path):
            raise ValueError('file_path error, is not a valid file path')

        self.__file_path = file_path
        self.content = None
        try:
            with open(self.__file_path) as f:
                self.content = load(f, Loader)
        except Exception:
            traceback.print_exc()
            raise ValueError('%s is not a valid yaml file' % file_path)

        self.content = WDict(**self.content)

    def __getitem__(self, item):
        return self.content[item]
