import json
import os


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
