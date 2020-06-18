import sys
from .utils import get_root_dir

PROJECT_DIR = get_root_dir(sys.path[0])


class ConfigManager:
    def __init__(self, project_dir):
        self.__project_dir = project_dir

    def __parse_yaml(self):
        pass

    def __parse_properties(self):
        pass

    def __parse_ini(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass
