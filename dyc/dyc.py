import click


@click.group()
def main():
    print('Passing Here first')
    pass

@main.command()
@click.option("--count", default=1, help="Number of greetings.")
def test(count):
    """Simple program that greets NAME for a total of COUNT times."""
    print('Then Here')
    # MARKER = '# Everything below is ignored\n'
    # message = click.edit('\n\n' + MARKER)
    # if message is not None:
    #     return message.split(MARKER, 1)[0].rstrip('\n')