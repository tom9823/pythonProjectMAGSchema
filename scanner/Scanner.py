from scanner.MetaData import MetaData


class Scanner:

    def __init__(self) -> None:
        raise RuntimeError("Cannot instantiate directly, use getInstance() on any implementation of this")

    def scan(self, file_path) -> list[MetaData]:
        raise Exception("Not Yet Implemented")