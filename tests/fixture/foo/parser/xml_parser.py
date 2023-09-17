from foo.utils.file_util import FileUtil
from foo.utils.list_util import ListUtil
from foo.utils.string_util import StringUtil


class CSVParser:
    def __init__(self) -> None:
        self._list_util = ListUtil()
        self._file_util = FileUtil()
        self._string_util = StringUtil()
