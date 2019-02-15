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
from .utils import get_leading_whitespace

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
        for filename, details in self.details.iteritems():
            for method_name, method in details.methods.iteritems():
                method.prompts()
                method.confirm()

    def apply(self):
        pass

    def revert(self):
        pass


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
        self._method_docstring = None

    def get_method_name(self):
        clear_defs = re.sub('def', '', self.line.strip())
        return re.sub(r'\([^)]*\)\:', '', clear_defs).strip()

    def confirm(self):
        self._concatenate_documentation()
        # MARKER = '# Everything below is ignored\n'
        # message = click.edit('\n\n' + MARKER)
        # if message is not None:
        #     return message.split(MARKER, 1)[0].rstrip('\n')

    def _concatenate_documentation(self):
        ## TODO ADD A Class that takes method docstring options.
        ## And builds the ideal documentation for us
        quote_strings_start = '{}'.format('"""') # Flexible type, single or double
        quote_strings_end = '{}'.format('"""') # Flexible type, single or double
        leading_space = get_leading_whitespace(self.line)
        full_method_docstrings = '{leading_space}{start_string}{method_docstring}\n{argument_docstring}'.format
        print(full_method_docstrings(leading_space=leading_space,
                                     start_string=quote_strings_start,
                                     method_docstring=self._method_docstring,
                                     argument_docstring=self._arg_docstring,
                                     end_string=quote_strings_end))

    def prompts(self):
        echo_name = click.style(self.name, fg='green')
        echo_args = click.style(', '.join(self.arguments), fg='green')
        click.echo('-------  Method: {} missing documentation -------'.format(echo_name))
        click.echo('-------  Arguments: {} -------'.format(echo_args))
        self._prompt_method(echo_name)
        self._prompt_args()

    def _prompt_method(self, echo_name):
        self._method_docstring = click.prompt('({}) Method docstring '.format(echo_name))

    def _prompt_args(self):
        def _echo_arg_style(argument):
            return click.style('{}'.format(argument), fg='green')
        self._arg_docstring = dict()
        for arg in self.arguments:
            arg_type = click.prompt('({}) Argument type '.format(_echo_arg_style(arg)))
            arg_doc = click.prompt('({}) Argument docstring '.format(_echo_arg_style(arg)))
            self._arg_docstring[arg] = dict(type=arg_type, doc=arg_doc)


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
        return [arg.strip() for arg in args]

class ClassDetails(object):
    pass
