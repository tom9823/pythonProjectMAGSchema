from scanner.Scanner import Scanner
from scanner.impl.PdfScanner import PdfScanner
from scanner.impl.SimpleImageScanner import SimpleImageScanner
from scanner.impl.TiffScanner import TiffScanner


class ScannerFactory:

    @staticmethod
    def factory(extension :str) -> Scanner:
        if extension.lower() == '.pdf':
            return PdfScanner.getInstance()

        if extension.lower() in [
            '.jpeg', '.jpg', '.png', '.gif',
        ]:
            return SimpleImageScanner.getInstance()

        if extension.lower() in ['.tiff']:
            return TiffScanner.getInstance()
