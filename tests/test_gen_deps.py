from collections import defaultdict
from pathlib import Path
from unittest import TestCase

from snakefood3.gen_deps import GenerateDependency


class TestGenDeps(TestCase):
    def setUp(self) -> None:
        self._generate_dependency = GenerateDependency(
            root_path=Path(__file__).parent / "fixture", package_name="foo"
        )
        self._generate_dependency_with_group = GenerateDependency(
            root_path=Path(__file__).parent / "fixture",
            package_name="foo",
            group_packages={"foo.command", "foo.parser", "foo.utils"},
        )
        self._generate_dependency_internal = GenerateDependency(
            root_path=Path(__file__).parent / "fixture",
            package_name="foo",
            track_external=False,
        )
        return super().setUp()

    def test_get_import_map_without_group(self):
        expected = defaultdict(
            set,
            {
                "foo.external": {"os", "os.path", "threading"},
                "foo.command.connectivity.netsh": {"foo.parser.xml_parser"},
                "foo.command.power.powrcfg": {"foo.parser.xml_parser"},
                "foo.command.productivity.excel": {"foo.parser.csv_parser"},
                "foo.parser.csv_parser": {"foo.utils.file_util", "foo.utils.list_util"},
                "foo.parser.xml_parser": {
                    "foo.utils.string_util",
                    "foo.utils.file_util",
                    "foo.utils.list_util",
                },
                "foo.utils.list_util": {"foo.utils.string_util"},
            },
        )
        assert dict(expected, **self._generate_dependency.get_import_map()) == expected

    def test_get_import_map_with_group(self):
        expected = defaultdict(
            set, {
                "foo.external": {"os", "os.path", "threading"},
                "foo.command": {"foo.parser"},
                "foo.parser": {"foo.utils"}}
        )
        assert (
            dict(expected, **self._generate_dependency_with_group.get_import_map())
            == expected
        )

    def test_module_to_filename(self):
        # module: str, python_path: Path
        assert GenerateDependency.module_to_filename(
            "a.lib.csv_parser", Path("/home/usr/src")
        ) == Path("/home/usr/src/a/lib/csv_parser.py")

        # module: str, python_path: str
        assert GenerateDependency.module_to_filename(
            "a.lib.csv_parser", "/home/usr/src"
        ) == Path("/home/usr/src/a/lib/csv_parser.py")

    def test_filename_to_module(self):
        # filepath: str, python_path: str
        assert (
            GenerateDependency.filename_to_module(
                "/home/usr/src/a/lib/csv_parser.py", "/home/usr/src"
            )
            == "a.lib.csv_parser"
        )

        # filepath: Path, python_path: str
        assert (
            GenerateDependency.filename_to_module(
                Path("/home/usr/src/a/lib/csv_parser.py"), "/home/usr/src"
            )
            == "a.lib.csv_parser"
        )

        # filepath: str, python_path: Path
        assert (
            GenerateDependency.filename_to_module(
                "/home/usr/src/a/lib/csv_parser.py", Path("/home/usr/src")
            )
            == "a.lib.csv_parser"
        )

    def test_get_first_prefix_matching_string(self):
        # One prefix exist
        assert (
            GenerateDependency.get_first_prefix_matching_string(
                "a.parser.csv_parser", "a.utils", "a.parser", "a.command"
            )
            == "a.parser"
        )

        # No prefix exist
        assert (
            GenerateDependency.get_first_prefix_matching_string(
                "a.lib.command.ping", "a.command", "a.parser", "a.utils"
            )
            == "a.lib.command.ping"
        )

    def test_get_import_map_internal(self):
        expected = defaultdict(
            set,
            {
                "foo.external": {},
                "foo.command.connectivity.netsh": {"foo.parser.xml_parser"},
                "foo.command.power.powrcfg": {"foo.parser.xml_parser"},
                "foo.command.productivity.excel": {"foo.parser.csv_parser"},
                "foo.parser.csv_parser": {"foo.utils.file_util", "foo.utils.list_util"},
                "foo.parser.xml_parser": {
                    "foo.utils.string_util",
                    "foo.utils.file_util",
                    "foo.utils.list_util",
                },
                "foo.utils.list_util": {"foo.utils.string_util"},
            },
        )
        assert dict(expected, **self._generate_dependency_internal.get_import_map()) == expected
