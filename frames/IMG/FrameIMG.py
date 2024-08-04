from tkinter import ttk, messagebox
import tkinter as tk

import Utils
from ToolTip import ToolTip
from frames.CustomFrame import CustomFrame
from model.IMG import Scanning
from model.Piece import Piece


class FrameIMG(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="La sezione IMG raccoglie i metadati amministrativi e gestionali relativi alle immagini "
                        "statiche.\nAlcuni di questi dati, in realtà, possono essere raccolti direttamente "
                        "all\'interno della sezione GEN, grazie all\'elemento <img_group>.\nLa sezione IMG utilizza il "
                        "namespace niso: che fa riferimento a uno schema che traduce le linee guida del Data "
                        "Dictionary NISO.\nLa sezione IMG è costituita di una sequenza di elementi <img>, "
                        "uno per ciascuna immagine digitale descritta da MAG.",
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )

        self._init_widgets()

    def _init_widgets(self):
        tk.Label(self.container_frame, text=f'Seleziona il valore per il tipo di scansione').pack()
        self.options_side = {
            "l'immagine contiene la digitalizzazione della pagina sinistra di un volume o di un fascicolo": "left",
            "l'immagine contiene la digitalizzazione della pagina destra di un volume o di un fascicolo": "right",
            "l'immagine contiene la digitalizzazione di una doppia pagina di un volume o di un fascicolo": "double",
            "l'immagine contiene la digitalizzazione parziale dell'oggetto analogico": "part"
        }
        self.selected_side = tk.StringVar()
        dropdown_side = ttk.OptionMenu(
            self.container_frame,
            self.selected_side,
            *self.options_side.keys(),
        )

        dropdown_side.pack(pady=(5, 20))

        ttk.Separator(self.container_frame, orient='horizontal').pack(fill='x', padx=20, pady=20)

        self.var_selected_millimetric_scale = tk.IntVar(value=0)
        checkbox_millimetric_scale = tk.Checkbutton(self.container_frame,
                                                    text="è presente una scala millimetrica",
                                                    variable=self.var_selected_millimetric_scale, onvalue=1, offvalue=0,
                                                    )
        checkbox_millimetric_scale.pack(pady=(5, 20))

        ttk.Separator(self.container_frame, orient='horizontal').pack(fill='x', padx=20, pady=20)
        self.var_is_scanning_enabled = tk.IntVar()

        checkbox_scanning = tk.Checkbutton(self.container_frame,
                                                  text="Desidero valorizzare il campo <niso:scanningsystem> ossia la descrizione del dispositivo usato per la scansione",
                                                  variable=self.var_is_scanning_enabled, onvalue=1, offvalue=0,
                                                  command=self.on_checkbox_scanning_selection)
        checkbox_scanning.pack()
        self.init_frame_scanning()

    def check_data(self):
        ret = True
        if self.selected_side.get() is not None:
            description_side = self.selected_side.get()
            key_side = self.options_side.get(description_side, None)
            super().save_to_session((Utils.KEY_SESSION_SIDE, key_side))
        if self.var_selected_millimetric_scale.get() is not None and self.var_selected_millimetric_scale.get() == 1:
            super().save_to_session((Utils.KEY_SESSION_SCALE, self.var_selected_millimetric_scale.get()))
        if self.var_is_scanning_enabled.get() is not None and self.var_is_scanning_enabled.get() == 1:
            source_type = None
            scanning_agency = None
            device_source = None
            scanner_manufacturer = None
            scanner_model = None
            capture_software = None
            if self.sourcetype_var.get() is not None:
                source_type = self.sourcetype_var.get()
            if self.scanningagency_entry.get() is not None:
                scanning_agency = self.scanningagency_entry.get()
            if self.devicesource_entry.get() is not None:
                device_source = self.devicesource_entry.get()
            if self.var_is_scanning_system_enabled.get() is not None and self.var_is_scanning_system_enabled.get() == 1:
                if self.scanner_manufacturer_entry.get() is not None and self.scanner_model_entry.get() is not None and self.capture_software_entry.get() is not None \
                        and self.capture_software_entry.get() and self.scanner_manufacturer_entry.get() and self.scanner_model_entry.get():
                    scanner_manufacturer = self.scanner_manufacturer_entry.get()
                    scanner_model = self.scanner_model_entry.get()
                    capture_software = self.capture_software_entry.get()
                else:
                    messagebox.showerror("Errore", "Il sistema di scansione deve avere il produttore, il modello e il "
                                                   "software definiti.")
                    ret = False
            if ret:
                scanning = Scanning(
                    source_type=source_type,
                    scanning_agency=scanning_agency,
                    device_source=device_source,
                    scanner_manufacturer=scanner_manufacturer,
                    scanner_model=scanner_model,
                    capture_software=capture_software
                )
                super().save_to_session((Utils.KEY_SESSION_SCANNING, scanning))
        return ret

    def init_frame_scanning(self):
        self.frame_scanning = ttk.Frame(self.container_frame)

        # Create a label and dropdown for <niso:sourcetype>
        sourcetype_label = ttk.Label(self.frame_scanning, text="<niso:sourcetype>:")
        sourcetype_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        # Dictionary to map descriptions to keywords
        sourcetype_options = {
            "negativo": "per immagini fotografiche i cui valori tonali risultino invertiti rispetto a quelli del "
                        "soggetto raffigurato e che permettono di produrre un numero illimitato di \"positivi\"",
            "positivo": "per immagini fotografiche, ottenute da \"negativi\", i cui valori tonali corrispondano a "
                        "quelli del soggetto raffigurato; sono da considerarsi \"positivi\" anche i prodotti ottenuti "
                        "da matrici virtuali attraverso stampanti, plotter, etc.",
            "diapositiva": "per immagini fotografiche positive realizzate su supporti trasparenti e visibili per "
                           "trasparenza o per proiezione",
            "unicum": "per immagini fotografiche \"uniche\", ottenute cioè senza mediazione di \"negativi\" e che, "
                      "a loro volta, non possono essere utilizzate come \"matrici\"; sono da considerarsi \"unicum\", "
                      "ad esempio, dagherrotipi, ambrotipi, ferrotipi, polaroid ed inoltre prodotti unici ottenuti "
                      "con procedimenti elettronici analogico-digitali, come fax o fotocopie",
            "fotografia virtuale": "per \"matrici virtuali\", cioè per immagini latenti memorizzate su memorie di "
                                   "massa analogiche, analogico-digitali e digitali",
            "vario": "per oggetti complessi e/o compositi costituiti da elementi appartenenti a categorie diverse. "
                     "Es.: vario: positivo/unicum; vario: unicum/positivo/fotografia virtuale"
        }

        self.sourcetype_var = tk.StringVar()

        sourcetype_dropdown = ttk.OptionMenu(
            self.frame_scanning,
            self.sourcetype_var,
            *sourcetype_options.keys()
        )
        sourcetype_dropdown.grid(row=0, column=1, pady=5, sticky=tk.EW)
        ToolTip(sourcetype_dropdown,
                "opzionale e non ripetibile, descrive le caratteristiche fisiche del supporto analogico di partenza")

        # Create a label and entry for <niso:scanningagency>
        scanningagency_label = ttk.Label(self.frame_scanning, text="<niso:scanningagency>:")
        scanningagency_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.scanningagency_entry = ttk.Entry(self.frame_scanning)
        self.scanningagency_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.scanningagency_entry, "opzionale e non ripetibile, contiene il nome della persona, società o "
                                           "ente produttore dell'immagine digitale, cioè dell'entità che ha "
                                           "realizzato la scansione. È di tipo xsd:string. \n Se assente, "
                                           "si assume che la scansione sia stata effettuata all'interno "
                                           "dell'istituzione responsabile del progetto di digitalizzazione.")

        # Create a label and entry for <niso:devicesource>
        devicesource_label = ttk.Label(self.frame_scanning, text="<niso:devicesource>:")
        devicesource_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.devicesource_entry = ttk.Entry(self.frame_scanning)
        self.devicesource_entry.grid(row=2, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.devicesource_entry, "opzionale e non ripetibile, descrive la tipologia dell'apparecchiatura di "
                                         "scansione, per esempio \"scanner\", \"fotocamera digitale\",\"videocamera\". È "
                                         "di tipo xsd:string.")
        self.var_is_scanning_system_enabled = tk.IntVar(value=0)
        checkbox_scanning = tk.Checkbutton(self.frame_scanning,
                                           text="Desidero valorizzare il campo <niso:scanningsystem> ossia la descrizione del dispositivo usato per la scansione",
                                           variable=self.var_is_scanning_system_enabled, onvalue=1, offvalue=0,
                                           command=self.on_checkbox_scanning_system_selection)
        checkbox_scanning.grid()

        # Configure grid to allow column resizing
        self.frame_scanning.columnconfigure(1, weight=1)
        self.init_frame_scanning_system()

    def init_frame_scanning_system(self):
        self.frame_scanning_system = ttk.Frame(self.container_frame)

        # Create a label and entry for <niso:scanner_manufacturer>
        scanner_manufacturer_label = ttk.Label(self.frame_scanning_system, text="<niso:scanner_manufacturer>:")
        scanner_manufacturer_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.scanner_manufacturer_entry = ttk.Entry(self.frame_scanning_system)
        self.scanner_manufacturer_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.scanner_manufacturer_entry, "obbligatorio e non ripetibile, contiene il nome del produttore del "
                                                 "dispositivo. È di tipo xsd:string.")

        # Create a label and entry for <niso:scanner_model>
        scanner_model_label = ttk.Label(self.frame_scanning_system, text="<niso:scanner_model>:")
        scanner_model_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        self.scanner_model_entry = ttk.Entry(self.frame_scanning_system)
        self.scanner_model_entry.grid(row=4, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.scanner_model_entry,
                "obbligatorio e non ripetibile, contiene la marca e il modello dell'apparecchiatura di acquisizione. È di tipo xsd:string.")

        # Create a label and entry for <niso:capture_software>
        capture_software_label = ttk.Label(self.frame_scanning_system, text="<niso:capture_software>:")
        capture_software_label.grid(row=5, column=0, sticky=tk.W, pady=5)

        self.capture_software_entry = ttk.Entry(self.frame_scanning_system)
        self.capture_software_entry.grid(row=5, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.capture_software_entry, "obbligatorio e non ripetibile, contiene il nome del software usato per "
                                             "l'acquisizione dell'immagine. È di tipo xsd:string.")
        self.frame_scanning_system.columnconfigure(1, weight=1)

    def on_checkbox_scanning_selection(self):
        if self.var_is_scanning_enabled.get() == 1:
            self.frame_scanning.pack(expand=True, fill=tk.BOTH)
        else:
            self.frame_scanning.pack_forget()
        self.var_is_scanning_system_enabled.set(0)
        self.container_frame.update_idletasks()

    def on_checkbox_scanning_system_selection(self):
        if self.var_is_scanning_system_enabled.get() == 1:
            self.frame_scanning_system.pack(expand=True, fill=tk.BOTH)
        else:
            self.frame_scanning_system.pack_forget()
        self.container_frame.update_idletasks()
