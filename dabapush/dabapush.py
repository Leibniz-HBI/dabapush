import click
import sys
import os
import yaml
from pathlib import Path

# import importlib
# from typing import Dict, Literal
# import sys
# from multiprocessing import cpu_count
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# from threading import get_ident, active_count
from loguru import logger as log

from .reader_subcommand import reader
from .writer_subcommand import writer
# from .read import read

@click.group()
@click.option('--logfile', help='file to log in (optional)')
@click.option('--loglevel', default='INFO', help='the level to log, yk')
@click.pass_context
def cli(ctx, logfile, loglevel):
    # prepare log options
    if (logfile != None):
        log.remove()
        if (loglevel == None):
            loglevel = 'DEBUG'
            log.add(sys.stdout, loglevel)
        log.add(logfile, loglevel)
    wd = Path(os.getcwd())
    sd = Path(__file__).parent.parent # arkwardly fetch the package dir

    log.debug(f'Starting DaBaPush in {wd} fom {__file__}')
    
    # prepare context
    ctx.ensure_object(dict)
    ctx.obj['wd'] = wd # store working dir in context
    ctx.obj['sd'] = sd
    with Path(sd/'config.yml').open('r') as file:
        ctx.obj['globconf'] = yaml.safe_load(file)



# CREATE
@cli.command()
@click.pass_context
def create(ctx):
    log.debug(f'Creating project in {ctx.obj["wd"]}')
    prj_name = click.prompt('project name', type=str)
    prj_author = click.prompt('author name (split several authors with ";")', type=str)
    man_config = click.confirm("Should we configure readers and writers?")
    while (man_config == True):
        thing_to_configure = click.prompt('Reader/Writer?', default='Writer')
        if (thing_to_configure != 'Reader' and thing_to_configure != 'Writer'):
            log.debug(f'Try again')
        else:
            if (thing_to_configure == 'Reader'):
                log.debug(f'Configuring a Reader')
            if (thing_to_configure == 'Writer'):
                log.debug(f'Configuring a Reader')
            man_config = click.confirm('do another')


# DISCOVER
@cli.command()
def discover():
    pass

# RUN
@cli.command(help="Run the specified target, if specified target is 'all' all targets are run.")
@click.argument('target')
@click.pass_context
def run(ctx, target):
    log.debug(f'Runrunrun {target} in {ctx.obj["wd"]}')
    pass

@cli.command()
def update():
    pass


cli.add_command(reader)
cli.add_command(writer)



# @click.command()
# @click.argument('input', type=click.Path(exists=True))
# @click.option('--pattern', default='*.json', help='file extension to look for')
# @click.option('--host', default='localhost', help='Host address of the dabase too write to.')
# @click.option('--port', default='5432', help='Host port of the dabase-server.')
# @click.option('--dbname', default='dabapushed', help='Name of the dabase too write to.')
# @click.option('--n_workers', default=cpu_count, help="Number of worker threads to read/write data")
# @click.option('--reader', default='Twacapic', help='python class to read stuff (see docs). Possible values: Twacapic')
# @click.option('--writer', default='CSV',help='python class to write stuff (see docs)')
# @click.option('--recursive', '-r', help='should the reader recurse in subdirectories? Default: TRUE.', is_flag=True)
# @click.option('--logfile', help='file to logi in (optional)')
# @click.option('--loglevel', default='INFO', help='the level to log, yk')
# def run(
#     input: str,
#     pattern: str,
#     reader: str,
#     writer: str,
#     host: str,
#     port: str,
#     dbname: str,
#     n_workers: str,
#     recursive: bool,
#     logfile: str,
#     loglevel: str
# ):
#     # load config
#     config = yaml.load(Path('config.yml').open(), Loader=yaml.FullLoader)
    
#     log.remove()
#     log.add(sys.stdout, level=loglevel)
#     log.debug('Using this configuration', config)
#     # Validate all inputs
#     if logfile is not None:
#         log.add(logfile, level=loglevel, rotation="64 MB")
#         log.add(sys.stderr, level='ERROR')

#     log.add('errors.log', level='ERROR')
#     log.add('warnings.log', level='WARNING')

#     log.info(f'{input}**/*.{pattern} will be written to {host}:{port}/{dbname} with {n_workers} parallel threads')

#     ReaderClass = None
#     # Load the reader/writer:
#     ReaderClass = load_from_config(reader, 'reader', config)
#     WriterClass = load_from_config(writer, 'writer', config)

#     # Fire up the engines and find in all matching files
#     files = read(input, pattern, recursive=recursive)

#     # Get a Writer
#     writerInstance = WriterClass()

#     def proop(thing: Path) -> any:
#         readerInstance = ReaderClass(thing)
#         tid = get_ident()
#         log.debug(f'Reading {thing} with Thread ID: {tid}')
#         return writerInstance.write(readerInstance.read())
        
#     with ThreadPoolExecutor() as executor:
#         # log.debug(f'Starting {active_count()} threads.')
#         lines = executor.map(proop, files)
#         # log.info(f'Read a total of {sum(lines)} records')

# def load_from_config(name: str, key: str, config: Dict):
#     if (name is not None and name in config['plugins'][key].keys()):
#         log.debug(f'Using this {key}: {name}')
#         try:
#             moduleName = config['plugins'][key][name]['moduleName']
#             className = config['plugins'][key][name]['className']
#             ReaderClass = importlib.import_module(moduleName, package='dabapush').__getattribute__(className)
#         except Exception as e:
#             log.error(e)
#     else:
#         log.warning(f'{key.upper()} {name} cannot be found')
#     return ReaderClass
#     # start $n_workers workers to read the data
#     # if JSON accecssor is given, apply it to each loaded file
#     # writer(host, port, dbname)

if __name__ == '__main__':
    cli(obj={})