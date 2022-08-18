# ƎƧЯƎVƎЯ
Quickly reverse binaries using ghidra.

Welcome to the esrever documentation.

**warning:** This is a very much alpha version.

## Installation

This package is not yet available on the pypi package index, so for now you'll have to install it through pip+git,
but following the developer instructions below is recommended.
```console
pip install git@github.com:infosec-garage/esrever.git
```

### For developers

You can install an editable version of esrever by cloning this repository locally
and then from within the repository root run:

```bash
pip install -e .[dev]
```
This will make the package available to the (virtual) python environment,
while all project dependencies and an associated toolset that is used for development (type checking, code style...)
is included, as well as packages used for running the unit tests.

Running unit tests locally before committing is recommended,
this can be done by running `pytest -v` in the root of the repository.

## API Documentation

Auto-generated API documentation is _or rather, will be_ available at https://pages.github.com/infosec-garage/esrever


## Sample usage

Quickly reverse binaries using ghidra

```console
hunter@forest:~$ esrever decompile evil.dll
```

```console
hunter@forest:~$ esrever --help
Usage: esrever [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  decompile  Reverse a set of binary files with Ghidra.
```
