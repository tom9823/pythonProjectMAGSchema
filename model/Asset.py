from scanner.MetaData import MetaData


class Asset:

    def __init__(self) -> None:
        self.path :str = None
        self.metadata :list[MetaData] = []