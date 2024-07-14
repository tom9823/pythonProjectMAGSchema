

from PIL import Image
from PIL.ExifTags import TAGS

from scanner.MetaData import MetaData
from scanner.Scanner import Scanner
import exifread


class SimpleImageScanner(Scanner):
    _instance = None

    def __init__(self):
        raise RuntimeError("Cannot instantiate directly, use getInstance()")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def scan(self, file):
        metas  = []
        with Image.open(file) as img:
            # Pillow
            exif_data = img.getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    meta :MetaData = MetaData()
                    if tag in TAGS:
                        meta.key = TAGS[tag]
                        meta.values = [value]
                        metas.append(meta)
        #exifread
        tags_exif_read = exifread.process_file(file)
        for tag, value in tags_exif_read:
            metas.append(MetaData(key=tag, values=[value]))
        return metas