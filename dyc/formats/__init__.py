import os
from ..utils import read_config
from ..exceptions import FormattingConfigurationHandler
ROOT_PATH = os.getcwd()


class ExtensionManager(object):
    @classmethod
    def get_format_extension(self, extension, configs):
        result = filter(lambda cnf: cnf.get('extension') == extension, configs)
        if len(result):
        	return result[0]
        else:
        	return []

class DefaultConfig(object):
    def __init__(self, filename):
        curr_path = os.path.join(ROOT_PATH, 'dyc', 'formats')
        extension = filename.split('.')[-1]
        configs = next(read_config('{}/formats.yaml'.format(curr_path)))
        try:
            self.config = ExtensionManager.get_format_extension(extension, configs)
        except Exception as e:
            raise FormattingConfigurationHandler(e.message)

     