"""
Reusable methods throughout DYC
"""
import yaml
import string

def get_leading_whitespace(s): 
    accumulator = [] 
    for c in s: 
        if c in ' \t\v\f\r\n': 
            accumulator.append(c) 
        else: 
            break 
    return ''.join(accumulator) 

def read_config(path):
    try:
        with open(path, 'r') as config:
            try:
                yield yaml.load(config)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError as io_err:
        print('Configuration File missing, using default')

class BlankFormatter(string.Formatter):
    def __init__(self, default=''):
        self.default=default

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            return kwds.get(key, self.default)
        else:
            return string.Formatter.get_value(key, args, kwds)

