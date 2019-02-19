import os
from ..utils import read_config
from ..exceptions import FormattingConfigurationHandler
ROOT_PATH = os.getcwd()
DEFAULT = os.path.join(ROOT_PATH, 'dyc', 'formats', 'defaults.yaml')

class ExtensionManager(object):
    @classmethod
    def get_format_extension(self, extension, configs):
        result = filter(lambda cnf: cnf.get('extension') == extension, configs)
        if len(result):
        	return result[0]
        else:
        	return dict()

class DefaultConfig(object):
    def __init__(self, filename):
        extension = filename.split('.')[-1]
        configs = next(read_config(DEFAULT))
        try:
            self.config = ExtensionManager.get_format_extension(extension, configs)
        except Exception as e:
            raise FormattingConfigurationHandler(e.message)

     