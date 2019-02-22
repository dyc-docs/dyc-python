import os
import click
import tempfile
from .parser import Config
from .main import DYC
from diff import Diff

config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@config
def main(config):
    config.read()
    pass

@main.command()
@click.argument('input', type=click.File('r'), required=False, default=None)
@config
def start(config, input):
    """Simple program that greets NAME for a total of COUNT times."""
    dyc = DYC(config.options)
    dyc.start()


@main.command()
@config
def diff(config):
    """This argument will run DYC on DIFF patch only"""
    diff = Diff()
    for index in diff.uncommitted:
        if index.get('diff'):
            diff = index.get('diff')
            name = index.get('name')
            temp_file = '.dyc.{}'.format(name)
            # We have a temp file to get the function name from from and see where to document
            print(index.get('name'), index.get('hunk'))
            # with open(temp_file, 'w+') as temp:
            #     try:
            #         temp.write(index.get('additions'))
            #         temp.seek(0)
            #         config.options['files'] = [temp_file]
            #         dyc = DYC(config.options)
            #         dyc.start()
            #     except:
            #         os.remove(temp_file)
            #         break
