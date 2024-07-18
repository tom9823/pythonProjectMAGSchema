import xml.etree.ElementTree as ET
from enum import Enum
from typing import List, Optional


# Definizione della prima enum per tipo di immagine
class ImageType(Enum):
    MASTER = 1
    HIGH_RESOLUTION = 2
    LOW_RESOLUTION = 3
    PREVIEW = 4


# Definizione della seconda enum per stato di copyright
class CopyrightStatus(Enum):
    NO_COPYRIGHT = 'a'
    HAS_COPYRIGHT = 'b'


class IMG:
    _sequence_counter = 0  # Variabile di classe per mantenere il conteggio delle istanze

    def __init__(self, nomenclature=None, usage=None, side=None, scale=None,
                 file=None, md5=None, filesize=None, image_dimensions=None, image_metrics=None,
                 ppi=None, dpi=None, format=None, scanning=None, datetimecreated=None, target=None,
                 altimg=None, note=None, imggroupID=None, holdingsID=None):
        IMG._increment_sequence_counter()
        self._sequence_number = IMG._sequence_counter
        self._nomenclature = nomenclature
        self._usage = usage if usage is not None else []
        self._side = side
        self._scale = scale
        self._file = file
        self._md5 = md5
        self._filesize = filesize
        self._image_dimensions = image_dimensions
        self._image_metrics = image_metrics
        self._ppi = ppi
        self._dpi = dpi
        self._format = format
        self._scanning = scanning
        self._datetimecreated = datetimecreated
        self._target = target if target is not None else []
        self._altimg = altimg if altimg is not None else []
        self._note = note
        self._imggroupID = imggroupID
        self._holdingsID = holdingsID

    @classmethod
    def _increment_sequence_counter(cls):
        cls._sequence_counter += 1

    @property
    def sequence_number(self):
        return self._sequence_number

    def get_nomenclature(self):
        return self._nomenclature

    def set_nomenclature(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("nomenclature deve essere di tipo xsd:string")
        self._nomenclature = value

    def get_usage(self):
        return self._usage

    def set_usage(self, value):
        if not isinstance(value, list):
            raise ValueError("usage deve essere una lista di tipo usages")
        self._usage = value

    def get_side(self):
        return self._side

    def set_side(self, value):
        self._side = value

    def get_scale(self):
        return self._scale

    def set_scale(self, value):
        self._scale = value

    def get_file(self):
        return self._file

    def set_file(self, value):
        self._file = value

    def get_md5(self):
        return self._md5

    def set_md5(self, value):
        self._md5 = value

    def get_filesize(self):
        return self._filesize

    def set_filesize(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("filesize deve essere un xsd:positiveInteger")
        self._filesize = value

    def get_image_dimensions(self):
        return self._image_dimensions

    def set_image_dimensions(self, value):
        self._image_dimensions = value

    def get_image_metrics(self):
        return self._image_metrics

    def set_image_metrics(self, value):
        self._image_metrics = value

    def get_ppi(self):
        return self._ppi

    def set_ppi(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("ppi deve essere un xsd:positiveInteger")
        self._ppi = value

    def get_dpi(self):
        return self._dpi

    def set_dpi(self, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("dpi deve essere un xsd:positiveInteger")
        self._dpi = value

    def get_format(self):
        return self._format

    def set_format(self, value):
        self._format = value

    def get_scanning(self):
        return self._scanning

    def set_scanning(self, value):
        self._scanning = value

    def get_datetimecreated(self):
        return self._datetimecreated

    def set_datetimecreated(self, value):
        self._datetimecreated = value

    def get_target(self):
        return self._target

    def set_target(self, value):
        if not isinstance(value, list):
            raise ValueError("target deve essere una lista di tipo niso:targetdata")
        self._target = value


# Definizione dei tipi semplici e complessi NISO
class NISOChecksum(str):
    def __new__(cls, value):
        if len(value) != 32:
            raise ValueError("Checksum must be 32 characters long")
        return str.__new__(cls, value)


class ImageDimensions:
    def __init__(self, imagelength: int, imagewidth: int, source_xdimension: Optional[float] = None,
                 source_ydimension: Optional[float] = None):
        self.imagelength = imagelength
        self.imagewidth = imagewidth
        self.source_xdimension = source_xdimension
        self.source_ydimension = source_ydimension

    def to_xml(self):
        dimensions_elem = ET.Element('dimensions')
        ET.SubElement(dimensions_elem, 'imagelength').text = str(self.imagelength)
        ET.SubElement(dimensions_elem, 'imagewidth').text = str(self.imagewidth)
        if self.source_xdimension is not None:
            ET.SubElement(dimensions_elem, 'source_xdimension').text = str(self.source_xdimension)
        if self.source_ydimension is not None:
            ET.SubElement(dimensions_elem, 'source_ydimension').text = str(self.source_ydimension)
        return dimensions_elem


class ImageMetrics:
    def __init__(self, sampling_frequency_unit: str, sampling_frequency_plane: str,
                 photo_metric_interpretation: str, bit_per_sample: str,
                 x_sampling_frequency: Optional[int] = None, y_sampling_frequency: Optional[int] = None,
                 ):
        self.sampling_frequency_unit = sampling_frequency_unit
        self.sampling_frequency_plane = sampling_frequency_plane
        self.x_sampling_frequency = x_sampling_frequency
        self.y_sampling_frequency = y_sampling_frequency
        self.photo_metric_interpretation = photo_metric_interpretation
        self.bit_per_sample = bit_per_sample

    def to_xml(self):
        metrics_elem = ET.Element('image_metrics')
        ET.SubElement(metrics_elem, 'samplingfrequencyunit').text = self.sampling_frequency_unit
        ET.SubElement(metrics_elem, 'samplingfrequencyplane').text = self.sampling_frequency_plane
        if self.x_sampling_frequency is not None:
            ET.SubElement(metrics_elem, 'xsamplingfrequency').text = str(self.x_sampling_frequency)
        if self.y_sampling_frequency is not None:
            ET.SubElement(metrics_elem, 'ysamplingfrequency').text = str(self.y_sampling_frequency)
        ET.SubElement(metrics_elem, 'photometricinterpretation').text = self.photo_metric_interpretation
        ET.SubElement(metrics_elem, 'bitpersample').text = self.bit_per_sample
        return metrics_elem


class Format:
    def __init__(self, name: str, mime: str, compression: Optional[str] = None):
        self.name = name
        self.mime = mime
        self.compression = compression

    def to_xml(self):
        format_elem = ET.Element('format')
        ET.SubElement(format_elem, 'name').text = self.name
        ET.SubElement(format_elem, 'mime').text = self.mime
        if self.compression is not None:
            ET.SubElement(format_elem, 'compression').text = self.compression
        return format_elem


class ImageCreation:
    def __init__(self, sourcetype: Optional[str] = None, scanningagency: Optional[str] = None,
                 devicesource: Optional[str] = None, scanner_manufacturer: Optional[str] = None,
                 scanner_model: Optional[str] = None, capture_software: Optional[str] = None):
        self.sourcetype = sourcetype
        self.scanningagency = scanningagency
        self.devicesource = devicesource
        self.scanner_manufacturer = scanner_manufacturer
        self.scanner_model = scanner_model
        self.capture_software = capture_software

    def to_xml(self):
        scanning_elem = ET.Element('scanning')
        if self.sourcetype is not None:
            ET.SubElement(scanning_elem, 'sourcetype').text = self.sourcetype
        if self.scanningagency is not None:
            ET.SubElement(scanning_elem, 'scanningagency').text = self.scanningagency
        if self.devicesource is not None:
            ET.SubElement(scanning_elem, 'devicesource').text = self.devicesource
        if self.scanner_manufacturer or self.scanner_model or self.capture_software:
            system_elem = ET.SubElement(scanning_elem, 'scanningsystem')
            ET.SubElement(system_elem, 'scanner_manufacturer').text = self.scanner_manufacturer
            ET.SubElement(system_elem, 'scanner_model').text = self.scanner_model
            ET.SubElement(system_elem, 'capture_software').text = self.capture_software
        return scanning_elem


# Definizione della classe ALT_IMG
class AltImg:
    def __init__(self, file: str, md5: NISOChecksum, image_dimensions: ImageDimensions, usage: Optional[List[str]] = None,
                 filesize: Optional[int] = None, image_metrics: Optional[ImageMetrics] = None,
                 ppi: Optional[int] = None, dpi: Optional[int] = None, format: Optional[Format] = None,
                 scanning: Optional[ImageCreation] = None, datetimecreated: Optional[str] = None,
                 imggroupID: Optional[str] = None):
        self.file = file
        self.md5 = md5
        self.image_dimensions = image_dimensions
        self.usage = usage if usage else []
        self.filesize = filesize
        self.image_metrics = image_metrics
        self.ppi = ppi
        self.dpi = dpi
        self.format = format
        self.scanning = scanning
        self.datetimecreated = datetimecreated
        self.imggroupID = imggroupID

    def to_xml(self):
        altimg_elem = ET.Element('altimg')

        for use in self.usage:
            ET.SubElement(altimg_elem, 'usage').text = use

        ET.SubElement(altimg_elem, 'file').text = self.file
        ET.SubElement(altimg_elem, 'md5').text = str(self.md5)

        if self.filesize is not None:
            ET.SubElement(altimg_elem, 'filesize').text = str(self.filesize)

        altimg_elem.append(self.image_dimensions.to_xml())

        if self.image_metrics is not None:
            altimg_elem.append(self.image_metrics.to_xml())

        if self.ppi is not None:
            ET.SubElement(altimg_elem, 'ppi').text = str(self.ppi)

        if self.dpi is not None:
            ET.SubElement(altimg_elem, 'dpi').text = str(self.dpi)

        if self.format is not None:
            altimg_elem.append(self.format.to_xml())

        if self.scanning is not None:
            altimg_elem.append(self.scanning.to_xml())

        if self.datetimecreated is not None:
            ET.SubElement(altimg_elem, 'datetimecreated').text = self.datetimecreated

        if self.imggroupID is not None:
            altimg_elem.set('imggroupID', self.imggroupID)

        return altimg_elem
