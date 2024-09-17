import copy
import re
import threading
import tkinter as tk
from enum import Enum
from tkinter import ttk, messagebox, simpledialog
import os
import Utils
from frames.CustomFrame import CustomFrame
from model.IMG import IMG, AltImg, ImageGroup, Format, FormatName, MimeType, CompressionType
from scanner.Scanner import Scanner
from scanner.ScannerFactory import ScannerFactory


class XmlOption(Enum):
    ONE_PROJECT_FILE = "Unico file XML a livello di progetto"
    EACH_FOLDER_FILE = "Un file XML per ogni cartella"
    BOTH = "Entrambe le opzioni (unico file XML a livello di progetto, un file XML per ogni cartella)"


class FrameSCAN(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, is_ocr_recognition=False, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame='Scansione',
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )
        self.img_groups = []
        self.controller = controller
        self.scanner_running = False
        self.is_ocr_recognition = is_ocr_recognition
        self.img_dict = dict()
        self.path_var = tk.StringVar()
        self.xml_option = tk.StringVar()
        self.xml_option.set(XmlOption.ONE_PROJECT_FILE.value)
        self.img_dict_folder_dict = {}
        self._init_widgets()

    def _init_widgets(self):
        super().disable_right_button()

        label = ttk.Label(self.container_frame, text="Scegli come generare i file XML:")
        label.pack(padx=20, pady=0)

        options = [option.value for option in XmlOption]
        self.option_menu = ttk.OptionMenu(self.container_frame, self.xml_option, options[0], *options)
        self.option_menu.pack(padx=20, pady=(5, 20))

        button_frame = tk.Frame(self.container_frame)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Avvia scansione", command=self.start_scanning)
        self.start_button.grid(row=1, column=0, padx=5, pady=10)

        self.stop_button = ttk.Button(button_frame, text="Ferma scansione", command=self.stop_scanning,
                                      state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=5, pady=10)

        self.progress_bar = ttk.Progressbar(
            self.container_frame,
            orient="horizontal",
            mode="determinate",
        )
        self.progress_bar.pack(pady=10, padx=100, fill=tk.X)

        self.status_label = ttk.Label(self.container_frame, text="stato scansione")
        self.status_label.pack(pady=10)

    def start_scanning(self):
        # Disabilita il bottone destro
        super().disable_right_button()

        # Ottieni il percorso selezionato
        self.path_var.set(self.controller.session.get(Utils.KEY_SESSION_FOLDER_PATH, ""))
        if not self.path_var.get():
            messagebox.showwarning("Attenzione", "Seleziona un percorso!")
            return

        # Configura la barra di avanzamento e lo stato
        self.progress_bar["value"] = 0
        self.status_label.config(text="Scansione...")
        self.scanner_running = True
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = "enabled"
        self.option_menu['state'] = "disabled"

        self.nomenclature_dict = self.controller.session.get(Utils.KEY_SESSION_NOMENCLATURE, dict())
        self.img_dict_folder_dict = dict()
        # Avvia lo scanning in un thread separato
        threading.Thread(target=self.scan_files).start()

    def stop_scanning(self):
        self.scanner_running = False
        self.controller.after(0, self.update_ui_after_stop)

    def update_ui_after_stop(self):
        self.progress_bar["value"] = 0
        self.status_label.config(text="stato scannerizzazione")
        self.start_button['state'] = "enabled"
        self.stop_button['state'] = "disabled"
        self.option_menu['state'] = "disabled"
        super().disable_right_button()
        self.controller.update_idletasks()

    def scan_files(self):
        path = self.path_var.get()
        total_files = sum([len(files) for r, d, files in os.walk(path)])
        scanned_files = 0
        self.img_dict = dict()
        self.img_groups = []
        imagegroupID = None
        usage = None
        side = self.controller.session.get(Utils.KEY_SESSION_SIDE, None)
        scanning = self.controller.session.get(Utils.KEY_SESSION_SCANNING, None)
        target = self.controller.session.get(Utils.KEY_SESSION_TARGET, None)
        scale = self.controller.session.get(Utils.KEY_SESSION_SCALE, None)
        if self.xml_option.get() != XmlOption.EACH_FOLDER_FILE.value:
            # Primo passaggio: scansiona solo le cartelle con file .tiff o .tif
            for root, dirs, files in os.walk(path):
                if not self.scanner_running:
                    break
                # Ordina i file in base al numero contenuto nel nome
                files = self.sort_files_by_number(files)
                # Verifica se la cartella contiene file .tiff o .tif
                tiff_files = [f for f in files if f.lower().endswith(('.tiff', '.tif'))]
                if tiff_files:
                    scanned_files = self.scan_folder(root, files, side, scanning, target, scale, imagegroupID,
                                                     usage, scanned_files, total_files)

        # Secondo passaggio: scansiona tutte le altre cartelle
        for root, dirs, files in os.walk(path):
            if not self.scanner_running:
                break
            # Ordina i file in base al numero contenuto nel nome
            files = self.sort_files_by_number(files)
            if self.xml_option.get() != XmlOption.EACH_FOLDER_FILE.value:
                # Salta le cartelle già scansionate nel primo passaggio
                tiff_files = [f for f in files if f.lower().endswith(('.tiff', '.tif'))]
                if tiff_files:
                    continue

            scanned_files = self.scan_folder(root, files, side, scanning, target, scale, imagegroupID, usage,
                                             scanned_files, total_files)

        if self.scanner_running:
            super().enable_right_button()
        self.scanner_running = False

    def scan_folder(self, root, files, side, scanning, target, scale, imagegroupID, usage, scanned_files,
                    total_files):
        old_dir = ""
        image_metrics = None
        img_group = None
        index_nomenclature_carta = -1
        old_nomenclature = ""
        current_dir = ""
        current_dir_img_dict = None
        if self.xml_option.get() != XmlOption.ONE_PROJECT_FILE.value:
            current_dir_img_dict = dict()
        for filename in files:
            if not self.scanner_running:
                break

            filename_without_extension, file_extension = os.path.splitext(filename)
            file_path = os.path.join(root, filename)
            current_dir = os.path.dirname(file_path)
            scanner: Scanner = ScannerFactory.factory(file_extension)
            if scanner is not None:
                if current_dir != old_dir:
                    image_metrics = None
                    format = None
                    imagegroupID, usage = self.ask_imgroupID_usage_value(
                        field_imagegroupID=f'imagegroupID della cartella \"{current_dir.split('/')[-1]}\"',
                        field_usage=f'usage della cartella \"{current_dir.split('/')[-1]}\"',
                        values=['ImgGrp_S', 'ImgGrp_M', 'ImgGrp_H', 'ImgGrp_T'],
                        options=[
                            ('1', 'Master'),
                            ('2', 'Alta risoluzione'),
                            ('3', 'Bassa risoluzione'),
                            ('4', 'Preview'),
                            ('a', 'Il repository non ha il copyright dell\'oggetto digitale'),
                            ('b', 'Il repository ha il copyright dell\'oggetto digitale')
                        ]
                    )
                    if file_extension.lower() in [".tiff", ".tif"]:
                        format = Format(name=FormatName.TIF, mime=MimeType.TIFF, compression=CompressionType.LZW)
                    elif file_extension.lower() in [".jpg", ".jpeg"]:
                        format = Format(name=FormatName.JPG, mime=MimeType.JPEG, compression=CompressionType.JPG)
                    img_group = ImageGroup(
                        imggroupID=imagegroupID,
                        image_metrics=image_metrics,
                        dpi=None,
                        ppi=None,
                        scanning=scanning,
                        format=format
                    )
                    self.img_groups.append(img_group)

                metadata_dict = scanner.scan(file_path)

                md5 = metadata_dict.get('MD5', None)
                size = metadata_dict.get('FILE_SIZE', None)
                datetimecreated = Utils.find_date_value(metadata_dict=metadata_dict)
                image_dimensions = Utils.get_image_dimensions(metadata_dict=metadata_dict)
                if image_metrics is None:
                    image_metrics = Utils.get_image_metrics(metadata_dict=metadata_dict)
                if img_group is not None and img_group.get_image_metrics() is None:
                    img_group.set_image_metrics(image_metrics)
                ppi, dpi = Utils.get_ppi_dpi(metadata_dict)
                if dpi is not None and img_group is not None and img_group.get_dpi() is None:
                    img_group.set_dpi(dpi)
                if ppi is not None and img_group is not None and img_group.get_ppi() is None:
                    img_group.set_ppi(ppi)

                nomenclature = self.find_nomenclature_by_filename(
                    file_name=os.path.splitext(os.path.basename(file_path))[0])
                if nomenclature is None:
                    if "carta" in old_nomenclature.lower():
                        if index_nomenclature_carta == -1:
                            match = re.search(r'\d+', old_nomenclature.lower())
                            if match:
                                index_nomenclature_carta = int(match.group(0))  # Converti il risultato in intero
                            else:
                                index_nomenclature_carta = 1
                        nomenclature = f"Carta {index_nomenclature_carta} {"verso" if "recto" in old_nomenclature.lower() else "recto"}"
                        if "verso" in nomenclature.lower():
                            index_nomenclature_carta += 1
                    else:
                        nomenclature = filename_without_extension
                old_nomenclature = nomenclature
                if not (file_extension.lower() in ['.tiff',
                                                   '.tif'] and self.xml_option.get() == XmlOption.EACH_FOLDER_FILE.value) \
                        or (file_extension.lower() not in ['.tiff',
                                                           '.tif'] and self.xml_option.get() == XmlOption.ONE_PROJECT_FILE.value):
                    img = IMG(
                        imggroupID=imagegroupID if imagegroupID is not None else 'ImgGrp_S',
                        nomenclature=nomenclature,
                        file=file_path,
                        datetimecreated=datetimecreated,
                        md5=md5,
                        filesize=size,
                        dpi=dpi,
                        ppi=ppi,
                        usage=usage if usage is not None else '1',
                        side=side,
                        target=target,
                        scale=scale,
                        image_dimensions=image_dimensions,
                    )
                    if (self.xml_option.get() == XmlOption.ONE_PROJECT_FILE.value or
                        self.xml_option.get() == XmlOption.BOTH.value) and file_extension.lower() in ['.tiff','.tif']:
                        self.img_dict[filename_without_extension] = img
                    if self.xml_option.get() != XmlOption.ONE_PROJECT_FILE.value and current_dir_img_dict is not None:
                        if file_extension.lower() not in ['.tiff', '.tif']:
                            current_dir_img_dict[filename_without_extension] = img
                        else:
                            current_dir_img_dict[filename_without_extension] = copy.deepcopy(img)
                if file_extension.lower() not in ['.tiff', '.tif'] and (
                        self.xml_option.get() == XmlOption.BOTH.value or self.xml_option.get() == XmlOption.ONE_PROJECT_FILE.value):
                    alt_img = AltImg(
                        imggroupID=imagegroupID if imagegroupID is not None else 'ImgGrp_S',
                        file=file_path,
                        datetimecreated=datetimecreated,
                        md5=md5,
                        dpi=dpi,
                        ppi=ppi,
                        filesize=size,
                        usage=usage if usage is not None else ['1'],
                        image_dimensions=image_dimensions,
                    )
                    if filename_without_extension in self.img_dict:
                        self.img_dict[filename_without_extension].add_alt_img(alt_img)

            # Aggiorna la barra di progresso dopo aver processato il file
            scanned_files += 1
            progress = (scanned_files / total_files) * 100
            self.update_progress(progress, scanned_files, total_files)
            old_dir = current_dir
        if self.xml_option.get() != XmlOption.ONE_PROJECT_FILE.value and current_dir_img_dict and current_dir:
            self.img_dict_folder_dict[current_dir] = (current_dir_img_dict, img_group)
        return scanned_files

    def update_progress(self, progress, scanned_files, total_files):
        if self.scanner_running:
            self.progress_bar["value"] = progress
            self.status_label.config(text=f"Scannerizzati {scanned_files} su {total_files} files")
            self.controller.update_idletasks()

    def update_status(self, status_text):
        self.status_label.config(text=status_text)
        self.controller.update_idletasks()

    def check_data(self):
        if not self.scanner_running:
            super().save_to_session((Utils.KEY_SESSION_IMG_DICT_PROJECT, self.img_dict))
            super().save_to_session((Utils.KEY_SESSION_IMG_GROUPS, self.img_groups))
            super().save_to_session((Utils.KEY_SESSION_IMG_DICT_FOLDER, self.img_dict_folder_dict))
            super().save_to_session((Utils.KEY_SESSION_GENERATION_OPTION_XML, self.xml_option))
            return True

    def ask_imgroupID_usage_value(self, field_imagegroupID, field_usage, values, options):
        top = tk.Toplevel(self)
        x = self.winfo_x() + self.winfo_width() // 2 - top.winfo_width() // 2
        y = self.winfo_y() + self.winfo_height() // 2 - top.winfo_height() // 2
        top.geometry(f"+{x}+{y}")

        tk.Label(top, text=f'Seleziona il valore per {field_imagegroupID}').pack()
        imggroupID_value = tk.StringVar(value='ImgGrp_S')
        combo = ttk.Combobox(top, textvariable=imggroupID_value, values=values)
        combo.pack(pady=(5, 20))

        tk.Label(top, text=f'Seleziona il valore per {field_usage}').pack(pady=10)
        usage_value = tk.StringVar(value='1')
        for value, text in options:
            radio = ttk.Radiobutton(top, text=text, variable=usage_value, value=value)
            radio.pack(pady=5)

        confirm_button = ttk.Button(top, text="Conferma", command=lambda: top.destroy())
        confirm_button.pack(pady=20)

        top.grab_set()
        top.wait_window(top)

        return imggroupID_value.get(), usage_value.get()

    def set_path(self, path):
        self.path_var.set(path)

    def sort_files_by_number(self, files):
        """Ordina i file in base al numero contenuto nel nome."""

        def extract_number(filename):
            match = re.search(r'(\d+)(?!.*\d)', filename)
            return int(match.group(0)) if match else float('inf')

        return sorted(files, key=extract_number)

    def find_nomenclature_by_filename(self, file_name):
        for path in self.nomenclature_dict:
            current_file_name = os.path.splitext(os.path.basename(path))[0]
            if current_file_name == file_name:
                return self.nomenclature_dict[path]
        return None
