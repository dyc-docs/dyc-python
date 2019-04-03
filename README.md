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

## Method Docstring Options

*You can also Setup your own customized Docstring Method Formatting in `dyc.yaml` within `formats` key*


*Methods*

|          Key              |                                                       Description                                                           | Type |
|:---------------------:    |:-----------------------------------------------------------------------------------------------------------------------:    |------|
|         ignore            |                                     Known method Names to be ignored from Docstrings                                        | list |
|        keywords           |                            The necessary keyword to search for in a line the triggers actions                               | list |
|        enabled            |                                   Determine if formatting is enabled for the extension                                      | bool |
|         indent            |                         Indentation in a method. Limited options ['tab', '2 spaces', '4 spaces']                            | str  |
|     indent_content        |                              Confirm if the content of a docstring has to be indented aswel                                 | bool |
|          open             |                                             Starting opener text of a method                                                | str  |
|         close             | Close text of a method. This could be the same as opened, but not all languages opening and closing docstrings are same     | str  |
|    break_after_open       |                             Do we add a new line after adding the open strings of a method?                                 | bool |
| break_after_docstring     |                                     Do we add a new line after adding the docstring?                                        | bool |
|   break_before_close      |                                   Add a new line before closing docstrings on a method                                      | bool |
|     words_per_line        |                                         How many words do we add per docstring?                                             | int  |
|      within_scope         |              Should the docstring be within the scope of the method or out? Just like JS Method docstrings                  | bool |


*Arguments*

|    Key        |                  Description                      | Type  |
|:---------:    |:---------------------------------------------:    |:----: |
|   title       |    A title for arguments. i.e: "Parameters"       |  str  |
| underline     |              Underline the title                  | bool  |
|  add_type     | If true, it will prompt for the argument type     | bool  |
|   inline      |   Add docstrings all inline or break within.      | bool  |
|   ignore      |              Arguments to ignore.                 | list  |
|   prefix      |            A prefix like "@param".                |  str  |

## Classes Docstring Options

// TODO

## Top of file Options

// TODO

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

(name) Argument docstring : John Smith
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
    str name: John Smith
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
    str name: John Smith
    """
    return "Hello " + name%
```


## License

MIT ©