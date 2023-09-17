from foo.utils.file_util import FileUtil
from foo.utils.list_util import ListUtil


class CSVParser:
    def __init__(self) -> None:
        self._list_util = ListUtil()
        self._file_util = FileUtil()
