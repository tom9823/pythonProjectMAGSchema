
from PIL import Image
from PIL.TiffTags import TAGS as TIFF_TAGS

# FIXME ("understand what type of tags are there, there is V2 also.. do we have to mix them?")
from PIL.TiffTags import TAGS_V2 as TIFF_TAGS_V2

from scanner.MetaData import MetaData
from scanner.Scanner import Scanner


class TiffScanner(Scanner):
    _instance = None

    def __init__(self):
        raise RuntimeError("Cannot instantiate directly, use getInstance()")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def scan(self, file) -> list[MetaData]:
        metas :list[MetaData] = []
        with Image.open(file) as img:
            metadata = {TIFF_TAGS[tag]: value for tag, value in img.tag.items()}
            for key, value in metadata.items():
                meta :MetaData = MetaData()

                meta.key = key
                meta.values = [value]

                metas.append(meta)

        # FIXME ("v2 not working")    
        return metas

        with Image.open(file) as img:
            metadata = {TIFF_TAGS_V2[tag]: value for tag, value in img.tag.items()}
            for key, value in metadata.items():
                meta :MetaData = MetaData()

                meta.key = key
                meta.values = [value]

                metas.append(meta)

        return metas