from foo.parser.csv_parser import CSVParser


class Excel:
    def __init__(self) -> None:
        self._csv_parser = CSVParser()
