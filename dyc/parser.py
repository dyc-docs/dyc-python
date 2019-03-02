"""
This file is used to read the 
`.dyc` configurations at the root of a project.

It parses all the configs to be consumed in DYC.
"""
import copy
import click
from .configs import Config
from exceptions import DYCConfigurationSetup

class ParsedConfig(Config):
    def __init__(self):
        self.plain = copy.deepcopy(self.default)
        try:
            self.override()
        except AttributeError:
            click.echo(click.style('`dyc.yaml` Missing or Incorrectly formatted. USING defaults', fg='cyan'))
