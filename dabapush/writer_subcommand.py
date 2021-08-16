import click

# Writer
@click.group()
def writer():
    pass

@writer.command()
def add():
    pass

@writer.command()
def remove():
    pass

@writer.command()
def list():
    pass

@writer.command()
def configure():
    pass

@writer.command()
def register():
    pass
