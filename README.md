# dabapush

Database pusher for social media data (Twitter for the beginning) – pre-alpha version

## Using dabapush

`dabapush` is a tool to read longer running data collections and write them to another file format or persist them into a database. It is designed to run periodically, e.g. controlled by chron, thus, for convenience ot use project-based configurations which contain all required information on what to read where and what to do with it.
A **project** may have one or more **jobs**, each job consists of a reader and a writer configuration, e.g. read JSON-files from the Twitter API that we stored in folder `/home/user/fancy-project/twitter/` and write the flattened and compiled data set in to `/some/where/else` as CSV files.

### First steps

In order to run a first `dabapush`-job we'll need to create a project configuration. This is done by calling:

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
Whereas `reader add`/`writer add` is the verb, `NDJSON` or `CSV` is the plugin to add and `default` is the pipeline name. 

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

`create` -- creates a dabapush project (invokes interactive prompt)

Options:

`--non-interactive`, create an empty configuration and exit

`--interactive`, *this is the default behavior*: prompts for user input on

- project name,
- project authors name,
- project author email address(es) for notifications
- manually configure targets or run discover?

----

`run all` -- collect all known items and execute targets/destinations

`run <target>` -- run a single writer and/or named target

Options:

`--force-rerun, -r`: forces all data  to be read, ignores already logged data

----

`update` -- update items for target(s)

<subproject>

<subproject/writer>

<target>

all

----

`reader` -- interact with readers

`reader configure <name>` -- configure the reader for one or more subproject(s); Reader configuration is inherited from global to local level; throws if configuration is incomplete and defaults are missing

`reader list`: returns a table of all configured readers, with <path> <subproject-name> <class> <id>

`reader list_all`: returns a table of all registered reader plugins

`reader add <type> <name>`: add a reader to the project configuration

Options:

`--input-directory <path>`: directory to be read

`--pattern <pattern>`: pattern for matching file names against.

`remove <name>`: remove a reader from the project configuration.

`register <path>`: not there yet

----

`discover` -- discover (possible) targtets in project directory and configure them automagically

----

writer -- configure writer(s)

add <path> <subproject-name> <plugin-name>: 

remove <id> or <path>: removes the writer for given id or all writers for given path

list -- returns table of all writers, with <path> <subproject-name> <class> <id>

list available: returns a table of all registered writer plugins

configure <writer-id> <subproject/name>

configure all

--output-dir -o <path>: default for all targets: <project-dir>/output/<target-name>

--output-pattern -p <pattern>: pattern uesd for file name creation e.g. 'YYYY-MM-dd', file extension is added by the writer and cannot be overwritten

--roll-over -r <file-size>:

--roll-over -r <lines>: 

--roll-over -r <None>: should be the output chunked? Give either a file-size or a number of lines for roll-over or None to disable chunking

register <path> <class-name> <registry-name>

deregister <path> <registry-name>

## Programmtic documention


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

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone repository
3. In the cloned repository's root directory run `poetry install`
4. Run `poetry shell` to start development virtualenv
5. Run `dabapush create` to create your first project.
6. Run `pytest` to run all tests
