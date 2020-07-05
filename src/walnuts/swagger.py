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

    def parse(self):
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
                    'parameters': self.parse_parameters(method_obj.get('parameters', [])),
                }
                api_obj_list.append(api_obj)
        return {'host': self.host, 'info': self.info, 'base_path': self.basePath, 'paths': api_obj_list}

    def parse_parameters(self, parameter_obj_list: list):
        result = defaultdict(dict)
        for parameter_obj in parameter_obj_list:
            parameter_name = parameter_obj.get('name', 'unknown')
            parameter_type = parameter_obj.get('type')
            parameter_schema = parameter_obj.get('schema')

            if parameter_type:
                parameter_value = self.parse_parameter_use_type(parameter_type, parameter_obj)
            else:
                parameter_value = self.parse_parameter_use_schema(parameter_schema)

            result[parameter_obj['in']][parameter_name] = parameter_value

        return result

    def parse_parameter_use_type(self, parameter_type, parameter_obj):
        if parameter_type in ['string', 'integer', 'number', 'file']:
            return self.set_default_value_for_simple_type(parameter_type)
        elif parameter_type == 'array':
            return [self.set_default_value_for_simple_type(parameter_obj['items']['type'])]
        else:
            return 'unknown type'

    def parse_parameter_use_schema(self, parameter_schema: dict):
        parameter_schema_type = parameter_schema.get('type')
        if parameter_schema_type == 'array':
            definition_name = self.get_definition_name_from_path(parameter_schema['items']['$ref'])
            return [self.parse_definition(definition_name)]
        else:
            definition_name = self.get_definition_name_from_path(parameter_schema['$ref'])
            return self.parse_definition(definition_name)

    @staticmethod
    def get_definition_name_from_path(definition_path):
        return definition_path.split('/')[-1]

    @staticmethod
    def set_default_value_for_simple_type(parameter_type):
        if parameter_type == 'string':
            return 'string'
        elif parameter_type in ['integer', 'number']:
            return 1
        elif parameter_type == "boolean":
            return True
        elif parameter_type == 'file':
            return 'file object'
        else:
            raise ValueError('未知类型')

    def parse_definition(self, definition_name):
        result = {}
        try:
            definition_obj = self.definitions[definition_name]
        except KeyError:
            return result
        properties = definition_obj['properties']
        for property_name, property_obj in properties.items():
            property_type = property_obj.get('type')
            property_definition_path = property_obj.get('$ref')
            if property_type:
                if property_type in ['string', 'integer', 'number']:
                    result[property_name] = self.set_default_value_for_simple_type(property_type)
                elif property_type == 'array':
                    property_item_type = property_obj['items'].get('type')
                    property_item_definition_path = property_obj['items'].get('$ref')
                    if property_item_type:
                        result[property_name] = [self.set_default_value_for_simple_type(property_item_type)]
                    if property_item_definition_path:
                        result[property_name] = [
                            self.parse_definition(self.get_definition_name_from_path(property_item_definition_path))]

            if property_definition_path:
                result[property_name] = self.parse_definition(
                    self.get_definition_name_from_path(property_definition_path))
        return result
