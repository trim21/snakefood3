# snakefood3: Python Dependency Graphs


## Dependencies

- Python 3.
- jinja2


## Download

```bash
pip install snakefood3
```


## Usage

```bash
python -m snakefood3 PROJECT_PATH PYTHON_PACKAGE_NAME --group examples/group
```

file tree should be look like this

```
PROJECT_PATH
└─PYTHON_PACKAGE_NAME
   ├─a python package
   ├─another python package
   ├─a.py
   ├─b.py
   └─__init__.py
```

`PYTHON_PACKAGE_NAME` should be in `PROJECT_PATH`

`--group` if you want to group some package,
for example you want to group `a.lib.b` and `a.lib.c` as `a.lib`
write a file like

```
a.lib
```

all submodule will be grouped together.


```bash
python -m snakefood3 ~/code/bgmi/ bgmi -g examples/group > examples/bgmi.dot
dot -T png examples/bgmi.dot -o examples/bgmi.png # install graphviz
```


show example in [example](./example)

## Copyright and License

Copyright (C) 2019 Trim21<trim21me@gmail.com>.  All Rights Reserved.

Copyright (C) 2001-2007  Martin Blais.  All Rights Reserved.

This code is distributed under the `GNU General Public License <COPYING>`;

## Author

Trim21 <trim21me@gmail.com>

Martin Blais <blais@furius.ca>
