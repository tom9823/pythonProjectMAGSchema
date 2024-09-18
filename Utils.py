import os
import re
from urllib.parse import urlparse

from model.IMG import ImageDimensions, ImageMetrics, PhotometricInterpretation, SamplingFrequencyPlane, \
    SamplingFrequencyUnit, BitPerSample

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
KEY_SESSION_IMG_DICT_PROJECT = 'IMG_DICT_PROJECT'
KEY_SESSION_IMG_GROUPS = 'IMG_GROUPS'
KEY_SESSION_IMG_DICT_FOLDER = 'IMG_DICT_FOLDER'
KEY_SESSION_GENERATION_OPTION_XML = 'GENERATION_OPTION_XML'
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
    image_width = metadata_dict.get("ImageWidth",0)
    image_length = metadata_dict.get("ImageLength",0)
    x_res = metadata_dict.get('XResolution', (300))
    if x_res and isinstance(x_res, tuple):
        x_res = int(x_res[0])
    y_res = metadata_dict.get('YResolution', (300))
    if y_res and isinstance(y_res, tuple):
        y_res = int(y_res[0])
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


def get_image_metrics(metadata_dict):
    # Recupera la frequenza di campionamento sull'asse X
    x_sampling_frequency = metadata_dict.get('XResolution', None)
    if x_sampling_frequency and isinstance(x_sampling_frequency, tuple):
        x_sampling_frequency = int(x_sampling_frequency[0])

    # Recupera la frequenza di campionamento sull'asse Y
    y_sampling_frequency = metadata_dict.get('YResolution', None)
    if y_sampling_frequency and isinstance(y_sampling_frequency, tuple):
        y_sampling_frequency = int(y_sampling_frequency[0])

    # Recupera l'unità di misura per la frequenza di campionamento
    sampling_frequency_unit = metadata_dict.get('ResolutionUnit', None)
    if sampling_frequency_unit is not None:
        sampling_frequency_unit = int(sampling_frequency_unit)
        if sampling_frequency_unit == 2:
            sampling_frequency_unit = SamplingFrequencyUnit.INCH
        elif sampling_frequency_unit == 3:
            sampling_frequency_unit = SamplingFrequencyUnit.CENTIMETER
        else:
            sampling_frequency_unit = SamplingFrequencyUnit.NO_UNIT

    # Interpretazione fotometrica
    photometric_interpretation_value = metadata_dict.get('PhotometricInterpretation', None)
    if photometric_interpretation_value is not None:
        photometric_interpretation_value = int(photometric_interpretation_value)
        if photometric_interpretation_value == 0:
            photo_metric_interpretation = PhotometricInterpretation.WHITE_IS_ZERO
        elif photometric_interpretation_value == 1:
            photo_metric_interpretation = PhotometricInterpretation.BLACK_IS_ZERO
        elif photometric_interpretation_value == 2:
            photo_metric_interpretation = PhotometricInterpretation.RGB
        elif photometric_interpretation_value == 3:
            photo_metric_interpretation = PhotometricInterpretation.PALETTE_COLOR
        elif photometric_interpretation_value == 4:
            photo_metric_interpretation = PhotometricInterpretation.TRANSPARENCY_MASK
        elif photometric_interpretation_value == 5:
            photo_metric_interpretation = PhotometricInterpretation.CMYK
        elif photometric_interpretation_value == 6:
            photo_metric_interpretation = PhotometricInterpretation.YCBCR
        elif photometric_interpretation_value == 8:
            photo_metric_interpretation = PhotometricInterpretation.CIELAB
        else:
            photo_metric_interpretation = PhotometricInterpretation.RGB
    else:
        photo_metric_interpretation = PhotometricInterpretation.RGB
    # Piano focale del campionamento (sampling frequency plane)
    sampling_frequency_plane_value = metadata_dict.get('SamplingFrequencyPlane', None)
    if sampling_frequency_plane_value is not None:
        sampling_frequency_plane_value = int(sampling_frequency_plane_value)
        if sampling_frequency_plane_value == 1:
            sampling_frequency_plane = SamplingFrequencyPlane.CAMERA_SCANNER_FOCAL_PLANE
        elif sampling_frequency_plane_value == 2:
            sampling_frequency_plane = SamplingFrequencyPlane.OBJECT_PLANE
        elif sampling_frequency_plane_value == 3:
            sampling_frequency_plane = SamplingFrequencyPlane.SOURCE_OBJECT_PLANE
        else:
            sampling_frequency_plane = SamplingFrequencyPlane.CAMERA_SCANNER_FOCAL_PLANE
    else:
        sampling_frequency_plane = SamplingFrequencyPlane.CAMERA_SCANNER_FOCAL_PLANE

    # Bit per campione
    bits_per_sample = metadata_dict.get('BitsPerSample', BitPerSample.RGB_24_BIT)  # Default a 24 se non trovato
    if isinstance(bits_per_sample, tuple) or isinstance(bits_per_sample, list):
        bits_str = ','.join(map(str, bits_per_sample))
        for bit in BitPerSample:
            if bit.value == bits_str:
                bits_per_sample = bit

    if x_sampling_frequency and y_sampling_frequency and sampling_frequency_unit and photo_metric_interpretation and bits_per_sample and sampling_frequency_plane:
        return ImageMetrics(x_sampling_frequency=x_sampling_frequency,
                     y_sampling_frequency=y_sampling_frequency,
                     sampling_frequency_plane=sampling_frequency_plane,
                     bit_per_sample=bits_per_sample,
                     photo_metric_interpretation=photo_metric_interpretation,
                     sampling_frequency_unit=sampling_frequency_unit
        )
    else:
        return None


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


def get_ppi_dpi(metadata_dict):
    ppi, dpi = 0, 0
    tuple_dpi = metadata_dict.get('DPI', (0,0))
    dpi = int(tuple_dpi[0]) if len(tuple_dpi) == 2 and int(tuple_dpi[0]) == int(tuple_dpi[1]) and int(tuple_dpi[0]) != 0 else 0
    x_res = metadata_dict.get('XResolution', (300))
    if x_res and isinstance(x_res, tuple):
        x_res = int(x_res[0])
    y_res = metadata_dict.get('YResolution', (300))
    if y_res and isinstance(y_res, tuple):
        y_res = int(y_res[0])
    res_unit = metadata_dict.get('ResolutionUnit', None)
    if x_res is not None and y_res is not None and res_unit is not None:
        if res_unit == 2 and int(x_res) == int(y_res):
            ppi = int(x_res)
    return ppi, dpi
