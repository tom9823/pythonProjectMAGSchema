import xml.etree.ElementTree as ET
from enum import Enum
from typing import List, Optional

from model.ObjectXMLSerializable import ObjectXMLSerializable


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


class SamplingFrequencyPlane(Enum):
    CAMERA_SCANNER_FOCAL_PLANE = "1"  # quando non sono definite le dimensioni dell'oggetto
    OBJECT_PLANE = "2"  # quando l'oggetto e la riproduzione hanno la stessa dimensione
    SOURCE_OBJECT_PLANE = "3"  # quando la dimensione della riproduzione è maggiore dell'oggetto originale


class PhotometricInterpretation(Enum):
    WHITE_IS_ZERO = "WhiteIsZero"
    BLACK_IS_ZERO = "BlackIsZero"
    RGB = "RGB"
    PALETTE_COLOR = "Palette color"
    TRANSPARENCY_MASK = "Transparency Mask"
    CMYK = "CMYK"
    YCBCR = "YcbCr"
    CIELAB = "CIELab"


class SamplingFrequencyUnit(Enum):
    NO_UNIT = "1"  # nessuna unità di misura definita
    INCH = "2"  # inch, pollice
    CENTIMETER = "3"  # centimetro


def append_element(parent, tag, value):
    if value is not None:
        if isinstance(value, ObjectXMLSerializable):
            parent.append(value.to_xml())
        else:
            ET.SubElement(parent, tag).text = str(value)


class IMG(ObjectXMLSerializable):
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
        self.alt_imgs = altimg if altimg is not None else []
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

    def add_alt_img(self, alt_img):
        self.alt_imgs.append(alt_img)

    def to_xml(self):

        img_elem = ET.Element('img', attrib={'imggroupID': self._imggroupID})

        append_element(img_elem, 'nomenclature', self._nomenclature)

        for use in self._usage:
            append_element(img_elem, 'usage', use)

        append_element(img_elem, 'sequence_number', self.sequence_number)
        append_element(img_elem, 'side', self._side)
        append_element(img_elem, 'scale', self._scale)
        ET.SubElement(img_elem, 'file', {'Location': "URL", 'xlink': self._file})
        append_element(img_elem, 'md5', self._md5)
        append_element(img_elem, 'filesize', self._filesize)
        append_element(img_elem, 'ppi', self._ppi)
        append_element(img_elem, 'dpi', self._dpi)
        append_element(img_elem, 'datetimecreated', self._datetimecreated)
        append_element(img_elem, 'note', self._note)
        append_element(img_elem, 'holdingsID', self._holdingsID)

        # Process ObjectXMLSerializable properties
        append_element(img_elem, 'image_dimensions', self._image_dimensions)
        append_element(img_elem, 'image_metrics', self._image_metrics)
        append_element(img_elem, 'format', self._format)
        append_element(img_elem, 'scanning', self._scanning)
        append_element(img_elem, 'target', self._target)

        # Process lists of ObjectXMLSerializable
        for alt_img in self.alt_imgs:
            append_element(img_elem, 'altimg', alt_img)

        return img_elem


# Definizione dei tipi semplici e complessi NISO
class NISOChecksum(str):
    def __new__(cls, value):
        if len(value) != 32:
            raise ValueError("Checksum must be 32 characters long")
        return str.__new__(cls, value)


class ImageDimensions(ObjectXMLSerializable):
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


