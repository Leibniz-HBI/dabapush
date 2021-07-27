import click


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--host', default='localhost', help='Host address of the dabase too write to.')
@click.option('--port', default='5432', help='Host port of the dabase-server.')
@click.option('--dbname', default='dabapushed', help='Name of the dabase too write to.')
@click.option('--n_workers', default='4', help="Number of worker threads to read/write data")
def run(input, host, port, dbname, n_workers):
    # List all of the files in dir
    # start $n_workers workers to read the data
    # if JSON accecssor is given, apply it to each loaded file
    print(f'{input} will be written to {host}:{port}/{dbname} with {n_workers} parallel threads')



if __name__ == '__main__':
    run()