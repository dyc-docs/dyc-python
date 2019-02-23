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


def get_indent(space):
    if space == 'tab':
        return '\t'
    elif space == '2 spaces':
        return '  '
    elif space == False:
        return ''
    else:
        return '    '


def add_start_end(string):
    leading_space = get_leading_whitespace(string)
    start = '{}## START\n'.format(leading_space)
    end = '\n{}## END'.format(leading_space)
    string.split('\n')
    result = start + string + end
    return result


def get_file_lines(name):
    lines = 0
    with open(name, 'r') as stream:
        lines = len(stream.readlines())
    return lines


def get_hunk(patch):
    import re
    pat = r'.*?\@\@(.*)\@\@.*'
    match = re.findall(pat, patch)
    return [m.strip() for m in match]


def get_additions_in_first_hunk(hunk):
    """Assuming the hunk is a group and a list"""
    if not isinstance(hunk, list): return None, None
    if len(hunk) < 1: return None, None
    adds_patch = hunk[0].split('+')[-1].split(',')
    start = int(adds_patch[0])
    end = int(start) + int(adds_patch[1])
    return start, end


def line_num_for_phrase_in_file(phrase='', filename='', _range=(0, 0)):
    start, end = _range
    with open(filename,'r') as f:
        for (i, line) in enumerate(f):
            within_range = (i >= start) and (i <= end)
            if phrase == line and within_range:
                return i
    return -1
