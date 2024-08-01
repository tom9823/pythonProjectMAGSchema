import Utils
from scanner.MetaData import MetaData
from scanner.Scanner import Scanner
from PIL import Image, ExifTags, PngImagePlugin, GifImagePlugin
from PIL.TiffTags import TAGS as TIFF_TAGS


class ImageScanner(Scanner):
    _instance = None

    def __init__(self):
        raise RuntimeError("Cannot instantiate directly, use getInstance()")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def scan(self, file_path):
        metas = []
        with Image.open(file_path) as img:
            metadata = {}

            # Estrai i metadati EXIF per i file TIFF/TIF
            if img.format in ['TIFF', 'TIF']:
                metadata = {TIFF_TAGS[tag]: value for tag, value in img.tag.items()}

            # Estrai i metadati EXIF per i file JPEG/JPG
            if img.format in ['JPEG', 'JPG']:
                exif_data = img._getexif()
                if exif_data is not None:
                    metadata = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}

            # Estrai i metadati per i file PNG
            elif img.format == 'PNG':
                if isinstance(img, PngImagePlugin.PngImageFile):
                    metadata = {key: value for key, value in img.info.items()}

            # Estrai i metadati per i file GIF
            elif img.format == 'GIF':
                if isinstance(img, GifImagePlugin.GifImageFile):
                    metadata = {key: value for key, value in img.info.items()}
            for key, values in metadata.items():
                metadata_values = []
                if not Utils.is_iterable(values) or isinstance(values, str):
                    metadata_values.append(values)
                else:
                    for value in values:
                        metadata_values.append(value)
                metadata = MetaData(key=key, values=metadata_values)
                metas.append(metadata)
        return metas

