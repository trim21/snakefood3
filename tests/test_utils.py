from pathlib import Path
from unittest import TestCase
from snakefood3.utils import Utils


class TestUtils(TestCase):
    def test_module_to_filename(self):
        # module: str, python_path: Path
        self.assertEqual(
            Utils.module_to_filename("a.lib.csv_parser", Path("/home/usr/src")),
            Path(r"\home\usr\src\a\lib\csv_parser.py"),
        )
        # module: str, python_path: str
        self.assertEqual(
            Utils.module_to_filename("a.lib.csv_parser", "/home/usr/src"),
            Path(r"\home\usr\src\a\lib\csv_parser.py"),
        )

    def test_filename_to_module(self):
        # filepath: str, python_path: str
        self.assertEqual(
            Utils.filename_to_module(
                r"\home\usr\src\a\lib\csv_parser.py", "/home/usr/src"
            ),
            "a.lib.csv_parser",
        )
        # filepath: Path, python_path: str
        self.assertEqual(
            Utils.filename_to_module(
                Path(r"\home\usr\src\a\lib\csv_parser.py"), "/home/usr/src"
            ),
            "a.lib.csv_parser",
        )
        # filepath: str, python_path: Path
        self.assertEqual(
            Utils.filename_to_module(
                r"\home\usr\src\a\lib\csv_parser.py", Path("/home/usr/src")
            ),
            "a.lib.csv_parser",
        )

    def test_get_first_prefix_matching_string(self):
        # One prefix exist
        self.assertEqual(
            Utils.get_first_prefix_matching_string(
                "a.parser.csv_parser", "a.utils", "a.parser", "a.command"
            ),
            "a.parser",
        )
        # No prefix exist
        self.assertEqual(
            Utils.get_first_prefix_matching_string(
                "a.lib.command.ping", "a.command", "a.parser", "a.utils"
            ),
            "a.lib.command.ping",
        )
