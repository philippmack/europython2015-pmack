from yaml_parser import parse_yaml
from voluptuous import Schema,Object, Range, Coerce, All, Any, Optional, Lower, Invalid

import re
import sys
import argparse

"""
Python YAML validator
"""
list_of_ints = All([Coerce(int)], msg='invalid list of ints')

from datetime import datetime
def check_date(datestring):
    try:
       fmt='%Y-%m-%d'
       date_to_test = datetime.strptime(datestring, fmt)
       Coerce(datetime)
    except:
       raise Invalid('expected in Y-m-d')

simulation_schema=Schema({
    'quantiles': [All(Coerce(int), Range(1, 100), msg='not a valid quantile')],
    'prediction': {
            'model': str
     },
    'startdate': check_date,
    'enddate': check_date,
    'replenishment': {
             'model': str
    },
    'input_file' : str
})


replenishment_schema=Schema({
    'quantiles': [All(Coerce(int), Range(1, 100), msg='not a valid quantile')],
    'prediction': {
            'model': str
     },
    'replenishment': {
            'model': str
    },
    'input_file' : str
})

def test_file(yamlconfig, types):
    if types=='simulation':
        simulation_schema(yamlconfig['simulation'])
    if types=='replenishemnt':
        replenishment_schema(yamlconfig['replenishment'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--yaml", help="yaml inputfile to test", type=str)
    parser.add_argument("-t","--types", help="type of yaml", type=str)

    args = parser.parse_args()

    ### Parse YAML to test

    to_test = parse_yaml(args.yaml)

    test_file(to_test,args.types)

