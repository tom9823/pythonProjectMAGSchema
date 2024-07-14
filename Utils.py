import hashlib
import os
import re
from datetime import datetime
from urllib.parse import urlparse

KEY_FRAME_INIT = 'FrameINIT'
KEY_FRAME_SCAN = 'FrameSCAN'
KEY_FRAME_GEN = 'FrameGEN'
KEY_FRAME_DC = 'FrameDC'
KEY_FRAME_HOLDING = 'FrameHOLDING'
KEY_FRAME_LOCAL_BIB = 'FrameLOCALBIB'
KEY_FRAME_PIECE = 'FramePIECE'
KEY_FRAME_SCAN_OCR_RECOGNITION = 'FrameSCANOCRrecognition'
KEY_MAIN_WINDOW = 'MainWindow'
KEY_SESSION_DC = 'DC'
KEY_SESSION_LOCAL_BIB = 'LocalBIB'
KEY_SESSION_HOLDING = 'Holding'
KEY_SESSION_IMG = 'IMG'


def validate_uri(uri):
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def validate_agency(agency):
    pattern = re.compile(r'^[A-Z]{2}:[A-Za-z0-9]+$')
    return pattern.match(agency) is not None


def validate_sici(sici_string):
    sici_pattern = re.compile(
        r'\((\d{4}(/\d{4})?((\d{2})(/(\d{2}|\d{6}))?((\d{2})(/\d{2})?)?)?)?\)'
        r'((\+|\*)?|(\d{1,4}(:(\d{1,4})(/\d{1,4})?(\+|\*)?)?'
        r'(:(\d{1,4})(/\d{1,4})?(\+|\*)?)?(:(\d{1,4})(/\d{1,4})?(\+|\*)?)?)?)?'
    )
    return bool(sici_pattern.fullmatch(sici_string))


def validate_bici(bici_string):
    bici_pattern = re.compile(r'\d{1,3}(:\d{1,4}(:\d{1,4})?)?')
    return bool(bici_pattern.fullmatch(bici_string))


def get_creation_date(file_path):
    # Ottieni il timestamp di creazione del file
    creation_time = os.path.getctime(file_path)
    # Converti il timestamp in una data leggibile
    creation_date = datetime.fromtimestamp(creation_time)
    # Formatta la data nel formato desiderato (es. 'YYYY-MM-DD HH:MM:SS')
    formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def get_file_md5(file_path):
    # Crea un oggetto hash MD5
    md5_hash = hashlib.md5()

    # Leggi il file in blocchi per non occupare troppa memoria
    with open(file_path, 'rb') as file:
        # Leggi il file in blocchi di 4096 byte
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    # Restituisci l'hash MD5 in formato esadecimale
    return md5_hash.hexdigest()


def get_file_size(file_path):
    # Restituisce la dimensione del file in byte
    return os.path.getsize(file_path)
