import click

# Reader
@click.group()
@click.pass_context
def reader(ctx):
    print('I will read you stuff')

@reader.command()
def add():
    print('I will add a entity that reads stuff to you!')

@reader.command()
def remove():
    pass

@reader.command(help="lists all available reader plugins")
@click.pass_context
def list(ctx):
    readers = ctx.obj['globconf']['plugins']['reader']
    for key in readers:
        o = readers[key]
        click.echo(f'- {key}:\t{o["description"] if "description" in o else ""}')

@reader.command()
def configure():
    pass

@reader.command()
def register():
    pass
