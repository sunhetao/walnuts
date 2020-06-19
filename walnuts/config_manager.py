import os
import sys
from .utils import get_root_dir, YamlWrapper, format_json

PROJECT_DIR = get_root_dir(sys.path[0])
CONFIG_FILE_NAME = 'config'


class ConfigManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.config = self.parse_yaml()

    def as_dict(self):
        return dict(self.config)

    def get_file_path(self, suffix):
        file_list = [f.lower() for f in os.listdir(self.project_dir)]
        file_name = '%s.%s' % (CONFIG_FILE_NAME, suffix)
        return os.path.join(self.project_dir, file_name) if file_name in file_list else None

    def parse_yaml(self):
        file_path = self.get_file_path('yaml')
        if file_path:
            return YamlWrapper(file_path).content
        else:
            return {}

    def parse_properties(self):
        pass

    def parse_ini(self):
        pass

    def __getitem__(self, item):
        return self.config[item]

    def __call__(self, item):
        return self.config[item]

    def __repr__(self):
        return format_json(dict(self.config))

    def __str__(self):
        return self.__repr__()


v = ConfigManager(PROJECT_DIR)
