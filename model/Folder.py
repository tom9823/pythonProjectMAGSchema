import ET


class Folder(object):


    def __init__(self, name):
        self.children = []
        self.name = name
        self.parent = None
        self.elementTree = None
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def print_xml(self, xml_string, xmlGenType):
        if self.name == 'root':
            self.elementTree = ET.Element(
                'metadigit',
                {
                    'xmlns:dc': "http://purl.org/dc/elements/1.1/",
                    'xmlns:niso': "http://www.niso.org/pdfs/DataDict.pdf",
                    'xmlns:xlink': "http://www.w3.org/TR/xlink",
                    'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                    'xmlns': "http://www.iccu.sbn.it/metaAG1.pdf",
                    'xsi:schemaLocation': "http://www.iccu.sbn.it/metaAG1.pdf metadigit.xsd",
                    'version': "2.0.1"
                }
            )

            # L'elemento <gen> è il primo figlio dell'elemento root <metadigit> ed è obbligatorio.
            # Esso contiene una serie di elementi figli che contengono informazioni relative all'istituzione
            # responsabile del progetto di digitalizzazione, al progetto stesso, alla completezza o integrità
            # del file, all'accessibilità dell'oggetto (o gli oggetti) descritto nella sezione BIB.
            # L'elemento, inoltre, può contenere informazioni tecniche condivise da più oggetti
            # descritti dal documento MAG. L'elemento non è ripetibile.
            genRootElement = ET.SubElement(self.elementTree, 'gen')

            creation_date, modification_date = DataUtils.getFolderMeta(folder_path)
            if creation_date is not None:
                genRootElement.set('creation', creation_date)
            if modification_date is not None:
                genRootElement.set('last_update', modification_date)

            # stprog: indicazione del progetto di digitalizzazione; l'elemento è obbligatorio e non ripetibile
            stprog = ET.SubElement(genRootElement, 'stprog')
            # collection: riferimento alla collezione di cui la risorsa digitale farà parte; l'elemento è opzionale e non ripetibile
            collection = ET.SubElement(genRootElement, 'collection')
            # agency: agenzia responsabile del processo di digitalizzazione; l'elemento è obbligatorio e non ripetibile
            agency = ET.SubElement(genRootElement, 'agency')
            # access_rights: condizioni di accesso all'oggetto descritto nella sezione BIB; l'elemento è obbligatorio e non ripetibile
            access_rights = ET.SubElement(genRootElement, 'access_rights')
            # completeness: completezza della digitalizzazione; l'elemento è obbligatorio e non ripetibile
            completeness = ET.SubElement(genRootElement, 'completeness')
            # img_group: caratteristiche comuni a gruppi omogenei di immagini; l'elemento è opzionale e ripetibile
            img_group = ET.SubElement(genRootElement, 'img_group')
            # audio_group: caratteristiche comuni a gruppi omogenei di file audio; l'elemento è opzionale e ripetibile
            audio_group = ET.SubElement(genRootElement, 'audio_group')
            # video_group: caratteristiche comuni a gruppi omogenei di file video; l'elemento è opzionale e ripetibile
            video_group = ET.SubElement(genRootElement, 'video_group')


            # L'elemento <bib> è il secondo figlio dell'elemento root <metadigit> ed è obbligatorio. Esso contiene una serie di elementi figli che raccolgono metadati descrittivi relativamente all'oggetto analogico digitalizzato o, nel caso di documenti born digital,relativamente al documento stesso. L'elemento non è ripetibile.
            bibRootElement = ET.SubElement(self.elementTree, 'bib')
            bibRootElement.set('level',  )

            dc_tags = [
                'dc:title',
                'dc:creator',
                'dc:subject',
                'dc:description',
                'dc:publisher',
                'dc:contributor',
                'dc:date',
                'dc:type',
                'dc:format',
                'dc:identifier',
                'dc:source',
                'dc:language',
                'dc:relation',
                'dc:coverage',
                'dc:rights'
            ]

            for tag in dc_tags:
                ET.subElement(bibRootElement, tag)
            # holdings: raccoglie le informazioni relative all'Istituzione che possiede l'oggetto analogico. L'elemento è opzionale e ripetibile
            holdings: ET = ET.subElement(bibRootElement, 'holdings')
            # ID : di tipo xsd:ID, serve a definire un identificatore univoco all'interno del record MAG
            # cui è possibile fare riferimento da altri luoghi del medesimo record. L'attributo trova la
            # sua utilità qualora vi sia la necessità di dichiarare diversi <holdings>
            holdings.set('ID',)
            # library: contiene il nome dell'istituzione proprietaria dell'oggetto analogico o di
            # parte dell'oggetto analogico. Di tipo xsd:string, è opzionale e non ripetibile.
            library_element =  ET.SubElement(holdings, 'library')
            library_element.text = 'library'
            # inventory_number: contiene il numero di inventario attribuito all'oggetto analogico
            # dall'istituzione che lo possiede. Di tipo xsd:string, è opzionale e non ripetibile.
            inventory_number_element = ET.SubElement(holdings, 'inventory_number')
            inventory_number_element.text = "Your inventory number here"  # Specificare il numero di inventario
            # shelfmark: contiene la collocazione dell'oggetto digitale all'interno del catalogo
            # dell'istituzione che lo possiede. Di tipo xsd:string, è opzionale e ripetibile. Per
            # l'elemento è definito un attributo:
            shelfmark_element = ET.SubElement(library_element, 'shelfmark')
            shelfmark_element.text = "Your first shelfmark here"
            # type: Si usa per definire il tipo di collocazione nel caso di collocazioni plurime, per
            # esempio quando si vuole registrare una collocazione antica e una moderna.
            # L'attributo è opzionale e il suo contenuto è xsd:string.
            shelfmark_element.set('type', '')
            # Alcuni progetti di digitalizzazione che hanno adottato MAG come standard per la
            # raccolta dei metadati amministrativi e gestionali, hanno messo in evidenza la necessità di
            # dotare lo schema di alcuni elementi per la raccolta di particolari informazioni specialistiche
            # relativamente all'oggetto analogico raccolte durante il processo di digitalizzazione. Tali
            # informazioni non potevano essere agevolmente codificate all'interno del set Dublin Core
            # poiché la scelta di non avvalersi degli elementi Dublin Core qualificati rendevano
            # difficilmente identificabili tali contenuti. È stato perciò creato l'elemento <local_bib> di tipo
            # xsd:sequence, per il quale non sono definiti attributi. L'elemento è opzionale così pure come
            # gli elementi ivi contenuti
            local_bib = ET.subElement(bibRootElement, 'local_bib')
            # geo_coord : di tipo xsd:string, contiene le coordinate geografiche relative a una
            # carta o a una mappa. L'elemento è opzionale e ripetibile. Non sono definiti attributi.
            local_bib.set('geo_coord')
            # not_date : di tipo xsd:string, contiene la data di notifica relativa a un bando o a un
            # editto. L'elemento è opzionale e ripetibile. Non sono definiti attributi
            local_bib.set('not_date', )
        isLastLevel = True
        xml_string_single_folder = ""
        for child in self.children:
            isLastLevel &= isinstance(child, File)
            xml_string_single_folder += child.print_xml(xml_string, xmlGenType)

        if isLastLevel and xmlGenType != 'Genera XML del progetto':
            albero_xml = ET.ElementTree(ET.fromstring(xml_string_single_folder))
            albero_xml.write("singola_cartella.xml")



class File(Folder):
    metadata: list[MetaData]
    def __init__(self, nome ):
        super().__init__(nome)

    def add_metadata(self, metadata):
        self.metadata.append(metadata)

    def print_xml(self, xml_str, xmlGenType):







