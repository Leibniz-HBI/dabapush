from logging import ERROR
from pathlib import Path
import importlib
import click
import sys
import yaml
import multiprocessing.dummy as mp
from multiprocessing import cpu_count
from loguru import logger as log

from .read import read
from .writer import writer

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--host', default='localhost', help='Host address of the dabase too write to.')
@click.option('--port', default='5432', help='Host port of the dabase-server.')
@click.option('--dbname', default='dabapushed', help='Name of the dabase too write to.')
    # load config
    config = yaml.load(Path('config.yml').open(), Loader=yaml.FullLoader)
    
    log.debug('Using this configuration', config)
    
    # start $n_workers workers to read the data
    # if JSON accecssor is given, apply it to each loaded file
    print(f'{input} will be written to {host}:{port}/{dbname} with {n_workers} parallel threads')



if __name__ == '__main__':
    run()