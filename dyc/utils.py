"""
Reusable methods throughout DYC
"""
import yaml

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