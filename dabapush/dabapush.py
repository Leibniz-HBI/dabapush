import click


@click.command()
@click.option('--name', default='friend', help="Your name")
def run(name):
    print(f"Hello {name}")


if __name__ == '__main__':
    run()