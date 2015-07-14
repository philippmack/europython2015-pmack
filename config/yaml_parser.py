# -*- coding: utf-8 -*-
import yaml

def parse_yaml(path_to_yaml_file):
    """
    Parses a yaml file
    :param path_to_yaml_file:
    :return:
    """
    # Parse Yaml file
    with open(path_to_yaml_file) as yaml_file :
        yaml_config =yaml.load(yaml_file)
        return yaml_config

def load_yaml(yaml_string):
    """
    Parses a yaml string
    :param yaml_string:
    :return:
    """
    # Parse Yaml file
    yaml_config =yaml.load(yaml_string)
    return yaml_config

