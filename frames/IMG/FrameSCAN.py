import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import pytesseract
from PIL import Image
import Utils
from frames.CustomFrame import CustomFrame
from model.IMG import IMG
from scanner.MetaData import MetaData
from scanner.Scanner import Scanner
from scanner.ScannerFactory import ScannerFactory


class FrameSCAN(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, is_ocr_recognition=False, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame='Scannerizzazione',
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )
        self.controller = controller
        self.scanner_running = False
        self.is_ocr_recognition = is_ocr_recognition
        self._init_widgets()
        self.img_list = []

    def _init_widgets(self):
        super().disable_right_button()

        path_frame = tk.Frame(self.container_frame)
        path_frame.pack(pady=10)
        self.path_label = ttk.Label(path_frame, text="Select Path:")
        self.path_label.grid(row=0, column=0, padx=5, pady=5)

        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=30)
        self.path_entry.focus()
        self.path_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = ttk.Button(path_frame, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        button_frame = tk.Frame(self.container_frame)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Scanning", command=self.start_scanning)
        self.start_button.grid(row=1, column=0, padx=5, pady=10)

        self.stop_button = ttk.Button(button_frame, text="Stop Scanning", command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=5, pady=10)

        self.progress_bar = ttk.Progressbar(
            self.container_frame,
            orient="horizontal",
            mode="determinate",
            length=300
        )
        self.progress_bar.pack(pady=10)

        self.status_label = ttk.Label(self.container_frame, text="stato scannerizzazione")
        self.status_label.pack(pady=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def start_scanning(self):
        super().disable_right_button()
        if not self.path_var.get():
            messagebox.showwarning("Attenzione", "Seleziona un path!")
            return

        self.progress_bar["value"] = 0
        self.status_label.config(text="Scanning...")
        self.scanner_running = True
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = "enabled"

        threading.Thread(target=self.scan_files).start()

    def stop_scanning(self):
        self.scanner_running = False
        self.controller.after(0, self.update_ui_after_stop)

    def update_ui_after_stop(self):
        self.progress_bar["value"] = 0
        self.status_label.config(text="stato scannerizzazione")
        self.start_button['state'] = "enabled"
        self.stop_button['state'] = "disabled"
        super().disable_right_button()
        self.controller.update_idletasks()

    def scan_files(self):
        path = self.path_var.get()
        total_files = sum([len(files) for r, d, files in os.walk(path)])
        scanned_files = 0
        self.img_list = []
        old_dir = ''
        imagegroupID = None
        usage = None
        for root, dirs, files in os.walk(path):
            if not self.scanner_running:
                break
            for filename in files:
                if not self.scanner_running:
                    break

                _, file_extension = os.path.splitext(filename)
                file_path = os.path.join(root, filename)
                current_dir = os.path.dirname(file_path)
                if self.is_ocr_recognition:
                    if file_extension in [".jpg", ".jpeg", ".png", ".tiff"]:
                        image = Image.open(file_path)
                        text = pytesseract.image_to_string(image)
                        print(text + '\n\n')
                else:
                    scanner: Scanner = ScannerFactory.factory(file_extension)
                    if scanner is not None:
                        if current_dir != old_dir:
                            imagegroupID, usage = self.ask_imgroupID_usage_value(
                                field_imagegroupID=f'imagegroupID della cartella {current_dir}',
                                field_usage=f'usage della cartella {current_dir}',
                                values=['ImgGrp_S', 'ImgGrp_M', 'ImgGrp_H'],
                                options=[
                                    ('1', 'Master'),
                                    ('2', 'Alta risoluzione'),
                                    ('3', 'Bassa risoluzione'),
                                    ('4', 'Preview'),
                                    ('a', 'Il repository non ha il copyright dell\'oggetto digitale'),
                                    ('b', 'Il repository ha il copyright dell\'oggetto digitale')
                                ]
                            )

                        datetimecreated = Utils.get_creation_date(file_path)
                        md5 = Utils.get_file_md5(file_path)
                        size = Utils.get_file_size(file_path)
                        nomenclature = filename
                        img = IMG(
                            imggroupID=imagegroupID if imagegroupID is not None else 'ImgGrp_S',
                            nomenclature=nomenclature,
                            file=file_path,
                            datetimecreated=datetimecreated,
                            md5=md5,
                            filesize=size,
                            usage=usage if usage is not None else '1'
                        )
                        print(filename)
                        metas: list[MetaData] = scanner.scan(file_path)
                        datetimecreated = Utils.find_date_value(metas)
                        if datetimecreated is not None:
                            img.set_datetimecreated(datetimecreated)
                        image_dimensions = Utils.get_image_dimensions(metas)
                        if image_dimensions is not None:
                            img.set_image_dimensions(image_dimensions)
                        xmp_object = Utils.extract_xmp_metadata(metadata_list=metas)
                        if xmp_object is not None:
                            print(xmp_object)
                        self.img_list.append(img)
                scanned_files += 1
                old_dir = current_dir

                progress = (scanned_files / total_files) * 100
                self.update_progress(progress, scanned_files, total_files)

        if self.scanner_running:
            super().enable_right_button()
        self.scanner_running = False

    def update_progress(self, progress, scanned_files, total_files):
        if self.scanner_running:
            self.progress_bar["value"] = progress
            self.status_label.config(text=f"Scanned {scanned_files} of {total_files} files")
            self.controller.update_idletasks()

    def update_status(self, status_text):
        self.status_label.config(text=status_text)
        self.controller.update_idletasks()

    def check_data(self):
        if not self.scanner_running:
            super().save_to_session((Utils.KEY_SESSION_IMG, self.img_list))
            return True

    def ask_imgroupID_usage_value(self, field_imagegroupID, field_usage, values, options):
        top = tk.Toplevel()
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