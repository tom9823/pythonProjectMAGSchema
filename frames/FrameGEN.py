import tkinter as tk
from tkinter import messagebox, ttk
import re

import Utils
from ToolTip import ToolTip
from frames.CustomFrame import CustomFrame

class FrameGEN(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame=
            """
                L'elemento <gen> è il primo figlio dell'elemento root <metadigit> ed è obbligatorio.
                Esso contiene una serie di elementi figli che contengono informazioni relative all'istituzione
                responsabile del progetto di digitalizzazione, al progetto stesso, alla completezza o integrità
                del file, all'accessibilità dell'oggetto (o gli oggetti) descritto nella sezione BIB.
                L'elemento, inoltre, può contenere informazioni tecniche condivise da più oggetti
                descritti dal documento MAG. L'elemento non è ripetibile.
            """,
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )
        self._init_widgets()

    def show_identifier_modal(self):
        modal = tk.Toplevel(self.container_frame)
        modal.title("Inserisci Codice Identificativo")

        label = tk.Label(modal, text="Inserisci il codice dell'identificativo dell'opera (ISBN, codice inventario, ecc.):")
        label.pack(padx=20, pady=10)

        self.entry_identifier = tk.Entry(modal)
        self.entry_identifier.pack(padx=20, pady=5)

        button_frame = tk.Frame(modal)
        button_frame.pack(pady=10)

        btn_confirm = tk.Button(button_frame, text="Conferma", command=self._confirm_identifier)
        btn_confirm.pack(side=tk.LEFT, padx=5)

        btn_cancel = tk.Button(button_frame, text="Annulla", command=modal.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _confirm_identifier(self):
        identifier_code = self.entry_identifier.get()
        if identifier_code:
            self.controller.query_online_resources(identifier_code)
        print(f"Codice Identificativo inserito: {identifier_code}")
        self.controller.show_frame('FrameGEN')
        self.entry_identifier.master.destroy()

    def _init_widgets(self):
        tk.Label(self.container_frame, text="Progetto di Digitalizzazione (*):").pack(pady=(10,5))
        self.entry_stprog_var = tk.StringVar()
        entry_stprog = tk.Entry(self.container_frame, width=50, textvariable=self.entry_stprog_var)
        entry_stprog.focus()
        entry_stprog.pack()
        ToolTip(entry_stprog, "Contiene la URI dove è possibile trovare la documentazione relativa la progetto di digitalizzazione. \nTipicamente si tratta della pagina web in cui sono specificate le scelte relative alla \ndigitalizzazione del progetto; in alternativa si suggerisce di puntare alla home page \ndell'istituzione responsabile del progetto. Il suo contenuto è xsd:anyURI. L'elemento è \nobbligatorio, non ripetibile e non sono definiti attributi.")

        tk.Label(self.container_frame, text="Collezione:").pack(pady=(10,5))
        self.entry_collection_var = tk.StringVar()
        entry_collection = tk.Entry(self.container_frame, width=50, textvariable=self.entry_collection_var)
        entry_collection.pack()
        ToolTip(entry_collection, "Contiene la URI (tipicamente l'indirizzo di una pagina web) di un documento in cui viene specificata \nla collezione cui fa parte la risorsa o le risorse digitalizzate. Il suo contenuto è xsd:anyURI. \nL'elemento è opzionale, non ripetibile e non sono definiti attributi.")

        tk.Label(self.container_frame, text="Agenzia (*):").pack(pady=(10,5))
        self.entry_agency_var = tk.StringVar()
        entry_agency = tk.Entry(self.container_frame, width=50, textvariable=self.entry_agency_var)
        entry_agency.pack()
        ToolTip(entry_agency, "Contiene il nome dell'istituzione responsabile del progetto di digitalizzazione. Il suo contenuto è \nxsd:string, ma si raccomanda di usare la sintassi UNIMARC definita per il campo 801, cioè cod. paese \n(due caratteri):codice Agenzia per intero, per esempio: IT:BNCF. In alternativa è possibile usare \nuna sigla riconosciuta, per esempio dall'Anagrafe biblioteche italiane: http://anagrafe.iccu.sbn.it/ \n, per esempio: IT:VE0049 o IT:RM1316. L'elemento è obbligatorio, non ripetibile e non sono definiti \nattributi.")

        tk.Label(self.container_frame, text="Condizioni di Accesso (*):").pack(pady=(10,5))
        self.access_rights_var = tk.StringVar()
        self.access_rights_menu_options = {"0 : uso riservato all'interno dell'istituzione": 0, "1 : uso pubblico": 1}
        access_rights_menu = tk.OptionMenu(self.container_frame, self.access_rights_var, *self.access_rights_menu_options)
        access_rights_menu.pack()
        ToolTip(access_rights_menu, "Dichiara le condizioni di accessibilità dell'oggetto descritto nella sezione BIB. Il suo contenuto \ndeve assumere uno dei seguenti valori:\n- 0 : uso riservato all'interno dell'istituzione\n- 1 : uso pubblico\nL'elemento è obbligatorio, non ripetibile e non sono definiti attributi.")

        tk.Label(self.container_frame, text="Completezza (*):").pack(pady=(10,5))
        self.completeness_var = tk.StringVar()
        self.completeness_menu_options = {"0 : digitalizzazione completa": 0, "1 : digitalizzazione incompleta": 1}
        completeness_menu = tk.OptionMenu(self.container_frame, self.completeness_var, *self.completeness_menu_options.keys())
        completeness_menu.pack()
        ToolTip(completeness_menu, "Dichiara la completezza della digitalizzazione. Il suo contenuto deve assumere uno dei seguenti \nvalori:\n- 0 : digitalizzazione completa\n- 1 : digitalizzazione incompleta\nL'elemento è obbligatorio, non ripetibile e non sono definiti attributi.")

        tk.Label(self.container_frame, text="Creation (opzionale):").pack(pady=(10,5))
        self.entry_creation_var = tk.StringVar()
        entry_creation = tk.Entry(self.container_frame, width=50, textvariable=self.entry_creation_var)
        entry_creation.pack()
        ToolTip(entry_creation, "Data di creazione della sezione nel formato aaaa-mm-ggThh:mm:ss (ad esempio 2005-08-04T13:00:00). L'elemento è opzionale, non ripetibile.")

        tk.Label(self.container_frame, text="Last Update (opzionale):").pack(pady=(10,5))
        self.entry_last_update_var = tk.StringVar()
        entry_last_update = tk.Entry(self.container_frame, width=50, textvariable=self.entry_last_update_var)
        entry_last_update.pack()
        ToolTip(entry_last_update, "Data dell'ultimo aggiornamento della sezione nel formato aaaa-mm-ggThh:mm:ss (ad esempio 2005-08-04T13:00:00). L'elemento è opzionale, non ripetibile.")

    def check_data(self):
        ret = True
        datetime_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"

        if not self.entry_stprog_var.get() or not Utils.validate_uri(self.entry_stprog_var.get()):
            messagebox.showerror("Errore", "Il campo 'Progetto di Digitalizzazione' è obbligatorio e deve contenere una URI valida.")
            ret = False
        if self.entry_collection_var.get() and not Utils.validate_uri(self.entry_collection_var.get()):
            messagebox.showerror("Errore", "Il campo 'Collezione' deve contenere una URI valida.")
            ret = False
        if not self.entry_agency_var.get() or not Utils.validate_agency(self.entry_agency_var.get()):
            messagebox.showerror("Errore", "Il campo 'Agenzia' è obbligatorio e deve seguire il formato UNIMARC (es: IT:BNCF).")
            ret = False
        if not self.access_rights_var.get():
            messagebox.showerror("Errore", "Il campo 'Condizioni di Accesso' è obbligatorio.")
            ret = False
        if not self.completeness_var.get():
            messagebox.showerror("Errore", "Il campo 'Completezza' è obbligatorio.")
            ret = False
        if self.entry_creation_var.get() and not re.match(datetime_regex, self.entry_creation_var.get()):
            messagebox.showerror("Errore", "Il campo 'Creation' deve contenere una data valida nel formato aaaa-mm-ggThh:mm:ss.")
            ret = False
        if self.entry_last_update_var.get() and not re.match(datetime_regex, self.entry_last_update_var.get()):
            messagebox.showerror("Errore", "Il campo 'Last Update' deve contenere una data valida nel formato aaaa-mm-ggThh:mm:ss.")
            ret = False

        if ret:
            super().save_to_session(
                ('Progetto di Digitalizzazione', self.entry_stprog_var.get()),
                ('Collezione', self.entry_collection_var.get()),
                ('Agenzia', self.entry_agency_var.get()),
                ('Condizioni di Accesso', self.access_rights_menu_options[self.access_rights_var.get()]),
                ('Completezza', self.completeness_menu_options[self.completeness_var.get()]),
                ('Creation', self.entry_creation_var.get()),
                ('Last Update', self.entry_last_update_var.get())
            )

        return ret