class MetaData:

    def __init__(self) -> None:
        self.key :str = None
        self.values :list = []

    def __repr__(self) -> str:
        return f"MetaData(key={self.key!r}, values={self.values!r})"