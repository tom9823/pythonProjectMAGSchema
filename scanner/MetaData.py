class MetaData:

    def __init__(self, key = None, values = []):
        self.key  = key
        self.values = values

    def get_key(self):
        return self.key

    def get_values(self):
        return self.values

    def __repr__(self) -> str:
        return f"MetaData(key={self.key!r}, values={self.values!r})"