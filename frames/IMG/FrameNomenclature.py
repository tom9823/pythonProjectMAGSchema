import os
import re
from tkinter import Tk, Label, Button, filedialog, Frame, Scrollbar, Listbox, StringVar, OptionMenu
from PIL import Image, ImageTk

import Utils
from frames.CustomFrame import CustomFrame


class FrameNomenclature(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame='Nomenclature',
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )
        self.current_image_index = None
        self.nomenclature_dict = dict()
        self._init_widgets()

    def _init_widgets(self):
        self.grid_frame = Frame(self.container_frame)
        self.grid_frame.pack()
        self.left_frame = Frame(self.grid_frame)
        self.left_frame.grid(row=0, column=0)
        self.right_frame = Frame(self.grid_frame)
        self.right_frame.grid(row=0, column=1)

        self.load_button = Button(self.container_frame, text="Carica cartella", command=self.load_folder)
        self.load_button.pack(pady=20)
        self.image_frame = Frame(self.right_frame)
        self.image_frame.pack()
        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        self.label_options = [
            "Piatto anteriore", "Contropiatto anteriore", "Carta di guardia recto", "Carta di guardia verso",
            "Carta 1 recto", "Taglio laterale", "Dorso", "Taglio inferiore", "Taglio superiore",
            "Tavola fuori testo recto", "tavola fuori testo verso"
        ]

        self.selected_label = StringVar(self.master)

        self.frame_button_image = Frame(self.right_frame)
        self.frame_button_image.pack()

        # Inizialmente disattiva i bottoni "Precedente", "Successiva" e il dropdown
        self.prev_button = Button(self.frame_button_image, text="Precedente", command=self.prev_image, state='disabled')
        self.prev_button.grid(column=0, row=0)
        self.label_dropdown = OptionMenu(self.frame_button_image, self.selected_label, *self.label_options)
        self.label_dropdown.config(state='disabled')  # Disattiva dropdown
        self.label_dropdown.grid(column=1, row=0)
        self.next_button = Button(self.frame_button_image, text="Successiva", command=self.next_image, state='disabled')
        self.next_button.grid(column=2, row=0)

        self.image_listbox = Listbox(self.left_frame, height=20)
        self.image_listbox.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(self.left_frame)
        self.scrollbar.pack(side="left", fill="y")

        self.image_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.image_listbox.yview)

        self.image_listbox.bind("<<ListboxSelect>>", self.show_image_from_listbox)

        self.images = []
        self.current_image_index = 0
        self.labels = {}

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Usa os.walk per attraversare ricorsivamente tutte le sottocartelle
            self.images = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('tif', 'tiff')):
                        self.images.append(os.path.join(root, file))

            # Ordina le immagini per numero estratto dal nome del file
            self.images.sort(key=self.extract_number)

            self.update_listbox()
            if self.images:
                self.show_image(0)
                # Attiva i bottoni e il dropdown solo dopo che una cartella è stata caricata
                self.enable_buttons()

    def extract_number(self, filename):
        match = re.search(r'(\d+)(?=\.\w+$)', filename)
        return int(match.group(0)) if match else 0

    def update_listbox(self):
        self.image_listbox.delete(0, "end")
        for img in self.images:
            label = self.nomenclature_dict.get(os.path.splitext(img)[0],
                                               "")  # Ottiene l'etichetta associata o una stringa vuota
            display_text = f"{os.path.basename(img)} ({label})" if label else os.path.basename(img)
            self.image_listbox.insert("end", display_text)

    def show_image(self, index):
        if 0 <= index < len(self.images):
            self.current_image_index = index
            image_path = self.images[index]
            image = Image.open(image_path)
            image.thumbnail((300, 300))  # Ridimensiona l'immagine
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Evita che l'immagine venga raccolta dal garbage collector

            # Mostra l'etichetta associata all'immagine
            current_label = self.labels.get(image_path, self.label_options[0])
            self.selected_label.set(current_label)

    def next_image(self):
        current_label = self.selected_label.get()
        if current_label == "Carta 1 recto":
            self.save_current_label()
            # Salta all'ultima immagine e imposta l'etichetta su "Taglio inferiore"
            self.show_image(len(self.images) - 1)
            self.selected_label.set("Taglio inferiore")
        elif self.current_image_index < len(self.images) - 1:
            self.save_current_label()
            self.show_image(self.current_image_index + 1)

    def prev_image(self):
        if self.current_image_index > 0:
            self.save_current_label()
            self.show_image(self.current_image_index - 1)

    def show_image_from_listbox(self, event):
        selected_index = self.image_listbox.curselection()[0]
        self.save_current_label()
        self.show_image(selected_index)

    def save_current_label(self):
        image_path = self.images[self.current_image_index]
        label = self.selected_label.get()
        filename_without_extension, file_extension = os.path.splitext(image_path)
        self.nomenclature_dict[filename_without_extension] = label
        self.update_listbox()

    def enable_buttons(self):
        self.prev_button.config(state='normal')
        self.next_button.config(state='normal')
        self.label_dropdown.config(state='normal')

    def check_data(self):
        super().save_to_session((Utils.KEY_FRAME_NOMENCLATURE, self.nomenclature_dict))
        return True
