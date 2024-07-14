class MetaData:

    def __init__(self, key = None, values=[]):
        self.key  = key
        self.values :list = values

    def __repr__(self) -> str:
        return f"MetaData(key={self.key!r}, values={self.values!r})"