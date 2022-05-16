import argparse
import ast
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Generator, Set, Union

from snakefood3.graph import graph


class GenerateDependency:
    def __init__(
        self, root_path: str, package_name: str, group_packages: Set[str] = set()
    ) -> None:
        self._root_path = Path(root_path)
        self._package_name = package_name
        self._group_packages = group_packages
        self._internal_packages = None

    @classmethod
    def iter_py_files(
        cls, directory_path: Union[Path, str], extension="py"
    ) -> Generator[Path, None, None]:
        """Get all the files under a directory with specific extension

        :param directory_path: directory path
        :param extension: file extension, defaults to "py"
        :yield: Generator which yields path of all file of a specific extension
        """
        yield from Path(directory_path).rglob(f"*.{extension}")

    @classmethod
    def module_to_filename(cls, module_name: str, root_path: Union[Path, str]) -> Path:
        """Given a module name and root path of the module, give module path

        :param module_name: module name as in import statement (e.g. a.lib.csv_parser)
        :param root_path: root path of the module
        :return: path of the module
        """
        return Path(root_path) / (module_name.replace(".", "/") + ".py")

    @classmethod
    def filename_to_module(
        cls, filepath: Union[Path, str], root_path: Union[Path, str]
    ) -> str:
        """Given a filepath and a root_path derive the module name as in import statement

        :param filepath: file path of the module
        :param root_path: root path of the package
        :return: module name as in import statement (e.g. a.lib.csv_parser)
        """
        realpath = str(Path(filepath).relative_to(root_path))
        realpath = realpath.replace("\\", ".")
        realpath = realpath.replace("/", ".")
        realpath = realpath.split(".py")[0]
        if realpath.endswith(".__init__"):
            realpath = realpath.split(".__init__")[0]
        return realpath

    @classmethod
    def get_first_prefix_matching_string(cls, string: str, *prefixes: str) -> str:
        """Given prefixs and a string, return the first prefix with which the string starts. If no such prefix is present, return the original string

        :param string: string which will be matched against multiple prefix
        :return: first prefix with which the string starts if present, else return original string
        """
        for prefix in prefixes:
            if string.startswith(prefix):
                return prefix
        return string

    def get_internal_packages(self) -> Set[Path]:
        """Get all the internal packages for a project"""
        if self._internal_packages is None:
            python_path = self._root_path.resolve()
            self._internal_packages = {
                directory
                for directory in python_path.iterdir()
                if directory.is_dir() and (directory / "__init__.py").exists()
            }
        return self._internal_packages

    def _get_all_imports_of_file(self, filename: Path) -> Set[str]:
        current_module = self.filename_to_module(filename, self._root_path)
        if filename.name == "__init__.py":
            current_module += ".__init__"
        imports = set()
        for node in ast.walk(
            ast.parse(source=filename.read_text(encoding="utf8"), filename=filename)
        ):
            if isinstance(node, ast.Import):
                for name in node.names:
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
                    module = ".".join(current_module.split(".")[: -node.level])
                    if node.module:
                        module += "." + node.module
                    else:
                        # from . import b # module==None,name=='b'
                        # maybe base_module.b or Base_module#b
                        pass
                for name in node.names:
                    maybe_dir = (
                        self._root_path / "/".join(module.split(".")) / name.name
                    )
                    maybe_file = self.module_to_filename(
                        module + "." + name.name, self._root_path
                    )
                    if Path(maybe_dir).exists() or Path(maybe_file).exists():
                        added.add(module + "." + name.name)
                    else:
                        added.add(module)
                imports.update(added)
        return imports

    def get_import_map(self) -> DefaultDict[str, Set[str]]:
        """Gets the import mapping for each module in the project"""
        imports = defaultdict(set)
        internal_packages = self.get_internal_packages()

        for file in self.iter_py_files(self._root_path / self._package_name):
            file_imports = self._get_all_imports_of_file(file)
            current_module = self.filename_to_module(file, self._root_path)
            imports[
                self.get_first_prefix_matching_string(
                    current_module, *self._group_packages
                )
            ].update(
                {
                    self.get_first_prefix_matching_string(
                        _import, *self._group_packages
                    )
                    for _import in file_imports
                    if [c for c in str(internal_packages) if _import.startswith(str(c))]
                }
            )
        formatted_imports = defaultdict(set)
        for source, dist in imports.items():
            if dist:
                for d in dist:
                    if source != d:
                        formatted_imports[source].add(d)
        return formatted_imports

    def make_dot_file(self) -> str:
        """Use existing template to generate a graph in dot language"""
        return graph(self.get_import_map())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g", "--group", help="group module name", type=argparse.FileType("r")
    )
    parser.add_argument("project_path")
    parser.add_argument("package_name")

    args = parser.parse_args()
    if args.group:
        groups = {line.strip() for line in args.group.readlines() if line.strip()}
        generate_dependency = GenerateDependency(
            args.project_path, args.package_name, groups
        )
    else:
        generate_dependency = GenerateDependency(args.project_path, args.package_name)
    print(generate_dependency.make_dot_file())
