"""
This file is used to read the 
`.dyc` configurations at the root of a project.

It parses all the configs to be consumed in DYC.
"""


############
# Imports
############

import yaml
import os

from .utils import read_config
from .exceptions import ConfigurationMissing

ROOT_PATH = os.getcwd()

class Config(object):
    def __init__(self):
        self.verbose = False
    	self.options = dict()
        self.name = 'dyc.yaml'
        self.set_config_path(self.name)

    def read(self):
        self.options = next(read_config(self.config_path))
        self._attach_files_to_read()

    def set_config_path(self, name):
        self.config_path = '{}/{}'.format(ROOT_PATH, name) # Default file name

    def _attach_files_to_read(self):
        files = self.options.get('files')
        result = []
        for file_name in files:
            full_path = os.path.join(ROOT_PATH, file_name)
            result.append(full_path) if os.path.exists(full_path) else None
        self.options['files'] = result
