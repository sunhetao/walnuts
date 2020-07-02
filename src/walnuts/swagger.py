import json
from collections import defaultdict
from pprint import pprint

import requests


class SwaggerParser:
    def __init__(self, url_or_json: str):
        self.swagger_json = None
        if url_or_json.startswith('http'):
            self.swagger_json = requests.get(url_or_json).json()
        else:
            with open(url_or_json, encoding='utf-8') as f:
                self.swagger_json = json.loads(f.read())
        self.info = self.swagger_json['info']
        self.host = self.swagger_json['host']
        self.basePath = self.swagger_json['basePath']
        self.tags = self.swagger_json['tags']
        self.paths = self.swagger_json['paths']
        self.definitions = self.swagger_json['definitions']

    def parse_paths(self):
        api_obj_list = []
        for path, path_obj in self.paths.items():
            for method, method_obj in path_obj.items():
                api_obj = {
                    'path': path,
                    'method': method,
                    'tags': method_obj['tags'],
                    'summary': method_obj['summary'],
                    'operation_id': method_obj['operationId'],
                    'consumes': method_obj.get('consumes', None),
                    'parameters': self.convert_parameter_list_to_dict(method_obj.get('parameters', [])),
                }
                api_obj_list.append(api_obj)

    def convert_parameter_list_to_dict(self, parameter_obj_list: list):
        result = defaultdict(dict)
        for parameter_obj in parameter_obj_list:
            parameter_name = parameter_obj['name']
            parameter_type = parameter_obj.get('type')
            parameter_schema = parameter_obj.get('schema')

            if parameter_type:
                parameter_value = self.gen_value_from_parameter_type(parameter_type, parameter_obj)
            else:
                parameter_value = self.gen_value_from_parameter_schema(parameter_schema, parameter_obj)

            result[parameter_obj['in']][parameter_name] = parameter_value

        return result

    def gen_value_from_parameter_type(self, parameter_type, parameter_obj):
        if parameter_type == 'string':
            return 'string'
        elif parameter_type in ['integer', 'number']:
            return 1
        elif parameter_type == 'file':
            pass  # TODO
        elif parameter_type == 'object':
            pass
        elif parameter_type == 'array':
            pass
        else:
            return 'unknown type'

    def gen_value_from_parameter_schema(self, parameter_schema, parameter_obj):
        definition_path = parameter_schema['$ref']
        definition_name = definition_path.split('/')[-1]
        return self.parse_definition(definition_name)

    def parse_definition(self, definition_name):
        definition_obj = self.definitions[definition_name]
        return self.gen_value_from_parameter_type(definition_obj['type'], definition_obj)
