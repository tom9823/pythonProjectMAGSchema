import hashlib
import os
import re
from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from model.IMG import ImageDimensions, ImageMetrics, PhotometricInterpretation, SamplingFrequencyPlane, \
    SamplingFrequencyUnit

KEY_FRAME_INIT = 'FrameINIT'
KEY_FRAME_SCAN = 'FrameSCAN'
KEY_FRAME_GEN = 'FrameGEN'
KEY_FRAME_DC = 'FrameDC'
KEY_FRAME_HOLDING = 'FrameHOLDING'
KEY_FRAME_LOCAL_BIB = 'FrameLOCALBIB'
KEY_FRAME_PIECE = 'FramePIECE'
KEY_FRAME_IMG = 'FrameIMG'
KEY_FRAME_IMG_2 = 'FrameIMG2'
KEY_FRAME_SCAN_OCR_RECOGNITION = 'FrameSCANOCRrecognition'
KEY_MAIN_WINDOW = 'MainWindow'
KEY_SESSION_DC = 'DC'
KEY_SESSION_LOCAL_BIB = 'LocalBIB'
KEY_SESSION_HOLDING = 'Holding'
KEY_SESSION_IMG = 'IMG'
KEY_SESSION_IMG_GROUPS = 'IMG_GROUPS'
KEY_SESSION_SIDE = 'SIDE'
KEY_SESSION_SCALE = 'SCALE'
KEY_SESSION_SCANNING = 'SCANNING'
KEY_SESSION_TARGET = 'TARGET'


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


def find_date_value(metadata_list):
    for metadata in metadata_list:
        if metadata.get_key() in ("DateTime", "CreationDate"):
            return metadata.get_values()[0]
    return None


def get_image_dimensions(metadata_list):
    image_length = None
    image_width = None
    source_xdimension = None
    source_ydimension = None
    for metadata in metadata_list:
        if metadata.get_key() in ["ImageWidth", "XResolution"]:
            image_width = metadata.get_values()[0]
        if metadata.get_key() in ["ImageLength", "YResolution"]:
            image_length = metadata.get_values()[0]
    if image_length is not None and image_width is not None:
        return ImageDimensions(imagewidth=image_width, imagelength=image_length)


def get_image_metrics(metadata_list):
    x_sampling_frequency = 400
    y_sampling_frequency = 400
    sampling_frequency_unit = SamplingFrequencyUnit.CENTIMETER
    bits_per_sample = 24
    photo_metric_interpretation = PhotometricInterpretation.RGB
    sampling_frequency_plane = SamplingFrequencyPlane.CAMERA_SCANNER_FOCAL_PLANE

    for metadata in metadata_list:
        key = metadata.get_key()

        if key == "FocalPlaneXResolution":
            x_sampling_frequency = metadata.get_values()[0]

        if key == "FocalPlaneYResolution":
            y_sampling_frequency = metadata.get_values()[0]

        if key in ["ResolutionUnit"]:
            if metadata.get_values()[0]:
                pass

        if key == "BitsPerSample":
            bits_per_sample = sum(metadata.get_values())

    if photo_metric_interpretation and bits_per_sample and sampling_frequency_unit and sampling_frequency_plane:
        return ImageMetrics(
            x_sampling_frequency=x_sampling_frequency,
            y_sampling_frequency=y_sampling_frequency,
            sampling_frequency_unit=sampling_frequency_unit,
            bit_per_sample=str(bits_per_sample),
            sampling_frequency_plane=sampling_frequency_plane,
            photo_metric_interpretation=photo_metric_interpretation
        )

def get_image_metrics(img_groupID):
    x_sampling_frequency = None
    y_sampling_frequency = None
    sampling_frequency_unit = SamplingFrequencyUnit.CENTIMETER
    bits_per_sample = 24
    photo_metric_interpretation = PhotometricInterpretation.RGB
    sampling_frequency_plane = SamplingFrequencyPlane.CAMERA_SCANNER_FOCAL_PLANE
    if img_groupID == "ImgGrp_H" or img_groupID == "ImgGrp_M":
        x_sampling_frequency = 400
        y_sampling_frequency = 400
    elif img_groupID == "ImgGrp_S":
        x_sampling_frequency = 300
        y_sampling_frequency = 300
    elif img_groupID == "ImgGrp_T":
        x_sampling_frequency = 150
        y_sampling_frequency = 150
    return ImageMetrics(
        x_sampling_frequency=x_sampling_frequency,
        y_sampling_frequency=y_sampling_frequency,
        sampling_frequency_unit=sampling_frequency_unit,
        bit_per_sample=str(bits_per_sample),
        sampling_frequency_plane=sampling_frequency_plane,
        photo_metric_interpretation=photo_metric_interpretation
    )


def get_imagegroupID(file_path):
    _, file_extension = os.path.splitext(file_path)
    definition_letter = ''
    string_parts = file_path.split('_')
    if string_parts is not None and len(string_parts) >= 1:
        definition_letter = string_parts[-1][0]

    ret = "ImgGrp_S"
    if definition_letter in ["s", "t"]:
        ret = "ImgGrp_S"
    elif definition_letter == "m":
        ret = "ImgGrp_M"
    elif definition_letter == "h":
        ret = "ImgGrp_H"
    return ret


def split_path_into_subpaths(path):
    subpaths = []
    path, folder = os.path.split(path)
    while folder != "":
        if folder != "":
            subpaths.append(folder)
        path, folder = os.path.split(path)
    if path != "":
        subpaths.append(path)
    return subpaths


def extract_xmp_metadata(metadata_list):
    # Aprire l'immagine TIFF
    xmp = None
    for metadata in metadata_list:
        key = metadata.get_key()
        if key == "XMP":
            xmpAsXML = BeautifulSoup(metadata.get_values())
            print(xmpAsXML.prettify())
        return xmp


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
