import re
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
KEY_SESSION_LOCAL_BIB = 'LocalBIB'
KEY_SESSION_HOLDING = 'Holding'


def validate_uri(uri):
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def validate_agency(agency):
    pattern = re.compile(r'^[A-Z]{2}:[A-Za-z0-9]+$')
    return pattern.match(agency) is not None

def validate_sici_format(string):
    # Definire i pattern regex per cronologia, numerazione, supplementi e indici
    cronologia = r"\(\d{4}(?:\d{2}(?:\d{2})?)?(?:/\d{4}(?:\d{2}(?:\d{2})?)?)?\)"
    cronologia_combinata = r"\((?:\d{4}(?:\d{2}(?:\d{2})?)?(?:/\d{4}(?:\d{2}(?:\d{2})?)?)?|(?:\d{4}(?:\d{2})?)?\)\d{2}/\d{2})?\)"
    numerazione = r"(?:(?:\d+(:\d+){0,3})|\*)"
    supplementi = r"\+"
    indici = r"\*"

    # Creare il pattern completo combinando cronologia e numerazione
    pattern = fr"^{cronologia_combinata}({numerazione})?(:{numerazione})?(:{numerazione})?(:{numerazione})?({supplementi}|{indici})?$"

    # Verificare se la stringa corrisponde al pattern
    match = re.match(pattern, string)

    return match is not None