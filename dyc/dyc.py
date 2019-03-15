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
    # print(config)
    dyc = DYC(config.plain)
    dyc.prepare()
    dyc.process_methods()


@main.command()
@config
def diff(config):
    """This argument will run DYC on DIFF patch only"""
    diff = Diff(config.plain)
    uncommitted = diff.uncommitted
    paths = [idx.get('path') for idx in uncommitted]
    if len(uncommitted):
        dyc = DYC(config.plain)
        dyc.prepare(files=paths)
        dyc.process_methods(diff_only=True, changes=uncommitted)
