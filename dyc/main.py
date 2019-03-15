"""
Entry point to DYC Class

DYC (Document Your Code) Class initiator
is constructed here. It performs all the readings

"""
import sys
import re
import string
import fileinput
import copy
import linecache
import click
from formats import DefaultConfig, ExtensionManager
from utils import get_leading_whitespace, BlankFormatter, get_indent, add_start_end, get_file_lines, get_hunk, get_extension
from .exceptions import QuitConfirmEditor
from .base import Processor

class Builder(object):
    details = dict()

    def initialize(self, change=None):
        result = dict()

        patches = []
        if change:
            patches = change.get('additions')

        for line in fileinput.input(self.filename):
            filename = fileinput.filename()
            lineno = fileinput.lineno()
            keywords = self.config.get('keywords')
            found = len(filter(lambda word: word in keywords, line.split(' '))) > 0

            if change and found:
                found = self._is_line_part_of_patches(lineno, line, patches)

            if not self.details.get(filename):
                self.details[filename] = dict()

            if found:
                length = get_file_lines(filename)
                result = self.extract_and_set_information(filename, lineno, line, length)
                if self.validate(result):
                    self.details[filename][result.name] = result

    def _is_line_part_of_patches(self, lineno, line, patches):
        result = False
        for change in patches:
            start, end = change.get('hunk')
            if start <= lineno <= end:
                patch = change.get('patch')
                found = filter(lambda l: line.replace('\n', '') == l, patch.split('\n'))
                if found:
                    result = True
                    break
        return result

    def prompts(self):
        """Abstract method to get inputs from user"""
        pass

    def apply(self):
        """Abstract method to changes on the file"""
        pass

class MethodFormatter():

    formatted_string = '{open}{break_after_open}{method_docstring}{break_after_docstring}{argument_format}{break_before_close}{close}'
    fmt = BlankFormatter()

    def format(self):
        self.pre()
        self.build_docstrings()
        self.build_arguments()
        self.result = self.fmt.format(self.formatted_string, **self.method_format)
        self.add_indentation()
        self.polish()

    def wrap_strings(self, words):
        subs = []
        n = self.config.get('words_per_line')
        for i in range(0, len(words), n):
            subs.append(" ".join(words[i:i+n]))
        return '\n'.join(subs)

    def pre(self):
        method_format = copy.deepcopy(self.config)
        method_format['indent'] = get_indent(method_format['indent']) if method_format['indent'] else '    '
        method_format['indent_content'] = get_indent(method_format['indent']) if get_indent(method_format['indent_content']) else ''
        method_format['break_after_open'] = '\n' if method_format['break_after_open'] else ''
        method_format['break_after_docstring'] = '\n' if method_format['break_after_docstring'] else ''
        method_format['break_before_close'] = '\n' if method_format['break_before_close'] else ''

        argument_format = copy.deepcopy(self.config.get('arguments'))
        argument_format['inline'] = '' if argument_format['inline'] else '\n'

        self.method_format = method_format
        self.argument_format = argument_format

    def build_docstrings(self):
        text = self.method_docstring or 'Missing Docstring!'
        self.method_format['method_docstring'] = self.wrap_strings(text.split(' '))

    def build_arguments(self):
        config = self.config.get('arguments')
        formatted_args = '{prefix} {type} {name}: {doc}'
        title = self.argument_format.get('title')
        if title:
            underline = '-' * len(title)
            self.argument_format['title'] = '{}\n{}\n'.format(title, underline) if config.get('underline') else '{}\n'.format(title)

        result = []
        if len(self.arguments):
            for argument_details in self.arg_docstring:
                argument_details['prefix'] = self.argument_format.get('prefix')
                result.append(self.fmt.format(formatted_args, **argument_details).strip())
        self.argument_format['body'] = '\n'.join(result)
        self.method_format['argument_format'] = self.fmt.format('{title}{body}', **self.argument_format)

    def add_indentation(self):
        temp = self.result.split('\n')
        space = self.method_format.get('indent')
        indent_content = self.method_format.get('indent_content')
        if indent_content:
            content = temp[1:-1]
            content = [indent_content + docline for docline in temp][1:-1]
            temp[1:-1] = content
        self.result = '\n'.join([space + docline for docline in temp])

    def confirm(self, polished):
        polished = add_start_end(polished)
        method_split = self.plain.split('\n')
        if self.config.get('within_scope'):
            method_split.insert(1, polished)
        else:
            method_split.insert(0, polished)

        result = '\n'.join(method_split)
        message = click.edit('## CONFIRM: MODIFY DOCSTRING BETWEEN START AND END LINES ONLY\n\n' + result)

        if not message:
            raise QuitConfirmEditor('You quit the editor')

        message = '\n'.join(message.split('\n')[2:])
        final = []
        start = False
        end = False

        for x in message.split('\n'):
            stripped = x.strip()
            if stripped == '## END':
                end = True
            if start and not end:
              final.append(x)
            if stripped == '## START':
                start = True

        self.result = '\n'.join(final)

    def polish(self):
        docstring = self.result.split('\n')
        polished = '\n'.join([self.leading_space + docline for docline in docstring])
        self.confirm(polished)