class ImageMetrics(ObjectXMLSerializable):
    def __init__(self, sampling_frequency_unit: SamplingFrequencyUnit, sampling_frequency_plane: SamplingFrequencyPlane,
                 photo_metric_interpretation: PhotometricInterpretation, bit_per_sample: str,
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
        ET.SubElement(metrics_elem, 'samplingfrequencyunit').text = self.sampling_frequency_unit.value
        ET.SubElement(metrics_elem, 'samplingfrequencyplane').text = self.sampling_frequency_plane.value
        if self.x_sampling_frequency is not None:
            ET.SubElement(metrics_elem, 'xsamplingfrequency').text = str(self.x_sampling_frequency)
        if self.y_sampling_frequency is not None:
            ET.SubElement(metrics_elem, 'ysamplingfrequency').text = str(self.y_sampling_frequency)
        ET.SubElement(metrics_elem, 'photometricinterpretation').text = self.photo_metric_interpretation.value
        ET.SubElement(metrics_elem, 'bitpersample').text = self.bit_per_sample
        return metrics_elem


class Format(ObjectXMLSerializable):
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


class Scanning(ObjectXMLSerializable):
    def __init__(self, source_type, scanning_agency, device_source, scanner_manufacturer, scanner_model,
                 capture_software):
        # Elementi opzionali e non ripetibili con valori di default None
        self.sourcetype = source_type
        self.scanningagency = scanning_agency
        self.devicesource = device_source
        self.scanner_manufacturer = scanner_manufacturer
        self.scanner_model = scanner_model
        self.capture_software = capture_software

    def set_sourcetype(self, sourcetype):
        # Settaggio di sourcetype con valori suggeriti
        allowed_values = [
            "negativo",
            "positivo",
            "diapositiva",
            "unicum",
            "fotografia virtuale",
            "vario: .../...",
        ]
        if sourcetype in allowed_values:
            self.sourcetype = sourcetype
        else:
            raise ValueError(f"Valore di sourcetype non valido. Scegli uno tra: {', '.join(allowed_values)}")

    def set_scanningagency(self, scanningagency):
        # Imposta il nome dell'ente o della persona responsabile della scansione
        self.scanningagency = scanningagency

    def set_devicesource(self, devicesource):
        # Imposta il tipo di apparecchiatura di scansione
        self.devicesource = devicesource

    def set_scanning_system(self, scanner_manufacturer, scanner_model, capture_software):
        # Imposta i dettagli del sistema di scansione
        self.scanner_manufacturer = scanner_manufacturer
        self.scanner_model = scanner_model
        self.capture_software = capture_software

    def get_scanning_details(self):
        # Ritorna una rappresentazione stringa dei dettagli di scansione
        return f"""
        Scanning Details:
        Source Type: {self.sourcetype}
        Scanning Agency: {self.scanningagency}
        Device Source: {self.devicesource}
        Scanning System:
            Manufacturer: {self.scanner_manufacturer}
            Model: {self.scanner_model}
            Capture Software: {self.capture_software}
        """

    def to_xml(self):
        # Crea un elemento radice <scanning>
        scanning_element = ET.Element('scanning')

        # Aggiunge l'elemento <niso:sourcetype> se esiste
        if self.sourcetype:
            sourcetype_element = ET.SubElement(scanning_element, 'niso:sourcetype')
            sourcetype_element.text = self.sourcetype

        # Aggiunge l'elemento <niso:scanningagency> se esiste
        if self.scanningagency:
            scanningagency_element = ET.SubElement(scanning_element, 'niso:scanningagency')
            scanningagency_element.text = self.scanningagency

        # Aggiunge l'elemento <niso:devicesource> se esiste
        if self.devicesource:
            devicesource_element = ET.SubElement(scanning_element, 'niso:devicesource')
            devicesource_element.text = self.devicesource

        # Aggiunge il sistema di scansione come elemento complesso <niso:scanningsystem>
        if self.scanner_manufacturer and self.scanner_model and self.capture_software:
            scanningsystem_element = ET.SubElement(scanning_element, 'niso:scanningsystem')

            scanner_manufacturer_element = ET.SubElement(scanningsystem_element, 'niso:scanner_manufacturer')
            scanner_manufacturer_element.text = self.scanner_manufacturer

            scanner_model_element = ET.SubElement(scanningsystem_element, 'niso:scanner_model')
            scanner_model_element.text = self.scanner_model

            capture_software_element = ET.SubElement(scanningsystem_element, 'niso:capture_software')
            capture_software_element.text = self.capture_software

        return scanning_element


# Definizione della classe ALT_IMG
class AltImg(ObjectXMLSerializable):
    def __init__(self, file: str, md5: NISOChecksum, image_dimensions: ImageDimensions,
                 usage: Optional[List[str]] = None,
                 filesize: Optional[int] = None, image_metrics: Optional[ImageMetrics] = None,
                 ppi: Optional[int] = None, dpi: Optional[int] = None, format: Optional[Format] = None,
                 scanning: Optional[Scanning] = None, datetimecreated: Optional[str] = None,
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

        ET.SubElement(altimg_elem, 'file', {'Location': "URL", 'xlink': self.file})
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


class Target(ObjectXMLSerializable):
    def __init__(self, target_type=None, target_id=None, image_data=None, performance_data=None, profiles=None):
        # Initialize with default values
        self.target_type = target_type  # 0 for external, 1 for internal
        self.target_id = target_id  # Name or ID of the target
        self.image_data = image_data  # Path to image data (only for external targets)
        self.performance_data = performance_data  # Path to performance data file
        self.profiles = profiles  # Path to ICC color profile or management profile

    def set_target_type(self, target_type):
        # Validate and set target type
        allowed_values = [0, 1]  # 0: external, 1: internal
        if target_type in allowed_values:
            self.target_type = target_type
        else:
            raise ValueError(f"Valore di targetType non valido. Scegli 0 (esterno) o 1 (interno).")

    def set_target_id(self, target_id):
        # Set the target ID
        if isinstance(target_id, str) and target_id:
            self.target_id = target_id
        else:
            raise ValueError("targetID deve essere una stringa non vuota.")

    def set_image_data(self, image_data):
        # Set the image data path (only for external targets)
        if self.target_type == 0:
            if isinstance(image_data, str):
                self.image_data = image_data
            else:
                raise ValueError("imageData deve essere una stringa valida (path).")
        else:
            raise ValueError("imageData può essere impostato solo per target esterni (targetType = 0).")

    def set_performance_data(self, performance_data):
        # Set the performance data path
        if isinstance(performance_data, str):
            self.performance_data = performance_data
        else:
            raise ValueError("performanceData deve essere una stringa valida (path).")

    def set_profiles(self, profiles):
        # Set the profiles path
        if isinstance(profiles, str):
            self.profiles = profiles
        else:
            raise ValueError("profiles deve essere una stringa valida (path).")

    def get_target_details(self):
        # Return a string representation of the target details
        return f"""
        Target Details:
        Target Type: {'Esterno' if self.target_type == 0 else 'Interno'}
        Target ID: {self.target_id}
        Image Data: {self.image_data or 'N/A'}
        Performance Data: {self.performance_data or 'N/A'}
        Profiles: {self.profiles or 'N/A'}
        """

    def to_xml(self):
        # Create a root element <target>
        target_element = ET.Element('target')

        # Add the element <niso:targetType> if it exists
        if self.target_type is not None:
            target_type_element = ET.SubElement(target_element, 'niso:targetType')
            target_type_element.text = str(self.target_type)

        # Add the element <niso:targetID> if it exists
        if self.target_id:
            target_id_element = ET.SubElement(target_element, 'niso:targetID')
            target_id_element.text = self.target_id

        # Add the element <niso:imageData> if it exists
        if self.image_data:
            image_data_element = ET.SubElement(target_element, 'niso:imageData')
            image_data_element.text = self.image_data

        # Add the element <niso:performanceData> if it exists
        if self.performance_data:
            performance_data_element = ET.SubElement(target_element, 'niso:performanceData')
            performance_data_element.text = self.performance_data

        # Add the element <niso:profiles> if it exists
        if self.profiles:
            profiles_element = ET.SubElement(target_element, 'niso:profiles')
            profiles_element.text = self.profiles

        return target_element


class ImageGroup(ObjectXMLSerializable):
    def __init__(self, image_metrics: Optional[ImageMetrics] = None,
                 ppi: Optional[int] = None, dpi: Optional[int] = None, format: Optional[Format] = None,
                 scanning: Optional[Scanning] = None, imggroupID: Optional[str] = None):
        self.image_metrics = image_metrics
        self.ppi = ppi
        self.dpi = dpi
        self.format = format
        self.scanning = scanning
        self.imggroupID = imggroupID

    def to_xml(self):
        imgroup_elem = ET.Element('img_group')

        if self.image_metrics is not None:
            imgroup_elem.append(self.image_metrics.to_xml())

        if self.ppi is not None:
            ET.SubElement(imgroup_elem, 'ppi').text = str(self.ppi)

        if self.dpi is not None:
            ET.SubElement(imgroup_elem, 'dpi').text = str(self.dpi)

        if self.format is not None:
            imgroup_elem.append(self.format.to_xml())

        if self.scanning is not None:
            imgroup_elem.append(self.scanning.to_xml())

        if self.imggroupID is not None:
            imgroup_elem.set('ID', self.imggroupID)

        return imgroup_elem
