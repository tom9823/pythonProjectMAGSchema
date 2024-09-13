import hashlib
import os
import re
from datetime import datetime
from urllib.parse import urlparse

import exifread
from PIL import Image

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
KEY_FRAME_NOMENCLATURE = 'FrameNOMENCLATURE'
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
KEY_SESSION_NOMENCLATURE = 'NOMENCLATURE'
KEY_SESSION_FOLDER_PATH = 'FOLDERPATH'


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


def find_date_value(metadata_dict):
    ret = metadata_dict.get('DateTimeOriginal')
    if ret is None:
        ret = metadata_dict.get('DateTimeDigitized')
    if ret is None:
        ret = metadata_dict.get('CreationDate')
    if ret is None:
        ret = metadata_dict.get('DateTime')
    if ret is None:
        ret = metadata_dict.get('CREATION_DATE_FILE')
    return ret


def get_image_dimensions(metadata_dict):
    x_res = int(metadata_dict.get('Image XResolution', 300))
    y_res = int(metadata_dict.get('Image YResolution', 300))
    # Ottieni larghezza e lunghezza dell'immagine in pixel, default a 0 se non trovate
    image_width = int(metadata_dict.get('Image ImageWidth', 0))
    image_length = int(metadata_dict.get('Image ImageLength', 0))
    # Calcola dimensioni in pollici
    source_xdimension = image_width / x_res if x_res else 0
    source_ydimension = image_length / y_res if y_res else 0
    if image_length == 0 or image_width == 0:
        image_width = metadata_dict.get("ImageWidth",0)
        image_length = metadata_dict.get("ImageLength",0)
        x_res = int(metadata_dict.get('XResolution', 300))
        y_res = int(metadata_dict.get('YResolution', 300))
        source_xdimension = image_width / x_res if x_res else 0
        source_ydimension = image_length / y_res if y_res else 0
    if image_length == 0 or image_width == 0:
        image_width = metadata_dict.get("IMAGE_WIDTH", 0)
        image_length = metadata_dict.get("IMAGE_LENGTH", 0)
    return ImageDimensions(
        imagewidth=image_width,
        imagelength=image_length,
        source_xdimension=source_xdimension,
        source_ydimension=source_ydimension
    )


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


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def get_ppi_dpi(metadata_dict):
    ppi, dpi = 0, 0
    dpi = int(metadata_dict.get('dpi',(0,0))[0])
    x_res = metadata_dict.get('Image XResolution', None)
    y_res = metadata_dict.get('Image YResolution', None)
    res_unit = metadata_dict.get('Image ResolutionUnit', None)
    if x_res is not None and y_res is not None and res_unit is not None:
        if res_unit == 'Pixels/Inch' and int(x_res) == int(y_res):
            ppi = int(x_res)
    return ppi, dpi
