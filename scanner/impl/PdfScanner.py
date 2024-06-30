from PyPDF2 import PdfReader

from scanner.MetaData import MetaData
from scanner.Scanner import Scanner


class PdfScanner(Scanner):
    _instance = None

    def __init__(self):
        raise RuntimeError("Cannot instantiate directly, use getInstance()")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def scan(self, file) ->  list[MetaData]:
        with open(file, 'rb') as file:
            reader = PdfReader(file)
            metadata = reader.metadata
            print(metadata)

            metas: list = []
            for key, value in metadata.items():
                meta: MetaData = MetaData()
                meta.key = key.replace('/', '')
                meta.values = [value]

                metas.append(meta)

            return metas
