"""
Entry point to DYC Class

DYC (Document Your Code) Class initiator
is constructed here. It performs all the readings

"""
import sys
import re
import string
import fileinput
import linecache
import click
from formats import DefaultConfig, ExtensionManager
from .utils import get_leading_whitespace, BlankFormatter

class DYC(object):

    def __init__(self, options):
        self.options = options
        self.details = None

    def start(self):
        self.setup()
        self.prompts()
        self.apply()

    def setup(self):
        file_candidates = self.options.get('files')
        files = FilesReader(file_candidates)
        self.details = files.details

    def prompts(self):
    	for method_name, method in self._method_generator():
        	method.process()

    def apply(self):
    	for method_name, method in self._method_generator():
            docs = MethodDocBuilder(method, self.options)
            docs.build()

    def revert(self):
        pass

    def _method_generator(self):
        for filename, details in self.details.iteritems():
            for method_name, method in details.methods.iteritems():
                yield method_name, method

class FilesReader(object):

    def __init__(self, file_list):
        self.list = file_list # List of files

    @property
    def details(self):
        changes = dict()
        for line in fileinput.input(self.list):
            filename = fileinput.filename()

            if not changes.get(fileinput.filename()):
                changes[filename] = FileDetails(filename)

            if line.strip().startswith('def'):
                length = changes[filename].get_file_lines()
                method = MethodDetails(fileinput.filename(), fileinput.lineno(), line, length)
                changes[filename].add_method(method)

        return changes

class FileDetails(object):
    def __init__(self, name):
        self.name = name
        self.methods = dict()

    def add_method(self, method):
        self.methods[method.name] = method

    def get_file_lines(self):
        lines = 0
        with open(self.name, 'r') as stream:
            lines = len(stream.readlines())
        return lines

class MethodDetails(object):
    def __init__(self, filename, start, line, file_length):
        self.filename = filename
        self.start = start
        self.line = line
        self.end = None
        self.file_length = file_length
        self.method_string = self._read_method()
        args = ArgumentDetails(line)
        self.arguments = args.get_args()
        self.name = self.get_method_name()
        self.docs = dict(main='', args=dict())

    def get_method_name(self):
        clear_defs = re.sub('def', '', self.line.strip())
        return re.sub(r'\([^)]*\)\:', '', clear_defs).strip()

    def process(self):
        self.prompts()

    def prompts(self):
        echo_name = click.style(self.name, fg='green')
        echo_args = click.style(', '.join(self.arguments), fg='green')
        click.echo('-------  Method: {} missing documentation -------'.format(echo_name))
        click.echo('-------  Arguments: {} -------'.format(echo_args))
        self._prompt_method(echo_name)
        self._prompt_args()

    def _prompt_method(self, echo_name):
        self.docs['main'] = click.prompt('\n({}) Method docstring '.format(echo_name))

    def _prompt_args(self):
        def _echo_arg_style(argument):
            return click.style('{}'.format(argument), fg='green')
        for arg in self.arguments:
            arg_type = click.prompt('\n({}) Argument type '.format(_echo_arg_style(arg)))
            arg_doc = click.prompt('({}) Argument docstring '.format(_echo_arg_style(arg)))
            self.docs['args'] = dict(type=arg_type, doc=arg_doc)


    def _read_method(self):
        start = linecache.getline(self.filename, self.start)
        start_leading_space = get_leading_whitespace(start) # Where function started
        method_string = start
        line_within_scope = True
        lineno = self.start + 1
        line = linecache.getline(self.filename, lineno)
        end_of_file = False
        while (line_within_scope and not end_of_file):
            current_leading_space = get_leading_whitespace(line)
            if len(current_leading_space) <= len(start_leading_space) and line.strip():
                self.end = lineno - 1
                break
            method_string += line
            lineno = lineno + 1
            line = linecache.getline(self.filename, lineno)
            end_of_file = True if lineno > self.file_length else False
        return method_string

class ArgumentDetails(object):

    def __init__(self, line):
        self.line = line

    def get_args(self):
        args = self.line[self.line.find("(")+1:self.line.find(")")].split(', ')
        return filter(None, [arg.strip() for arg in args])

class ClassDetails(object):
    pass


class MethodDocBuilder(object):
    def __init__(self, method, options):
        self.method = method
        self.options = options
        self.default = DefaultConfig(self.method.filename)
        self.formatting = MethodFormatter(self.default.config.get('extension'), self.default.config.get('method'), self.options)

    def confirm(self):
        pass

    def _build(self):
        print('=====')
        print(self.formatting.run())
        print('=====')

    def build(self):
        self._build()
        self.confirm()

class MethodFormatter(object):

    def __init__(self, extension, default_config, options):
        self.format = default_config
        self.options = options
        self.extension = extension
        self.override()
        # self.params = self.default_config.get('params')
        # if self.default_config.get('break'):
        #     self.default_config['break'] = '\n'
        # if self.params and self.params.get('title'):
        #     title = self.params.get('title')
        #     underline = '-' * len(self.params.get('title'))
        #     self.default_config['params_title'] = '{}\n{}'.format(title, underline)

    def override(self):
        # Overrides custom formatting
        custom = ExtensionManager.get_format_extension(self.extension, self.options.get('formats') or [])
        self.format.update(**custom.get('method'))

    def run(self):
        fmt = BlankFormatter()
        return fmt.format('{open}{break}{docstring}{break}{params_title}{arguments}{break}{close}', **self.format)

    
# MARKER = '# Everything below is ignored\n'
# message = click.edit('\n\n' + MARKER)
# if message is not None:
#     return message.split(MARKER, 1)[0].rstrip('\n')