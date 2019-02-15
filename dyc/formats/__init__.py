import os
from ..utils import read_config
ROOT_PATH = os.getcwd()

class DefaultConfig(object):
    def __init__(self, filename):
        curr_path = os.path.join(ROOT_PATH, 'dyc', 'formats')
        file_list = [config for config in os.listdir(curr_path) if config.endswith('.yaml')]
        extension = filename.split('.')[-1]
        config = dict()
        for ext in file_list:
            conf = next(read_config('{}/{}'.format(curr_path, ext)))
            if conf and conf.get('extension') == extension:
                config = conf
                break
		return config

