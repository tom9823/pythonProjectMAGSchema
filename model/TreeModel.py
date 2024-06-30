import logging

import xml.etree.ElementTree as ET
from xml.dom import minidom

from it.horigin.mnemosyne.mui.R import R
from it.horigin.mnemosyne.mui.scanner.MetaData import MetaData

class TreeModel:

    TAG_BIB :str = 'bib'
    TAG_GEN :str = 'gen'
    TAG_IMG :str = 'img'

    def __init__(self) -> None:
        self._logger :logging.Logger = logging.getLogger(__name__)
        self._root = ET.Element("metadigit", {
            'xmlns:dc' : "http://purl.org/dc/elements/1.1/",
            'xmlns:niso' : "http://www.niso.org/pdfs/DataDict.pdf",
            'xmlns:xlink' : "http://www.w3.org/TR/xlink",
            'xmlns:xsi' : "http://www.w3.org/2001/XMLSchema-instance",
            'xmlns' : "http://www.iccu.sbn.it/metaAG1.pdf",
            'xsi:schemaLocation' : "http://www.iccu.sbn.it/metaAG1.pdf metadigit.xsd",
            'version' : "2.0.1"
        })
        self._tree = ET.ElementTree(self._root)

        # -- generated by the user
        self._gen = ET.SubElement(self.getRoot(), self.TAG_GEN, {})
        
        # -- generated by the http service
        self._bib = ET.SubElement(self.getRoot(), self.TAG_BIB, {})

    def getRoot(self):
        return self._root
    
    def getTree(self) -> ET.ElementTree:
        return self._tree
    
    def find(self, path) -> ET.SubElement:
        return self.getRoot().find(path)

    def getGen(self) -> ET.SubElement:
        return self.getRoot().find(self.TAG_GEN)
    
    def getBib(self) -> ET.SubElement:
        return self.getRoot().find(self.TAG_BIB)
    
    def addImg(self, path :str, group :str, metadata :list[MetaData]):
        #imggroupID="ImgGrp_H"
        img :ET.SubElement = ET.SubElement(self.getRoot(), self.TAG_IMG, { 'imggroupID' : group })

        for md in metadata:
            meta :MetaData = md

            imgMeta = ET.SubElement(img, meta.key)
            txt :str = ''
            self._logger.info(f"Value that shall be iterated: {meta.values[0]}")
            
            if isinstance(meta.values[0], tuple):
                for v in meta.values[0]:
                    print("value meta: " + str(v))
                    txt += str(v) + ' '
            else:
                txt = str(meta.values[0])

            print("Will write: " + txt)
            imgMeta.text = str(txt)

    
    def addTag(self, parent :ET.SubElement, name :str, text :str = '', attributes :dict[str, str] = {}) -> ET.SubElement:
        element :ET.SubElement = ET.SubElement(
            parent, 
            name,
            attributes
        )
        element.text = text
    
    def treeModelToXML(self, output :str):
        xml_string = ET.tostring(self.getRoot(), encoding=R.encoding.UTF_8, xml_declaration=True).decode()
        try:
            pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

            # Write XML string to file
            with open(output, "w") as file:
                file.write(pretty_xml)
        except Exception as exc:
            self._logger.exception(exc)
            self._logger.error(f"The output during the exception was:\n{xml_string}")

    def toXML(self, output :str):
        xml_string = ET.tostring(self.getRoot(), encoding=R.encoding.UTF_8, xml_declaration=True).decode()
        try:
            pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

            # Write XML string to file
            with open(output, "w") as file:
                file.write(pretty_xml)
        except Exception as exc:
            self._logger.exception(exc)
            self._logger.error(f"The output during the exception was:\n{xml_string}")

    def addAsset(self, root :ET.Element, asset, attribute :dict) -> None:
        node = ET.SubElement(root, R.xml.tag.IMAGE, attribute)
        node.text = asset.path

        metaNode = ET.SubElement(node, R.xml.tag.METADATA)
        for metadata in asset.metadata:
            self.addMeta(metaNode, metadata)

    def addMeta(self, root :ET.Element, metadata) -> None:
        if len(metadata.values):

            # -- FIXME("Make it work")
            #if not metadata.values[0] and self._ignoreEmpty:

            # -- convert
            from it.horigin.mnemosyne.mui.xml.Converter import Converter
            
            metadata.values[0] = Converter.convert(metadata.key, metadata.values[0])

            self._logger.info(f"KEY {metadata.key} VAL {metadata.values[0]}")
            node = ET.SubElement(root, f"{metadata.key}")
            node.text = f'{metadata.values[0]}'