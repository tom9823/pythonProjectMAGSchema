from scanner.impl.ImageScanner import ImageScanner


class ScannerFactory:

    @staticmethod
    def factory(extension):
        if extension.lower() in [
            '.jpeg', '.jpg', '.png', '.gif','.tif','.tiff',
        ]:
            return ImageScanner.getInstance()
