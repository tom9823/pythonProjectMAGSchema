

from PIL import Image
from PIL.ExifTags import TAGS

from scanner.MetaData import MetaData
from scanner.Scanner import Scanner


class SimpleImageScanner(Scanner):
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
            # TIFF             metadata = {Image.TAGS_V2[tag]: value for tag, value in img.tag_v2.items()}
            exif_data = img.getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    meta :MetaData = MetaData()
                    if tag in TAGS:
                        meta.key = TAGS[tag]
                        meta.values = [value]
                    # TODO("Unknown tags shall be included?")
                    #else:
                    #    meta.key = f'UNKNOWN_TAG_{tag}'
                    #    meta.values = [value]
                        metas.append(meta)

        return metas