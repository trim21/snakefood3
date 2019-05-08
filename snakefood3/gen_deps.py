import ast
import glob
from collections import defaultdict
from os import path

from snakefood3.graph import graph

cached_exists_files = {}


def file_exists(filename):
    if filename in cached_exists_files:
        return cached_exists_files[filename]
    else:
        status = path.exists(filename)
        cached_exists_files[filename] = status
        return status


def parse_file(filename) -> ast.AST:
    with open(filename, 'r', encoding='utf8') as f:
        return ast.parse(f.read(), filename)


def iter_py_files(dir_name):
    return glob.glob(path.join(dir_name, '**', '*.py')) +\
           glob.glob(path.join(dir_name, '*.py'))


def get_all_imports_of_file(filename, python_path):
    current_module = filename_to_module(filename, python_path)
    if filename.endswith('__init__.py'):
        current_module += '.__init__'
    imports = set()
    for node in ast.walk(parse_file(filename)):
        if isinstance(node, ast.Import):
            for name in node.names:
                # print(name.name)
                imports.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            # find which module is imported from
            # from .a import b # module=='a',name=='b'
            # maybe base_module.a.b or Base_module.a#b
            # from .a.b import c # module=='a.b',name=='c'
            # maybe base_module.a.b.c or Base_module.a.b#c
            # module should be
            added = set()
            if node.level == 0:
                module = node.module
            else:
                module = '.'.join(current_module.split('.')[:-node.level])
                if node.module:
                    module += '.' + node.module
                else:
                    # from . import b # module==None,name=='b'
                    # maybe base_module.b or Base_module#b
                    pass
            for name in node.names:
                maybe_dir = path.join(
                    python_path,
                    *module.split('.'),
                    name.name,
                )
                maybe_file = module_to_filename(
                    module + '.' + name.name, python_path
                )
                if file_exists(maybe_dir) or file_exists(maybe_file):
                    added.add(module + '.' + name.name)
                else:
                    added.add(module)
            imports.update(added)
    return imports


def filename_to_module(filepath, python_path):
    realpath = path.relpath(filepath, python_path)
    realpath = realpath.replace('\\', '.')
    realpath = realpath.replace('/', '.')
    realpath = realpath.split('.py')[0]  # type: str
    if realpath.endswith('.__init__'):
        realpath = realpath.split('.__init__')[0]
    return realpath


def module_to_filename(module: str, python_path):
    module = module.replace('.', '/') + '.py'
    return path.join(python_path, module)


import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--internal', action='store_true')
    # parser.add_argument('-e', '--external', action='store_true')
    parser.add_argument(
        '-g',
        '--group',
        help='group module name',
        type=argparse.FileType('r'),
    )
    parser.add_argument('project_path', )
    parser.add_argument('package_name', )

    r = parser.parse_args()

    if r.group:
        groups = [line.strip() for line in r.group.readlines() if line.strip()]
    else:
        groups = []

    def replace(node_name):
        for m in groups:
            if node_name.startswith(m):
                return m

        return node_name

    python_path = path.abspath(path.expanduser(r.project_path))
    internal_package = {
        x for x in os.listdir(python_path)
        if path.isdir(path.join(python_path, x))
        and path.exists(path.join(python_path, x, '__init__.py'))
    }

    imports = defaultdict(set)
    for file in iter_py_files(path.join(python_path, r.package_name)):
        file_imports = get_all_imports_of_file(
            file,
            python_path=python_path,
        )
        current_module = filename_to_module(file, python_path)
        imports[replace(current_module)].update({
            replace(x)
            for x in file_imports
            if [c for c in internal_package if x.startswith(c)]
        })
    formatted_imports = defaultdict(set)
    for source, dist in imports.items():
        if dist:
            for d in dist:
                if source != d:
                    formatted_imports[source].add(d)
    print(graph(formatted_imports.items()))


if __name__ == '__main__.py':
    main()
