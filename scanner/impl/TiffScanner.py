
from PIL import Image
from PIL.TiffTags import TAGS as TIFF_TAGS
from scanner.MetaData import MetaData
from scanner.Scanner import Scanner
from exif import Image as ImageEXIF


class TiffScanner(Scanner):
    _instance = None

    def __init__(self):
        raise RuntimeError("Cannot instantiate directly, use getInstance()")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def scan(self, file_path) -> list[MetaData]:
        metas  = []
        with Image.open(file_path) as img:
            metadata = {TIFF_TAGS[tag]: value for tag, value in img.tag.items()}
            for key, values in metadata.items():
                metadata_values = []
                for value in values:
                    metadata_values.append(value)
                metadata = MetaData(key=key, values=metadata_values)
                metas.append(metadata)
        with open(file_path, 'rb') as image_file:
            my_image = ImageEXIF(image_file)
            my_image.list_all()
        return metas