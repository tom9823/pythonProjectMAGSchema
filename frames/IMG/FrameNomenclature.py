import os
import re
from tkinter import Tk, Label, Button, filedialog, Frame, Scrollbar, Listbox, StringVar, OptionMenu
from PIL import Image, ImageTk

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
        self._init_widgets()

    def _init_widgets(self):
        self.load_button = Button(self.container_frame, text="Carica Cartella", command=self.load_folder)
        self.load_button.pack(side="left")

        self.save_button = Button(self.container_frame, text="Salva Etichette", command=self.save_labels)
        self.save_button.pack(side="left")

        self.image_frame = Frame(self.container_frame)
        self.image_frame.pack()

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        self.label_options = [
            "Piatto anteriore", "Contropiatto anteriore", "Carta di guardia recto", "Carta di guardia verso",
            "Carta 1 recto", "Taglio laterale", "Dorso", "Taglio inferiore", "Taglio superiore"
        ]

        self.selected_label = StringVar(self.master)
        self.selected_label.set(self.label_options[0])  # Imposta l'opzione predefinita

        self.label_dropdown = OptionMenu(self.image_frame, self.selected_label, *self.label_options)
        self.label_dropdown.pack()

        self.next_button = Button(self.image_frame, text="Successiva", command=self.next_image)
        self.next_button.pack()

        self.prev_button = Button(self.image_frame, text="Precedente", command=self.prev_image)
        self.prev_button.pack()

        self.image_listbox = Listbox(self.container_frame, height=20)
        self.image_listbox.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(self.container_frame)
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
            self.images = [f for f in os.listdir(folder_path) if
                           f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'tiff'))]
            self.images.sort(key=self.extract_number)
            self.images = [os.path.join(folder_path, img) for img in self.images]
            self.update_listbox()
            if self.images:
                self.show_image(0)

    def extract_number(self, filename):
        match = re.search(r'(\d+)(?=\.\w+$)', filename)
        return int(match.group(0)) if match else 0

    def update_listbox(self):
        self.image_listbox.delete(0, "end")
        for img in self.images:
            self.image_listbox.insert("end", os.path.basename(img))

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
        self.labels[image_path] = label

    def save_labels(self):
        with open("labels.txt", "w") as f:
            for image_path, label in self.labels.items():
                f.write(f"{image_path}\t{label}\n")
        print("Etichette salvate.")

    def check_data(self):
        return True
