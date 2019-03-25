import os
from ..utils import read_yaml, read_config
from ..exceptions import FormattingConfigurationHandler
ROOT_PATH = os.getcwd()
DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defaults.yaml')
CUSTOM = os.path.join(ROOT_PATH, 'dyc.yaml')

class Config(object):
    default = read_yaml(DEFAULT)
    custom = read_yaml(CUSTOM)

    def override_basic(self):
        for key, value in self.custom.iteritems():
            if not self.is_mutated(value):
                self.plain[key] = value

    def override_formats(self):
        formats = self.custom.get('formats', [])
        for index, value in enumerate(formats):
            extension = value.get('extension')
            cnf_index = self.get_custom_extension_index(extension)
            try:
                for nested_key, nested_obj in value.iteritems():
                    try: 
                        self.plain.get('formats')[cnf_index][nested_key].update(**nested_obj) if nested_obj else None
                    except AttributeError:
                        continue
            except (IndexError, TypeError):
                self.plain.get('formats').append(value)

    def get_custom_extension_index(self, extension):
        for index, value in enumerate(self.plain.get('formats')):
            if value.get('extension') == extension:
                return index

    def is_mutated(self, value):
        return isinstance(value, list) and len(value) and isinstance(value[0], dict)

    def override(self):
        self.override_basic()
        self.override_formats()
