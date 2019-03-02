import os
import click
import tempfile
from .parser import ParsedConfig
from .main import DYC
from diff import Diff

config = click.make_pass_decorator(ParsedConfig, ensure=True)

@click.group()
@config
def main(config):
    pass

@main.command()
@click.argument('input', type=click.File('r'), required=False, default=None)
@config
def start(config, input):
    """Simple program that greets NAME for a total of COUNT times."""
    dyc = DYC(config.plain)
    dyc.prepare()
    dyc.process_methods()
    # dyc.process_classes()
    # dyc.process_top()
    # dyc.start()


@main.command()
@config
def diff(config):
    """This argument will run DYC on DIFF patch only"""
    diff = Diff(config.plain)
    for index in diff.uncommitted:
        print(index)
    #     if index.get('diff'):
    #         diff = index.get('diff')
    #         name = index.get('name')
    #         temp_file = '.dyc.{}'.format(name)
    #         dyc = DYC.candidates(index.get('path'), index.get('additions'))
    #         dyc.prompts()
    #         dyc.apply()
