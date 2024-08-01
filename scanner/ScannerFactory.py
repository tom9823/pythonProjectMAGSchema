from scanner.Scanner import Scanner
from scanner.impl.PdfScanner import PdfScanner
from scanner.impl.ImageScanner import ImageScanner


class ScannerFactory:

    @staticmethod
    def factory(extension) -> Scanner:
        if extension.lower() == '.pdf':
            return PdfScanner.getInstance()

        if extension.lower() in [
            '.jpeg', '.jpg', '.png', '.gif','.tif','.tiff',
        ]:
            return ImageScanner.getInstance()
