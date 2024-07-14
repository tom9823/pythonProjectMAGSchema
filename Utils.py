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
KEY_SESSION_DC = 'DC'
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
