import hashlib
import os
from datetime import datetime

import exifread

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
        metadata_dict = {}
        with Image.open(file_path) as img:
            image_width, image_length = img.size
            metadata_dict['IMAGE_WIDTH'] = image_width
            metadata_dict['IMAGE_LENGTH'] = image_length
            metadata_dict = metadata_dict | img.info
            # Estrai i metadati EXIF per i file TIFF/TIF
            if img.format in ['TIFF', 'TIF']:
                metadata_dict = {TIFF_TAGS[tag]: self.convert_value(value) for tag, value in img.tag.items()}

            # Estrai i metadati EXIF per i file JPEG/JPG
            if img.format in ['JPEG', 'JPG']:
                exif_data = img._getexif()
                if exif_data is not None:
                    metadata_dict = {ExifTags.TAGS.get(tag, tag): self.convert_value(value) for tag, value in exif_data.items()}

            # Estrai i metadati per i file PNG
            elif img.format == 'PNG':
                if isinstance(img, PngImagePlugin.PngImageFile):
                    metadata_dict = {key: self.convert_value(value) for key, value in img.info.items()}

            # Estrai i metadati per i file GIF
            elif img.format == 'GIF':
                if isinstance(img, GifImagePlugin.GifImageFile):
                    metadata_dict = {key: self.convert_value(value) for key, value in img.info.items()}
            with open(file_path, 'rb') as img_file:
                meta_dict_exif = exifread.process_file(img_file)
                for key, tag in meta_dict_exif.items():
                    metadata_dict[key] = tag.printable if hasattr(tag, 'printable') else tag

            metadata_dict["MD5"] = self.get_file_md5(file_path)
            metadata_dict["FILE_SIZE"] = self.get_file_size(file_path)
            metadata_dict["CREATION_DATE_FILE"] = self.get_creation_date(file_path)
            metadata_dict["DPI"] = img.info.get('dpi',(0,0))

        return metadata_dict

    def convert_value(self, value):
        """Converte tuple o singoli valori nei tipi appropriati."""
        if isinstance(value, tuple):
            # Se la tupla ha un solo elemento
            if len(value) == 1:
                single_value = value[0]
                # Verifica se è int, float o stringa e restituiscilo nel suo tipo appropriato
                if isinstance(single_value, int):
                    return int(single_value)
                elif isinstance(single_value, float):
                    return float(single_value)
                elif isinstance(single_value, str):
                    return str(single_value)
                else:
                    return single_value
            # Se la tupla ha più di un elemento, mettili in un array (lista)
            return [v for v in value]
        return value

    def get_file_md5(self, file_path):
        # Crea un oggetto hash MD5
        md5_hash = hashlib.md5()

        # Leggi il file in blocchi per non occupare troppa memoria
        with open(file_path, 'rb') as file:
            # Leggi il file in blocchi di 4096 byte
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)

        # Restituisci l'hash MD5 in formato esadecimale
        return md5_hash.hexdigest()

    def get_file_size(self, file_path):
        # Restituisce la dimensione del file in byte
        return os.path.getsize(file_path)

    def get_creation_date(self,file_path):
        # Ottieni il timestamp di creazione del file
        creation_time = os.path.getctime(file_path)
        # Converti il timestamp in una data leggibile
        creation_date = datetime.fromtimestamp(creation_time)
        # Formatta la data nel formato desiderato (es. 'YYYY-MM-DD HH:MM:SS')
        formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date