class MethodInterface(MethodFormatter):
    def __init__(self, plain, name, start, end, filename, arguments, config, leading_space):
        self.plain = plain
        self.name = name
        self.start = start
        self.end = end
        self.filename = filename
        self.arguments = arguments
        self.method_docstring = ''
        self.arg_docstring = []
        self.config = config
        self.leading_space = leading_space

    def prompt(self):
        self._prompt_docstring()
        self._prompt_args()
        self.format()

    def _prompt_docstring(self):
        echo_name = click.style(self.name, fg='green')
        self.method_docstring = click.prompt('\n({}) Method docstring '.format(echo_name))

    def _prompt_args(self):
        def _echo_arg_style(argument):
            return click.style('{}'.format(argument), fg='green')
        for arg in self.arguments:
            arg_doc = click.prompt('\n({}) Argument docstring '.format(_echo_arg_style(arg)))
            arg_type = click.prompt('({}) Argument type '.format(_echo_arg_style(arg))) if self.config.get('arguments', {}).get('add_type', False) else ''
            self.arg_docstring.append(dict(type=arg_type, doc=arg_doc, name=arg))


class MethodBuilder(Builder):
    def __init__(self, filename, config):
        self.filename = filename
        self.config = config

    def extract_and_set_information(self, filename, start, line, length):
        start_line = linecache.getline(filename, start)
        initial_line = line
        start_leading_space = get_leading_whitespace(start_line) # Where function started
        method_string = start_line
        line_within_scope = True
        lineno = start + 1
        line = linecache.getline(filename, lineno)
        end_of_file = False
        end = None
        while (line_within_scope and not end_of_file):
            current_leading_space = get_leading_whitespace(line)
            if len(current_leading_space) <= len(start_leading_space) and line.strip():
                end = lineno - 1
                break
            method_string += line
            lineno = lineno + 1
            line = linecache.getline(filename, int(lineno))
            end_of_file = True if lineno > length else False

        if not end:
            end = length

        return MethodInterface(plain=method_string,
                    name=self._set_name(initial_line),
                    start=start,
                    end=end,
                    filename=filename,
                    arguments=self.extract_arguments(initial_line.strip('\n')),
                    config=self.config,
                    leading_space=get_leading_whitespace(initial_line))

    def validate(self, result):
        if not result:
            return False
        name = result.name
        if name not in self.config.get('ignore', []) \
            and not self.is_first_line_documented(result) \
            and click.confirm('Do you want to document method {}?'.format(click.style(name, fg='green'))):
                return True

        return False

    def extract_arguments(self, line):
        args = ArgumentDetails(line, self.config.get('arguments', {}))
        args.extract()
        return args.sanitize()

    def is_first_line_documented(self, result):
        returned = False
        for x in range(result.start, result.end):
            line = linecache.getline(result.filename, x)
            if self.config.get('open') in line:
                result = True
                break
        return returned

    def prompts(self):
        for method_interface in self._method_interface_gen():
            method_interface.prompt()

    def apply(self):
        for method_interface in self._method_interface_gen():
            for line in fileinput.input(method_interface.filename, inplace=True):
                if fileinput.lineno() == method_interface.start:
                    if self.config.get('within_scope'):
                        sys.stdout.write(line + method_interface.result + '\n')
                    else:
                        sys.stdout.write(method_interface.result + '\n' + line)
                else:
                    sys.stdout.write(line)

    def _method_interface_gen(self):
        if not self.details:
            yield None

        for filename, func_pack in self.details.iteritems():
            for method_interface in func_pack.values():
                yield method_interface

    def _set_name(self, line):
        for keyword in self.config.get('keywords', []):
            clear_defs = re.sub('{} '.format(keyword), '', line.strip())
            name = re.sub(r'\([^)]*\)\:', '', clear_defs).strip()
            if re.search(r'\((.*)\)', name):
                name = re.match(r'^[^\(]+', name).group()
            if name:
                return name

class DYC(Processor):

    def __init__(self, config, details=None):
        self.config = config
        self.details = details
        self.result = []

    def setup(self):
        self.details = FilesReader(self.options).details

    def process_methods(self, diff_only=False, changes=[]):
        for filename in self.file_list:
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

    def process_classes(self):
        self.classes = ClassesBuilder()

    def process_top(self):
        self.tops = TopBuilder()

class ArgumentDetails(object):

    def __init__(self, line, config):
        self.line = line
        self.config = config
        self.args = []

    def extract(self):
        ignore = self.config.get('ignore')
        args = re.search(r'\((.*)\)', self.line).group(1).split(', ')
        self.args = filter(lambda x: x not in ignore, filter(None, [arg.strip() for arg in args]))
        
    def sanitize(self):
        return map(lambda arg: re.findall(r"[a-zA-Z0-9_]+", arg)[0], self.args)

    def get_args(self, cnf):
        ignore = cnf.get('ignore')
        args = self.line[self.line.find("(")+1:self.line.find(")")].split(', ')
        return filter(lambda x: x not in ignore, filter(None, [arg.strip() for arg in args]))
