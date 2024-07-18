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
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )
        self.controller = controller
        self.scanner_running = False
        self._files_scanning_job = None
        self.is_ocr_recognition = is_ocr_recognition
        self._init_widgets()
        self.img_list = []

    def _init_widgets(self):
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

        self.reset_button = ttk.Button(button_frame, text="Reset scan", command=self.reset_scanning)
        self.reset_button.grid(row=1, column=2, padx=5, pady=10)

        self.progress_bar = ttk.Progressbar(self.container_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(pady=10)

        self.status_label = ttk.Label(self.container_frame, text="")
        self.status_label.pack(pady=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def start_scanning(self):
        if not self.path_var.get():
            messagebox.showwarning("Attenzione", "Seleziona un path!")
            return

        self.progress_bar["value"] = 0
        self.status_label.config(text="Scanning...")
        self.scanner_running = True
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = "enabled"

        self._files_scanning_job = self.after(1000, self.scan_files)

    def stop_scanning(self):
        self.scanner_running = False
        self.stop_button['state'] = "disabled"
        self.start_button['state'] = "enabled"
        if self._files_scanning_job:
            self.after_cancel(self._files_scanning_job)
            self._files_scanning_job = None

    def reset_scanning(self):
        if not self.scanner_running:
            messagebox.showwarning("Attenzione", "Avvia uno scan!")
            return
        self.path_var.set("")
        self.img_list = []
        self.stop_scanning()

    def scan_files(self):
        path = self.path_var.get()
        # Count the total number of files
        total_files = sum([len(files) for r, d, files in os.walk(path)])
        scanned_files = 0
        self.img_list = []
        for root, dirs, files in os.walk(path):
            if not self.scanner_running:
                break
            for filename in files:
                if not self.scanner_running:
                    break

                # Estrazione dell'estensione
                _, file_extension = os.path.splitext(filename)
                file_path = os.path.join(root, filename)
                if self.is_ocr_recognition:
                    if file_extension in [".jpg", ".jpeg", ".png", ".tiff"]:
                        # Open the image file
                        image = Image.open(file_path)
                        # Perform OCR using PyTesseract
                        text = pytesseract.image_to_string(image)
                        # Print the extracted text
                        print(text + '\n\n')
                else:
                    scanner: Scanner = ScannerFactory.factory(file_extension)
                    if scanner is not None:
                        #nomenclature = simpledialog.askstring("Input", f"Inserisci Nomenclature per {file_path}:")
                        datetimecreated = Utils.get_creation_date(file_path)
                        md5 = Utils.get_file_md5(file_path)
                        size = Utils.get_file_size(file_path)
                        nomenclature = filename
                        img = IMG(
                            nomenclature=nomenclature,
                            file=file_path,
                            datetimecreated=datetimecreated,
                            md5=md5,
                            filesize=size
                        )
                        metas: list[MetaData] = scanner.scan(file_path)
                        datetimecreated = Utils.find_date_value(metas)
                        if datetimecreated is not None:
                            img.set_datetimecreated(datetimecreated)
                        image_dimensions = Utils.get_image_dimensions(metas)
                        if image_dimensions is not None:
                            img.set_image_dimensions(image_dimensions)
                        self.img_list.append(img)
                scanned_files += 1
                progress = (scanned_files / total_files) * 100
                self.progress_bar["value"] = progress
                self.status_label.config(text=f"Scanned {scanned_files} of {total_files} files")

        if self.scanner_running:
            self.status_label.config(text="Scanning completato!")
        else:
            self.status_label.config(text="Scanning fermato!")

        self.scanner_running = False
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = "disabled"

    def check_data(self):
        if not self.scanner_running:
            super().save_to_session((Utils.KEY_SESSION_IMG, self.img_list))
            return True