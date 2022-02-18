---
description: |
    API documentation for modules: dabapush, dabapush.Configuration, dabapush.Configuration.ConfigurationError, dabapush.Configuration.FileWriterConfiguration, dabapush.Configuration.PlugInConfiguration, dabapush.Configuration.ProjectConfiguration, dabapush.Configuration.ReaderConfiguration, dabapush.Configuration.Registry, dabapush.Configuration.WriterConfiguration, dabapush.Dabapush, dabapush.Reader, dabapush.Reader.NDJSONReader, dabapush.Reader.Reader, dabapush.Reader.TwacapicReader, dabapush.Writer, dabapush.Writer.CSVWriter, dabapush.Writer.DBWriter, dabapush.Writer.NDJSONWriter, dabapush.Writer.Writer, dabapush.create_subcommand, dabapush.discover_subcommand, dabapush.main, dabapush.reader_subcommand, dabapush.run_subcommand, dabapush.update_subcommand, dabapush.utils, dabapush.writer_subcommand.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `dabapush` {#id}

Database pusher for social media data (Twitter for the beginning) – pre-alpha version

## Using dabapush

<code>[dabapush](#dabapush "dabapush")</code> is a tool to read longer running data collections and write them to another file format or persist them into a database. It is designed to run periodically, e.g. controlled by chron, thus, for convenience ot use project-based configurations which contain all required information on what to read where and what to do with it.
A **project** may have one or more **jobs**, each job consists of a reader and a writer configuration, e.g. read JSON-files from the Twitter API that we stored in folder `/home/user/fancy-project/twitter/` and write the flattened and compiled data set in to `/some/where/else` as CSV files.

### First steps

In order to run a first <code>[dabapush](#dabapush "dabapush")</code>-job we'll need to create a project configuration. This is done by calling:

```
dabapush create
```

By default this walks you through the configuration process in a step-by-step manner. Alternatively, you could call:

```
dabapush create --non-interactive
```

This will create an empty configuration, you'll have to fill out the required information by e.g. calling:

```
dabapush reader add NDJSON default
dabapush writer add CSV default
```
Whereas <code>reader add</code>/<code>writer add</code> is the verb, <code>NDJSON</code> or <code>CSV</code> is the plugin to add and <code>default</code> is the pipeline name. 

Of course you can edit the configration after creation in your favorite editor, but **BEWARE NOT TO TEMPER WITH THE YAMl-TAGS!!!**.

Although, 


To run the newly configured job, please call:

```
dabapush run default
```

## Command Reference

### Invocation Pattern:

```
dabapush <command> <subcommand?> <options>
```

### Commands:

<code>create</code> -- creates a dabapush project (invokes interactive prompt)

Options:

`--non-interactive`, create an empty configuration and exit

`--interactive`, *this is the default behavior*: prompts for user input on

- project name,
- project authors name,
- project author email address(es) for notifications
- manually configure targets or run discover?

----

<code>run all</code> -- collect all known items and execute targets/destinations

`run <target>` -- run a single writer and/or named target

Options:

`--force-rerun, -r`: forces all data  to be read, ignores already logged data

----

<code>update</code> -- update items for target(s)

`update <target>` or <code>update all</code> -- update the target's files-to-be-read list


----

<code>reader</code> -- interact with readers

`reader configure <name>` -- configure the reader for one or more subproject(s); Reader configuration is inherited from global to local level; throws if configuration is incomplete and defaults are missing

<code>reader list</code>: returns a table of all configured readers, with <path> <target> <class> <id>

<code>reader list\_all</code>: returns a table of all registered reader plugins

`reader add <type> <name>`: add a reader to the project configuration

Options:

`--input-directory <path>`: directory to be read

`--pattern <pattern>`: pattern for matching file names against.

`remove <name>`: remove a reader from the project configuration.

`register <path>`: not there yet

----

<code>discover</code> -- discover (possible) targtets in project directory and configure them automagically -- yeah, you dream of that, don't you?

----

<code>writer</code> -- interact with writers

`writer add <type> <name>`: 

`writer remove <name>`: removes the writer for the given name

<code>writer list</code> -- returns table of all writers, with <path> <subproject-name> <class> <id>

<code>writer list\_all</code>: returns a table of all registered writer plugins

`writer configure <name>` or <code>writer configure all</code>

Options:

`--output-dir, -o <path>`: default for all targets: `<project-dir>/output/<target-name>`

`--output-pattern, -p <pattern>`: pattern used for file name creation e.g. 'YYYY-MM-dd', file extension is added by the writer and cannot be overwritten

`--roll-over, -r `<file-size>:

`--roll-over, -r` <lines>: 

`--roll-over -r <None>`: should be the output chunked? Give either a file-size or a number of lines for roll-over or None to disable chunking

`writer register <path> <class-name>`: something for the roadmap.

`deregister <name> <registry-name>`: something for the roadmap.

## Programmatic documention


## Extending dabapush and developers guide

### dabapush's Approach to Projects and Configuration

### Class References

| **Dabapush** |     |
| ------------ | --- |
|              |     |
|              |     |
|              |     |
|              |     |

| **Reader** |     |
| ---------- | --- |
|            |     |
|            |     |
|            |     |
|            |     |

| **Writer** |     |
| ---------- | --- |
|            |     |
|            |     |
|            |     |
|            |     |

| **Configuration** |     |
|                   |     |
| ----------------- | --- |
|                   |     |
|                   |     |
|                   |     |
|                   |     |

### Developer Installation

1. Install [poetry](https://python-poetry.org/docs/#installation).
2. Clone repository.
3. In the cloned repository's root directory run <code>poetry install</code>.
4. Run <code>poetry shell</code> to start development virtualenv.
5. Run <code>[dabapush](#dabapush "dabapush") create</code> to create your first project.
6. Run <code>pytest</code> to run all tests.
## 7. Run `pdoc --http localhost:8080 dabapush` to locally serve this documentation.


Contact: smo (ät) leibniz-hbi.de


    
## Sub-modules

* [dabapush.Configuration](#dabapush.Configuration)
* [dabapush.Dabapush](#dabapush.Dabapush)
* [dabapush.Reader](#dabapush.Reader)
* [dabapush.Writer](#dabapush.Writer)
* [dabapush.create_subcommand](#dabapush.create_subcommand)
* [dabapush.discover_subcommand](#dabapush.discover_subcommand)
* [dabapush.main](#dabapush.main)
* [dabapush.reader_subcommand](#dabapush.reader_subcommand)
* [dabapush.run_subcommand](#dabapush.run_subcommand)
* [dabapush.update_subcommand](#dabapush.update_subcommand)
* [dabapush.utils](#dabapush.utils)
* [dabapush.writer_subcommand](#dabapush.writer_subcommand)






    
# Module `dabapush.Configuration` {#id}




    
## Sub-modules

* [dabapush.Configuration.ConfigurationError](#dabapush.Configuration.ConfigurationError)
* [dabapush.Configuration.FileWriterConfiguration](#dabapush.Configuration.FileWriterConfiguration)
* [dabapush.Configuration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration)
* [dabapush.Configuration.ProjectConfiguration](#dabapush.Configuration.ProjectConfiguration)
* [dabapush.Configuration.ReaderConfiguration](#dabapush.Configuration.ReaderConfiguration)
* [dabapush.Configuration.Registry](#dabapush.Configuration.Registry)
* [dabapush.Configuration.WriterConfiguration](#dabapush.Configuration.WriterConfiguration)






    
# Module `dabapush.Configuration.ConfigurationError` {#id}







    
## Classes


    
### Class `ConfigurationError` {#id}




>     class ConfigurationError(
>         *args: object
>     )





    
#### Ancestors (in MRO)

* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `dabapush.Configuration.FileWriterConfiguration` {#id}







    
## Classes


    
### Class `FileWriterConfiguration` {#id}




>     class FileWriterConfiguration(
>         name,
>         id=None,
>         chunk_size: int = 2000,
>         path: str = '.',
>         name_template: str = '${date}_${time}_${name}.${type}'
>     )


Abstract class describing configuration items for a file based writer


    
#### Ancestors (in MRO)

* [dabapush.Configuration.WriterConfiguration.WriterConfiguration](#dabapush.Configuration.WriterConfiguration.WriterConfiguration)
* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)


    
#### Descendants

* [dabapush.Writer.CSVWriter.CSVWriterConfiguration](#dabapush.Writer.CSVWriter.CSVWriterConfiguration)
* [dabapush.Writer.NDJSONWriter.NDJSONWriterConfiguration](#dabapush.Writer.NDJSONWriter.NDJSONWriterConfiguration)





    
#### Methods


    
##### Method `make_file_name` {#id}




>     def make_file_name(
>         self,
>         additional_keys: dict = {}
>     ) ‑> str


Parameters
-----
additional_keys :
    dict:  (Default value = {})
additional_keys :
    dict:  (Default value = {})
**```additional_keys```** :&ensp;`dict :`
:   (Default value = {})

Returns
-------

    
##### Method `set_name_template` {#id}




>     def set_name_template(
>         self,
>         template: str
>     )


Parameters
-----
template :
    str:
template :
    str:
**```template```** :&ensp;`str :`
:   &nbsp;

Returns
-------



    
# Module `dabapush.Configuration.PlugInConfiguration` {#id}







    
## Classes


    
### Class `PlugInConfiguration` {#id}




>     class PlugInConfiguration(
>         name: str,
>         id: str
>     )





    
#### Ancestors (in MRO)

* [yaml.YAMLObject](#yaml.YAMLObject)


    
#### Descendants

* [dabapush.Configuration.ReaderConfiguration.ReaderConfiguration](#dabapush.Configuration.ReaderConfiguration.ReaderConfiguration)
* [dabapush.Configuration.WriterConfiguration.WriterConfiguration](#dabapush.Configuration.WriterConfiguration.WriterConfiguration)


    
#### Class variables


    
##### Variable `yaml_tag` {#id}








    
#### Static methods


    
##### `Method get_instance` {#id}




>     def get_instance() ‑> Reader







    
# Module `dabapush.Configuration.ProjectConfiguration` {#id}







    
## Classes


    
### Class `ProjectConfiguration` {#id}




>     class ProjectConfiguration(
>         readers: Dict[str, dabapush.Configuration.ReaderConfiguration.ReaderConfiguration] = {},
>         writers: Dict[str, dabapush.Configuration.WriterConfiguration.WriterConfiguration] = {},
>         author: str = '',
>         name: str = ''
>     )


ProjectConfiguration hold necessary configuration informations


A ProjectConfiguration is for reading and writing data as well as the project's meta data
e.g. author name(s) and email addresses.

#### Parameters


#### Returns


`Initialize a ProjectConfiguration with optional reader and/or writer dicts`
:   &nbsp;




    
#### Ancestors (in MRO)

* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}









    
#### Methods


    
##### Method `add_reader` {#id}




>     def add_reader(
>         self,
>         type: str,
>         name: str
>     ) ‑> None


add a reader configuration to the project

###### Parameters

type :
    str: registry of the configuration to add
name :
    str: name of the configuration to add
    Returns: Nothing.
type :
    str:
name :
    str:
type :
    str:
name :
    str:
**```type```** :&ensp;`str :`
:   &nbsp;


**```name```** :&ensp;`str :`
:   &nbsp;

###### Returns


###### Raises

<code>ConfigurationError</code>
:   if no local or global configurations are found



    
##### Method `add_writer` {#id}




>     def add_writer(
>         self,
>         type: str,
>         name: str
>     ) ‑> None


Parameters
-----
type :
    str:
name :
    str:
    Returns: None: nothing to see, carry on.
type :
    str:
name :
    str:
type :
    str:
name :
    str:
**```type```** :&ensp;`str :`
:   &nbsp;


**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `list_readers` {#id}




>     def list_readers(
>         self
>     ) ‑> List[dict]


list all configured readers

Returns: List[Dict]: list of dicts with name- and id-fields

###### Parameters


Returns
-------

    
##### Method `list_writers` {#id}




>     def list_writers(
>         self
>     )


list all configured writers

Returns: List[Dict]: list of dicts with name- and id-fields

###### Parameters


Returns
-------

    
##### Method `remove_reader` {#id}




>     def remove_reader(
>         self,
>         name: str
>     ) ‑> None


remove a reader from the configuration

###### Parameters

name :
    str: name of the reader to be removed
    Returns: Nada.
name :
    str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `remove_writer` {#id}




>     def remove_writer(
>         self,
>         name: str
>     )


Parameters
-----
name :
    str:
name :
    str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `set_author` {#id}




>     def set_author(
>         self,
>         author
>     )


Parameters
-----
author :
    

Returns
-------

    
##### Method `set_name` {#id}




>     def set_name(
>         self,
>         name
>     )


Parameters
-----
name :
    

Returns
-------



    
# Module `dabapush.Configuration.ReaderConfiguration` {#id}







    
## Classes


    
### Class `ReaderConfiguration` {#id}




>     class ReaderConfiguration(
>         name,
>         id,
>         read_path: str,
>         pattern: str
>     )





    
#### Ancestors (in MRO)

* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)


    
#### Descendants

* [dabapush.Reader.NDJSONReader.NDJSONReaderConfiguration](#dabapush.Reader.NDJSONReader.NDJSONReaderConfiguration)
* [dabapush.Reader.TwacapicReader.TwacapicReaderConfiguration](#dabapush.Reader.TwacapicReader.TwacapicReaderConfiguration)


    
#### Class variables


    
##### Variable `yaml_tag` {#id}











    
# Module `dabapush.Configuration.Registry` {#id}







    
## Classes


    
### Class `Registry` {#id}




>     class Registry(
>         readers: Dict[str, str] = {},
>         writers: Dict[str, str] = {}
>     )





    
#### Ancestors (in MRO)

* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}








    
#### Static methods


    
##### `Method get_reader` {#id}




>     def get_reader(
>         type: str
>     ) ‑> dabapush.Configuration.ReaderConfiguration.ReaderConfiguration


Parameters
-----
type :
    str: registry key
    Returns: ReaderConfiguration or None: the requested ReaderConfiguration or None if
    no matching configuration is found.
type :
    str:
type :
    str:
**```type```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### `Method get_writer` {#id}




>     def get_writer(
>         type: str
>     ) ‑> dabapush.Configuration.WriterConfiguration.WriterConfiguration


Parameters
-----
type :
    str:
type :
    str:
type :
    str:
**```type```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### `Method list_all_readers` {#id}




>     def list_all_readers() ‑> List[str]




    
##### `Method list_all_writers` {#id}




>     def list_all_writers() ‑> List[str]





    
#### Methods


    
##### Method `list_writers` {#id}




>     def list_writers(
>         self
>     ) ‑> List[str]




    
##### Method `register_reader` {#id}




>     def register_reader(
>         self,
>         name: str,
>         plugin_configuration
>     ) ‑> None


Parameters
-----
name :
    str:
constructor :
    param name: str:
plugin_configuration :
    param name: str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `register_writer` {#id}




>     def register_writer(
>         self,
>         name: str,
>         constructor
>     ) ‑> None


Parameters
-----
name :
    str:
constructor :
    param name: str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `remove_reader` {#id}




>     def remove_reader(
>         self,
>         name: str
>     ) ‑> bool


Parameters
-----
name :
    str:
name :
    str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `remove_writer` {#id}




>     def remove_writer(
>         self,
>         name: str
>     ) ‑> bool


Parameters
-----
name :
    str:
name :
    str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------



    
# Module `dabapush.Configuration.WriterConfiguration` {#id}







    
## Classes


    
### Class `WriterConfiguration` {#id}




>     class WriterConfiguration(
>         name,
>         id=None,
>         chunk_size: int = 2000
>     )





    
#### Ancestors (in MRO)

* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)


    
#### Descendants

* [dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration](#dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration)


    
#### Class variables


    
##### Variable `yaml_tag` {#id}











    
# Module `dabapush.Dabapush` {#id}







    
## Classes


    
### Class `Dabapush` {#id}




>     class Dabapush(
>         install_dir: pathlib.Path = PosixPath('/home/philippkessling/repos/dabapush'),
>         working_dir: pathlib.Path = PosixPath('/home/philippkessling/repos/dabapush')
>     )


This is the main class for this application.

It is a Singleton pattern class and follows the interface pattern as well.

#### Parameters


Returns
-------







    
#### Methods


    
##### Method `gc_load` {#id}




>     def gc_load(
>         self
>     )


load the global registry and configuration

    
##### Method `jb_run` {#id}




>     def jb_run(
>         self,
>         targets: list
>     )


runs the job(s) configured in the current directory

###### Parameters

targets :
    list[str]:
targets :
    list[str]:
**```targets```** :&ensp;`list[str] :`
:   &nbsp;

Returns
-------

    
##### Method `jb_update` {#id}




>     def jb_update(
>         self
>     )


update the current job's targets

    
##### Method `pr_init` {#id}




>     def pr_init(
>         self
>     )


Initialize a new project in the current directory

    
##### Method `pr_read` {#id}




>     def pr_read(
>         self
>     ) ‑> bool


Read the project configuration file in the current directory

###### Parameters


###### Returns

<code>type</code>
:   bool Indicates wether loading load successful



    
##### Method `pr_write` {#id}




>     def pr_write(
>         self
>     )


Write the current configuration to the project configuration file in the current directory

    
##### Method `rd_add` {#id}




>     def rd_add(
>         self,
>         reader: str,
>         name: str
>     )


add a reader to the current project

###### Parameters

reader :
    str:
name :
    str:
reader :
    str:
name :
    str:
**```reader```** :&ensp;`str :`
:   &nbsp;


**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `rd_list` {#id}




>     def rd_list(
>         self
>     )


Lists all available readers

    
##### Method `rd_rm` {#id}




>     def rd_rm(
>         self
>     )


remove a reader from the current configuration

    
##### Method `rd_update` {#id}




>     def rd_update(
>         self
>     )


update a reader's configuration

    
##### Method `update_reader_targets` {#id}




>     def update_reader_targets(
>         self,
>         name: str
>     ) ‑> None


Parameters
-----
name :
    str:
name :
    str:
**```name```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
##### Method `wr_add` {#id}




>     def wr_add(
>         self
>     )


add a reader to the current project

    
##### Method `wr_list` {#id}




>     def wr_list(
>         self
>     )


Lists all available readers

    
##### Method `wr_rm` {#id}




>     def wr_rm(
>         self
>     )


remove a reader from the current configuration

    
##### Method `wr_update` {#id}




>     def wr_update(
>         self
>     )


update a reader's configuration



    
# Module `dabapush.Reader` {#id}




    
## Sub-modules

* [dabapush.Reader.NDJSONReader](#dabapush.Reader.NDJSONReader)
* [dabapush.Reader.Reader](#dabapush.Reader.Reader)
* [dabapush.Reader.TwacapicReader](#dabapush.Reader.TwacapicReader)






    
# Module `dabapush.Reader.NDJSONReader` {#id}







    
## Classes


    
### Class `NDJSONReader` {#id}




>     class NDJSONReader(
>         config: NDJSONReaderConfiguration
>     )





    
#### Ancestors (in MRO)

* [dabapush.Reader.Reader.Reader](#dabapush.Reader.Reader.Reader)
* [abc.ABC](#abc.ABC)






    
#### Methods


    
##### Method `read` {#id}




>     def read(
>         self
>     ) ‑> Generator[<built-in function any>, <built-in function any>, <built-in function any>]


reads multiple ndjson files and emits them line by line

    
### Class `NDJSONReaderConfiguration` {#id}




>     class NDJSONReaderConfiguration(
>         name,
>         id=None,
>         read_path: str = '.',
>         pattern: str = '*.ndjson',
>         flatten_dicts=True
>     )





    
#### Ancestors (in MRO)

* [dabapush.Configuration.ReaderConfiguration.ReaderConfiguration](#dabapush.Configuration.ReaderConfiguration.ReaderConfiguration)
* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}









    
#### Methods


    
##### Method `get_instance` {#id}




>     def get_instance(
>         self
>     ) ‑> dabapush.Reader.NDJSONReader.NDJSONReader






    
# Module `dabapush.Reader.Reader` {#id}







    
## Classes


    
### Class `Reader` {#id}




>     class Reader(
>         config: dabapush.Configuration.ReaderConfiguration.ReaderConfiguration
>     )


Abstract base class for all reader plugins. BEWARE: readers and writers are never
to be instanced directly by the user but rather will be obtain by calling
<code>get\_instance()</code> on their specific Configuration-counterparts.

#### Parameters


Returns
-------


    
#### Ancestors (in MRO)

* [abc.ABC](#abc.ABC)


    
#### Descendants

* [dabapush.Reader.NDJSONReader.NDJSONReader](#dabapush.Reader.NDJSONReader.NDJSONReader)
* [dabapush.Reader.TwacapicReader.TwacapicReader](#dabapush.Reader.TwacapicReader.TwacapicReader)





    
#### Methods


    
##### Method `read` {#id}




>     def read(
>         self
>     )






    
# Module `dabapush.Reader.TwacapicReader` {#id}







    
## Classes


    
### Class `TwacapicReader` {#id}




>     class TwacapicReader(
>         config: ReaderConfiguration
>     )


Reader to read ready to read Twitter json data


    
#### Ancestors (in MRO)

* [dabapush.Reader.Reader.Reader](#dabapush.Reader.Reader.Reader)
* [abc.ABC](#abc.ABC)






    
#### Methods


    
##### Method `read` {#id}




>     def read(
>         self
>     ) ‑> Generator[<built-in function any>, <built-in function any>, <built-in function any>]


reads the configured path a returns a generator of single posts

    
### Class `TwacapicReaderConfiguration` {#id}




>     class TwacapicReaderConfiguration(
>         name,
>         id=None,
>         read_path: str = None,
>         pattern: str = '*.json'
>     )


Reader configuration for reading Twacapic's Twitter JSON files.


    
#### Ancestors (in MRO)

* [dabapush.Configuration.ReaderConfiguration.ReaderConfiguration](#dabapush.Configuration.ReaderConfiguration.ReaderConfiguration)
* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}









    
#### Methods


    
##### Method `get_instance` {#id}




>     def get_instance(
>         self
>     ) ‑> dabapush.Reader.TwacapicReader.TwacapicReader






    
# Module `dabapush.Writer` {#id}




    
## Sub-modules

* [dabapush.Writer.CSVWriter](#dabapush.Writer.CSVWriter)
* [dabapush.Writer.DBWriter](#dabapush.Writer.DBWriter)
* [dabapush.Writer.NDJSONWriter](#dabapush.Writer.NDJSONWriter)
* [dabapush.Writer.Writer](#dabapush.Writer.Writer)






    
# Module `dabapush.Writer.CSVWriter` {#id}







    
## Classes


    
### Class `CSVWriter` {#id}




>     class CSVWriter(
>         config: CSVWriterConfiguration
>     )





    
#### Ancestors (in MRO)

* [dabapush.Writer.Writer.Writer](#dabapush.Writer.Writer.Writer)






    
#### Methods


    
##### Method `persist` {#id}




>     def persist(
>         self
>     )




    
### Class `CSVWriterConfiguration` {#id}




>     class CSVWriterConfiguration(
>         name,
>         id=None,
>         chunk_size: int = 2000,
>         path: str = '.',
>         name_template: str = '${date}_${time}_${name}_${chunk_number}.${type}'
>     )





    
#### Ancestors (in MRO)

* [dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration](#dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration)
* [dabapush.Configuration.WriterConfiguration.WriterConfiguration](#dabapush.Configuration.WriterConfiguration.WriterConfiguration)
* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}







    
#### Instance variables


    
##### Variable `file_path` {#id}



Type: `pathlib.Path`





    
#### Methods


    
##### Method `get_instance` {#id}




>     def get_instance(
>         self
>     )






    
# Module `dabapush.Writer.DBWriter` {#id}







    
## Classes


    
### Class `DBWriter` {#id}




>     class DBWriter





    
#### Ancestors (in MRO)

* [dabapush.Writer.Writer.Writer](#dabapush.Writer.Writer.Writer)






    
#### Methods


    
##### Method `persist` {#id}




>     def persist(
>         self,
>         chunkSize: int
>     )


Parameters
-----
chunkSize :
    int:
chunkSize :
    int:
**```chunkSize```** :&ensp;`int :`
:   &nbsp;

Returns
-------



    
# Module `dabapush.Writer.NDJSONWriter` {#id}







    
## Classes


    
### Class `NDJSONWriter` {#id}




>     class NDJSONWriter(
>         config: NDJSONWriterConfiguration
>     )





    
#### Ancestors (in MRO)

* [dabapush.Writer.Writer.Writer](#dabapush.Writer.Writer.Writer)






    
#### Methods


    
##### Method `persist` {#id}




>     def persist(
>         self
>     )




    
### Class `NDJSONWriterConfiguration` {#id}




>     class NDJSONWriterConfiguration(
>         name,
>         id=None,
>         chunk_size: int = 2000,
>         path: str = '.',
>         name_template: str = '${date}_${time}_${name}.${type}'
>     )





    
#### Ancestors (in MRO)

* [dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration](#dabapush.Configuration.FileWriterConfiguration.FileWriterConfiguration)
* [dabapush.Configuration.WriterConfiguration.WriterConfiguration](#dabapush.Configuration.WriterConfiguration.WriterConfiguration)
* [dabapush.Configuration.PlugInConfiguration.PlugInConfiguration](#dabapush.Configuration.PlugInConfiguration.PlugInConfiguration)
* [yaml.YAMLObject](#yaml.YAMLObject)



    
#### Class variables


    
##### Variable `yaml_tag` {#id}









    
#### Methods


    
##### Method `get_instance` {#id}




>     def get_instance(
>         self
>     )






    
# Module `dabapush.Writer.Writer` {#id}







    
## Classes


    
### Class `Writer` {#id}




>     class Writer(
>         config: dabapush.Configuration.WriterConfiguration.WriterConfiguration
>     )






    
#### Descendants

* [dabapush.Writer.CSVWriter.CSVWriter](#dabapush.Writer.CSVWriter.CSVWriter)
* [dabapush.Writer.DBWriter.DBWriter](#dabapush.Writer.DBWriter.DBWriter)
* [dabapush.Writer.NDJSONWriter.NDJSONWriter](#dabapush.Writer.NDJSONWriter.NDJSONWriter)



    
#### Instance variables


    
##### Variable `id` {#id}






    
##### Variable `name` {#id}








    
#### Methods


    
##### Method `persist` {#id}




>     def persist(
>         self
>     ) ‑> None




    
##### Method `write` {#id}




>     def write(
>         self,
>         queue: Generator[<built-in function any>, <built-in function any>, <built-in function any>]
>     )


Parameters
-----
df :
    dict
queue :
    Generator[any:
any :
    param any]:
queue :
    Generator[any:
**```queue```** :&ensp;`Generator[any :`
:   &nbsp;


any] :
    

Returns
-------



    
# Module `dabapush.create_subcommand` {#id}









    
# Module `dabapush.discover_subcommand` {#id}









    
# Module `dabapush.main` {#id}









    
# Module `dabapush.reader_subcommand` {#id}









    
# Module `dabapush.run_subcommand` {#id}

Some module documentation







    
# Module `dabapush.update_subcommand` {#id}









    
# Module `dabapush.utils` {#id}






    
## Functions


    
### Function `flatten` {#id}




>     def flatten(
>         thing: dict,
>         namespace: str = None,
>         sep: str = '.'
>     ) ‑> dict


Flattens a nested array, flattened keys are joined together with the specified seperator.

###### Parameters

thing :
    dict: Nested dict to flatten
namespace :
    str:  (Default value = None)
sep :
    str:  (Default value = '.')
**```thing```** :&ensp;`dict :`
:   &nbsp;


**```namespace```** :&ensp;`str :`
:   (Default value = None)


**```sep```** :&ensp;`str :`
:   (Default value = '.')

###### Returns

<code>type</code>
:   dict: the flattened dict



    
### Function `join` {#id}




>     def join(
>         id: str,
>         includes: list,
>         id_key: str
>     ) ‑> <built-in function any>


looks up an entity in a array of dicts by given key.

###### Parameters

id :
    str:
includes :
    list[any]:
id_key :
    str:
id :
    str:
includes :
    list[any]:
id_key :
    str:
**```id```** :&ensp;`str :`
:   &nbsp;


**```includes```** :&ensp;`list[any] :`
:   &nbsp;


**```id_key```** :&ensp;`str :`
:   &nbsp;

Returns
-------

    
### Function `safe_access` {#id}




>     def safe_access(
>         thing: dict,
>         path: list
>     )


Parameters
-----
thing :
    dict:
path :
    list[str]:
thing :
    dict:
path :
    list[str]:
**```thing```** :&ensp;`dict :`
:   &nbsp;


**```path```** :&ensp;`list[str] :`
:   &nbsp;

Returns
-------




    
# Module `dabapush.writer_subcommand` {#id}








-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
