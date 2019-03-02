import os
import glob
import fileinput
from utils import all_files_generator, get_extension

class FilesDirector():

    WILD_CARD = ['.', '*']

    def prepare_files(self):
        self.set_files_to_read()
        self.apply_includes()
        self.apply_excludes()

    def get_file_with_formats(self):
		return map(lambda filename: (filename, filter(lambda fmt: (fmt.get('extension') == get_extension(filename)), self.config.get('formats'))), self.file_list)

    def apply_includes(self):
        pass

    def apply_excludes(self):
    	pass

    def set_files_to_read(self):
        if self.config.get('file_list'):
            # File list has already been passed
            self.file_list = self.config.get('file_list')
            return
        result = []
        for paths in all_files_generator(extensions=self.extensions):
            result += paths

        self.file_list = result


class Processor(FilesDirector):
    """Subclass process that runs complete lifecycle for DYC"""
    def start(self):
    	pass
        # self.setup()
        # self.prompts()
        # self.apply()

    def prepare(self):
    	self.prepare_files()

    @property
    def extensions(self):
        return filter(None, map(lambda fmt: fmt.get('extension'), self.config.get('formats')))
    