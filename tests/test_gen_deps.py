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
        return super().setUp()

    def test_get_import_map_without_group(self):
        expected = defaultdict(
            set,
            {
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
        self.assertDictContainsSubset(
            self._generate_dependency.get_import_map(), expected
        )

    def test_get_import_map_with_group(self):
        expected = defaultdict(
            set, {"foo.command": {"foo.parser"}, "foo.parser": {"foo.utils"}}
        )
        self.assertDictContainsSubset(
            self._generate_dependency_with_group.get_import_map(), expected
        )
