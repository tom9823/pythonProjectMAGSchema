import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse

import Utils
from frames.BIB.FrameDC import FrameDC
from frames.BIB.FrameHolding import FrameHolding
from frames.BIB.FrameLocalBIB import FrameLocalBIB
from frames.BIB.FramePiece import FramePiece
from frames.FrameGEN import FrameGEN
from frames.FrameINIT import FrameINIT
from frames.IMG.FrameIMG import FrameIMG
from frames.IMG.FrameIMG2 import FrameIMG2
from frames.IMG.FrameNomenclature import FrameNomenclature
from frames.IMG.FrameSCAN import FrameSCAN
import xml.etree.ElementTree as ET


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Standard MAG")
        self.geometry('1080x720')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frames = dict()
        self.session = dict()
        self.identifier_modal_already_shown = True

        frameGEN = FrameGEN(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_GEN, container=Utils.KEY_FRAME_INIT),
            left_button_title='INIT',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_GEN, container=Utils.KEY_FRAME_DC),
            right_button_title='DC'
        )
        frameGEN.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_GEN] = frameGEN

        frameDC = FrameDC(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_DC, container=Utils.KEY_FRAME_GEN),
            left_button_title='GEN',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_DC, container=Utils.KEY_FRAME_HOLDING),
            right_button_title='HOLDING'
        )
        frameDC.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_DC] = frameDC

        frameHolding = FrameHolding(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_HOLDING, container=Utils.KEY_FRAME_DC),
            left_button_title='DC',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_HOLDING,
                                                        container=Utils.KEY_FRAME_LOCAL_BIB),
            right_button_title='LOCALBIB'
        )
        frameHolding.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_HOLDING] = frameHolding

        frameLocalBIB = FrameLocalBIB(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_LOCAL_BIB,
                                                       container=Utils.KEY_FRAME_HOLDING),
            left_button_title='HOLDING',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_LOCAL_BIB,
                                                        container=Utils.KEY_FRAME_PIECE),
            right_button_title='PIECE'
        )
        frameLocalBIB.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_LOCAL_BIB] = frameLocalBIB

        framePiece = FramePiece(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_PIECE,
                                                       container=Utils.KEY_FRAME_LOCAL_BIB),
            left_button_title='LOCALBIB',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_PIECE, container=Utils.KEY_FRAME_IMG),
            right_button_title='IMG'
        )
        framePiece.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_PIECE] = framePiece

        frameIMG = FrameIMG(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_IMG,
                                                       container=Utils.KEY_FRAME_PIECE),
            left_button_title='PIECE',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_IMG, container=Utils.KEY_FRAME_IMG_2),
            right_button_title='IMG 2'
        )
        frameIMG.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_IMG] = frameIMG

        frameIMG2 = FrameIMG2(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_IMG_2,
                                                       container=Utils.KEY_FRAME_IMG),
            left_button_title='IMG 1',
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_IMG_2,
                                                        container=Utils.KEY_FRAME_NOMENCLATURE),
            right_button_title='NOMENCLATURE'
        )
        frameIMG2.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_IMG_2] = frameIMG2

        frameNomenclature = FrameNomenclature(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_SCAN, container=Utils.KEY_FRAME_IMG_2),
            left_button_title="IMG 2",
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_SCAN, container=Utils.KEY_FRAME_SCAN),
            right_button_title="SCAN",
        )

        frameNomenclature.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_NOMENCLATURE] = frameNomenclature

        frameSCAN = FrameSCAN(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_SCAN,
                                                       container=Utils.KEY_FRAME_NOMENCLATURE),
            left_button_title="NOMENCLATURE",
            right_button_action=self.generate_file_xml,
            right_button_title="Genera file XML",
            is_ocr_recognition=False
        )
        frameSCAN.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_SCAN] = frameSCAN

        frameSCAN = FrameSCAN(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_SCAN, container=Utils.KEY_FRAME_INIT),
            left_button_title="INIT",
            right_button_action=lambda: {},
            right_button_title="Visualizza",
            is_ocr_recognition=True
        )
        frameSCAN.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_SCAN_OCR_RECOGNITION] = frameSCAN

        frameINIT = FrameINIT(
            parent=self,
            controller=self,
            left_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_INIT, container=Utils.KEY_FRAME_GEN),
            left_button_title="Genera file XML",
            right_button_action=lambda: self.show_frame(caller=Utils.KEY_FRAME_INIT,
                                                        container=Utils.KEY_FRAME_SCAN_OCR_RECOGNITION),
            right_button_title="Riconoscimento OCR"
        )
        frameINIT.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[Utils.KEY_FRAME_INIT] = frameINIT

        self.show_frame(caller=Utils.KEY_MAIN_WINDOW, container=Utils.KEY_FRAME_INIT)

    def show_frame(self, caller, container):
        frame = self.frames[container]
        if caller == Utils.KEY_FRAME_INIT and container == Utils.KEY_FRAME_GEN and not self.identifier_modal_already_shown:
            frame.show_identifier_modal()
            self.identifier_modal_already_shown = True
        frame.tkraise()

    def generate_file_xml(self):
        # Creare l'elemento principale
        metadigit = ET.Element("metadigit", attrib={
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
            "xmlns:niso": "http://www.niso.org/pdfs/DataDict.pdf",
            "xmlns:xlink": "http://www.w3.org/TR/xlink",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns": "http://www.iccu.sbn.it/metaAG1.pdf",
            "xsi:schemaLocation": "http://www.iccu.sbn.it/metaAG1.pdf metadigit.xsd",
            "version": "2.0.1"
        })

        # Aggiungere il sottotag <gen>
        self._attach_gen_tag(metadigit)

        # Aggiungere il sottotag <bib>
        self._attach_bib_tag(metadigit)

        self._attach_img_tag(metadigit)

        # Convertire l'albero degli elementi XML in una stringa
        xml_content = ET.tostring(metadigit, encoding="unicode", method="xml")
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        # Controlla se l'utente ha scelto un percorso
        if file_path:
            with open(file_path, "w",
                      encoding="utf-8") as file:
                file.write(xml_declaration)
                file.write(xml_content)
            self.destroy()

    def _attach_gen_tag(self, metadigit):
        gen = ET.SubElement(metadigit, "gen", attrib={
            "creation": str(self.session.get('Creation', '')),
            "last_update": str(self.session.get('Last Update', '')),
        })
        stprog = ET.SubElement(gen, "stprog")
        stprog.text = str(self.session.get('Progetto di Digitalizzazione', ''))

        collection = ET.SubElement(gen, "collection")
        collection.text = str(self.session.get('Collezione', ''))

        agency = ET.SubElement(gen, "agency")
        agency.text = str(self.session.get('Agenzia', ''))

        access_rights = ET.SubElement(gen, "access_rights")
        access_rights.text = str(self.session.get('Condizioni di Accesso', ''))

        completeness = ET.SubElement(gen, "completeness")
        completeness.text = str(self.session.get('Completezza', ''))

        for img_group in self.session.get(Utils.KEY_SESSION_IMG_GROUPS, []):
            gen.append(img_group.to_xml())

    def _attach_bib_tag(self, metadigit):
        # Creare il tag <bib>
        bib = ET.SubElement(metadigit, "bib", attrib={
            "level": str(self.session.get('Level', ''))
        })

        # Aggiungere i sottotag di <bib> con prefisso dc:
        for dc in self.session.get(Utils.KEY_SESSION_DC, []):
            tag, value = dc
            dc_tag = ET.SubElement(bib, f"dc:{tag.lower()}")
            dc_tag.text = value

        # aggiungere i sottotag di <bib> holding
        for holding in self.session.get(Utils.KEY_SESSION_HOLDING, []):
            holdings_element = ET.SubElement(bib, "holdings", ID=holding.holding_id)

            # Crea il sotto-elemento library
            library_element = ET.SubElement(holdings_element, "library")
            library_element.text = holding.get_library()

            # Crea il sotto-elemento inventory_number
            inventory_number_element = ET.SubElement(holdings_element, "inventory_number")
            inventory_number_element.text = holding.get_inventory_number()

            # Crea i sotto-elementi shelfmark
            for shelfmark in holding.shelfmarks:
                shelfmark_element = ET.SubElement(holdings_element, "shelfmark", type=shelfmark.get_type())
                shelfmark_element.text = shelfmark.get_value()

            # aggiungere i sottotag di <bib> local_bib
            for local_bib in self.session.get(Utils.KEY_SESSION_LOCAL_BIB, []):
                local_bib_element = ET.SubElement(bib, "local_bib")
                for geo_coord in local_bib.get_geo_coords():
                    geo_coord_element = ET.SubElement(local_bib_element, "geo_coord")
                    geo_coord_element.text = geo_coord
                for not_date in local_bib.get_not_dates():
                    not_date_element = ET.SubElement(local_bib_element, "not_date")
                    not_date_element.text = not_date

            # aggiungere i sottotag di <bib> piece
            piece = self.session.get(Utils.KEY_FRAME_PIECE, None)
            piece_element = ET.SubElement(bib, "bib")
            if piece == Utils:
                if piece.get_pubblicazioni_seriali():
                    year_element = ET.SubElement(piece_element, "year")
                    year_element.text = piece.get_year()
                    issue_element = ET.SubElement(piece_element, "issue")
                    issue_element.text = piece.get_year()
                    if piece.get_stpiece_per():
                        stpiece_per_element = ET.SubElement(piece_element, "stpiece_per")
                        stpiece_per_element.text = piece.get_stpiece_per()
                else:
                    part_number_element = ET.SubElement(piece_element, "part_number")
                    part_number_element.text = piece.get_year()
                    part_name_element = ET.SubElement(piece_element, "part_name")
                    part_name_element.text = piece.get_year()
                    if piece.get_stpiece_vol():
                        stpiece_vol_element = ET.SubElement(piece_element, "stpiece_vol")
                        stpiece_vol_element.text = piece.get_stpiece_vol()

    def _attach_img_tag(self, metadigit):
        for img in self.session.get(Utils.KEY_SESSION_IMG, []):
            metadigit.append(img.to_xml())


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
