import click
from .parser import Config
from .main import DYC

config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@config
def main(config):
    config.read_config()
    pass

@main.command()
@click.argument('input', type=click.File('r'), required=False, default=None)
@config
def start(config, input):
    """Simple program that greets NAME for a total of COUNT times."""
    dyc = DYC(config.options)
    dyc.start()