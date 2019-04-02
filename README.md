# Document Your Code

DYC is a CLI tool that helps with documenting your source code. Answer `dyc` prompts and it will append docstrings to your code with keeping a consistent pattern of docstrings.

    * Keep your Docstrings consistent.
    * Document your DIFF patch.
    * Ease of helping other developers understand your code.

## Tech

* [Python 2.7](https://www.python.org/download/releases/2.7/)


## Installation

```
$ pip install document-your-code
```

## Usage

To run on all files in a project. Run

```sh
$ dyc start
```

To run on a Git Diff patch. Run

```sh
$  dyc diff
```

### Example

```sh
$ cd myapp/
$ touch example.py
```

```python
# example.py

def hello(name):
    return "Hello " + name
```

```sh
$ dyc start

Processing Methods

Do you want to document method hello? [y/N]: y

(hello) Method docstring : DYC Greets you

(name) Argument docstring : your name
(name) Argument type : str
```

```vim
## CONFIRM: MODIFY DOCSTRING BETWEEN START AND END LINES ONLY

def hello(name):
    ## START
    """
    DYC Greets you
    Parameters
    ----------
    str name: your name
    """
    ## END
    return "Hello " + name
~
~
~
```

```sh
$ cat example.py

def hello(name):
    """
    DYC Greets you
    Parameters
    ----------
    str name: your name
    """
    return "Hello " + name%
```

## API

TODO


## License

MIT ©