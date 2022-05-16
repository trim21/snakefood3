from pathlib import Path
from typing import Generator, Union


class Utils:
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
