"""
Entry point to DYC Class

DYC (Document Your Code) Class initiator
is constructed here. It performs all the readings

"""
from utils import get_extension
from methods import MethodBuilder
from base import Processor

class DYC(Processor):

    def __init__(self, config, details=None):
        self.config = config

    def process_methods(self, diff_only=False, changes=[]):
        for filename in self.file_list:
            print('\nProcessing Methods on {filename}\n\r'.format(filename=filename))
            try:
                change = filter(lambda x: x.get('path') == filename, changes)[0]
            except:
                change = None

            extension = get_extension(filename)
            fmt = self.formats.get(extension)
            method_cnf = fmt.get('method', {})
            method_cnf['arguments'] = fmt.get('arguments')
            builder = MethodBuilder(filename, method_cnf)
            builder.initialize(change=change)
            builder.prompts()
            builder.apply()
            builder.clear(filename)

    def process_classes(self):
        # self.classes = ClassesBuilder()
        pass

    def process_top(self):
        # self.tops = TopBuilder()
        pass
