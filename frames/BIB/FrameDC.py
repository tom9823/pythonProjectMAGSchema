import tkinter as tk
from tkinter import ttk, messagebox
import Utils
from ToolTip import ToolTip
from frames.CustomFrame import CustomFrame

DC_TYPES_DEFINITIONS = {
    'Identifier': 'Un identificatore univoco di un record descrittivo in un dato contesto. Non va confuso con '
                  'segnatura o classificazione catalografica.',
    'Title': 'Il titolo della risorsa, o il nome attraverso il quale la risorsa è conosciuta.',
    'Creator': 'L\'autore della risorsa, ovvero l\'entità responsabile della produzione del contenuto della risorsa.',
    'Publisher': 'L\'entità responsabile della produzione della risorsa, come una casa editrice.',
    'Subject': 'L\'argomento della risorsa.',
    'Description': 'Una spiegazione del contenuto della risorsa. Può includere un riassunto, indice, riferimento '
                   'grafico, o testo libero.',
    'Contributor': 'Un’entità responsabile di un contributo al contenuto della risorsa (es. curatore, traduttore, '
                   'illustratore).',
    'Date': 'Una data associata a un evento del ciclo di vita della risorsa. Solitamente la creazione o la '
            'disponibilità.',
    'Type': 'La natura o il genere del contenuto della risorsa. Codifiche consigliate includono UNIMARC o il Dublin '
            'Core Type Vocabulary.',
    'Format': 'La manifestazione fisica della risorsa, includendo tipo di supporto o dimensioni.',
    'Source': 'Riferimento a una risorsa dalla quale è derivata la risorsa in oggetto.',
    'Language': 'La lingua del contenuto intellettuale della risorsa. Si consiglia di usare codici ISO 639 seguiti da '
                'ISO 3166 per la localizzazione.',
    'Relation': 'Riferimento a una risorsa correlata, utilizzando identificatori formali.',
    'Coverage': 'Estensione o scopo del contenuto della risorsa. Include localizzazione spaziale, periodo temporale o '
                'giurisdizione.',
    'Rights': 'Informazione sui diritti esercitati sulla risorsa, come diritti di proprietà intellettuale o copyright.'
}


class FrameDC(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="""La sezione BIB prevede un set di elementi Dublin Core (<dc:*>): raccoglie i metadati descrittivi dell'oggetto
analogico alla base della digitalizzazione; tutti gli elementi sono opzionali (tranne
<dc:identifier> che è obbligatorio) e ripetibili.""",
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )

        self._init_widgets()

    def _init_widgets(self):
        # Level frame
        level_frame = tk.Frame(self.container_frame)
        level_frame.pack(pady=10)
        self.level_var = tk.StringVar()
        label_level = tk.Label(level_frame, text="Level (*):")
        label_level.grid(row=0, column=0)
        self.level_menu_options = {"a: spoglio (una parte di una pubblicazione più grande, ad esempio un articolo in una rivista o un capitolo in un libro)": "a",
                                   "m: monografia (un'opera completa e indipendente)": "m",
                                   "s: seriale (""una pubblicazione periodica come una rivista)": "s",
                                   "c: raccolta prodotta dall'istituzione (una collezione aggregata)": "c",
                                   "f: unità ""archivistica (file)": "f",
                                   "d: unità documentaria (document, item)": "d"
                                   }
        level_menu = tk.OptionMenu(level_frame, self.level_var, *self.level_menu_options.keys())
        level_menu.grid(row=0, column=1)

        # Table DC
        tree_frame = tk.Frame(self.container_frame)
        tree_frame.pack()

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_dc = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.table_dc.yview)
        self.table_dc['columns'] = ('dc_type', 'value')
        self.table_dc.column("#0", width=0, stretch=tk.NO)
        self.table_dc.column("dc_type", anchor=tk.W, width=200)
        self.table_dc.column("value", anchor=tk.W, width=200)

        # Creazione delle intestazioni
        self.table_dc.heading("#0", text="Label", anchor=tk.W)
        self.table_dc.heading("dc_type", text="DC Tipo", anchor=tk.W)
        self.table_dc.heading("value", text="Valore", anchor=tk.W)

        self.table_dc.pack()

        # Frame per i pulsanti
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_record = tk.Button(buttons_frame, text="Aggiungi DC", command=self._open_add_dc_window)
        button_add_record.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_record = tk.Button(buttons_frame, text="Rimuovi DC selezionato", command=self._remove_selected)
        button_remove_record.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Modifica DC Element selezionato", command=self._open_update_dc_window)
        button_update_record.grid(row=0, column=3)

        self.dc_list = self.controller.session.get(Utils.KEY_SESSION_DC, [])
        for dc_element in self.dc_list:
            dc_element_key, dc_element_value = dc_element
            row = [dc_element_key, dc_element_value]
            self.table_dc.insert(parent='', index=tk.END, text="Parent", values=row)

    def _open_add_dc_window(self):
        # Inizializza la variabile dc_type_var
        self.dc_type_var = tk.StringVar(value=next(iter(DC_TYPES_DEFINITIONS.keys())))
        self.dc_type_var.trace_add('write', self._update_description)

        self.add_dc_window = tk.Toplevel(self)
        self.add_dc_window.update_idletasks()
        x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.add_dc_window.winfo_width() // 2
        y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.add_dc_window.winfo_height() // 2
        self.add_dc_window.geometry(f"+{x}+{y}")

        self.add_dc_window.title("Aggiungi DC Element")

        add_frame = tk.Frame(self.add_dc_window)
        add_frame.pack(pady=10)

        # Descrizione dell'elemento DC
        self.description_label = tk.Label(
            add_frame,
            text=DC_TYPES_DEFINITIONS[self.dc_type_var.get()],
            justify=tk.LEFT,
            wraplength=400
        )
        self.description_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # labels and entries
        dc_type_label = tk.Label(add_frame, text="DC Type")
        dc_type_label.grid(row=1, column=0)
        self.dc_type_menu = tk.OptionMenu(add_frame, self.dc_type_var, *DC_TYPES_DEFINITIONS.keys())
        self.dc_type_menu.grid(row=2, column=0)

        value_label = tk.Label(add_frame, text="Value")
        value_label.grid(row=1, column=1)
        self.value_entry = tk.Entry(add_frame)
        self.value_entry.grid(row=2, column=1)

        # Bottoni per confermare o annullare l'aggiunta
        buttons_frame = tk.Frame(self.add_dc_window)
        buttons_frame.pack(pady=5)

        button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_add_dc)
        button_confirm.grid(row=0, column=0)

        button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.add_dc_window.destroy)
        button_cancel.grid(row=0, column=1)

    def _open_update_dc_window(self):
        item_id = self.table_dc.focus()
        if item_id is not None and item_id != '':
            selected_index = self.table_dc.index(item_id)
            selected_dc = self.dc_list[selected_index]

            # Inizializza la variabile dc_type_var
            self.dc_type_var = tk.StringVar(value=selected_dc[0])
            self.dc_type_var.trace_add('write', self._update_description)

            # Crea una nuova finestra di dialogo per aggiornare il DC element
            self.update_dc_window = tk.Toplevel(self.get_parent())

            self.update_dc_window.update_idletasks()
            x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.update_dc_window.winfo_width() // 2
            y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.update_dc_window.winfo_height() // 2
            self.update_dc_window.geometry(f"+{x}+{y}")

            self.update_dc_window.title(f"Modifica DC Element {self.dc_type_var.get()}")

            update_frame = tk.Frame(self.update_dc_window)
            update_frame.pack(pady=10)

            # Descrizione dell'elemento DC
            self.description_label = tk.Label(
                update_frame,
                text=DC_TYPES_DEFINITIONS[self.dc_type_var.get()],
                justify=tk.LEFT,
                wraplength=400
            )
            self.description_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

            # labels and pre-filled entries
            dc_type_label = tk.Label(update_frame, text="DC Type")
            dc_type_label.grid(row=1, column=0)
            self.dc_type_menu = tk.OptionMenu(update_frame, self.dc_type_var, *DC_TYPES_DEFINITIONS.keys())
            self.dc_type_menu.grid(row=2, column=0)

            value_label = tk.Label(update_frame, text="Value")
            value_label.grid(row=1, column=1)
            self.value_entry = tk.Entry(update_frame)
            self.value_entry.grid(row=2, column=1)
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, selected_dc[1])

            # Bottoni per confermare o annullare l'aggiornamento
            buttons_frame = tk.Frame(self.update_dc_window)
            buttons_frame.pack(pady=5)

            button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_update_dc)
            button_confirm.grid(row=0, column=0)

            button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.update_dc_window.destroy)
            button_cancel.grid(row=0, column=1)
        else:
            messagebox.showerror("Errore", "Seleziona una riga nella tabella dei dublin core elements")

    def _update_description(self, *args):
        self.description_label.config(text=DC_TYPES_DEFINITIONS[self.dc_type_var.get()])

    def _confirm_add_dc(self):
        dc_type = self.dc_type_var.get()
        value = self.value_entry.get()
        self.table_dc.insert(parent='', index=tk.END, text="Parent", values=(dc_type, value))
        self.dc_list.append((dc_type, value))
        self.add_dc_window.destroy()

    def _confirm_update_dc(self):
        item_id = self.table_dc.focus()
        if item_id is not None and item_id != '':
            dc_type = self.dc_type_var.get()
            value = self.value_entry.get()
            selected_index = self.table_dc.index(item_id)
            self.table_dc.item(item_id, values=(dc_type, value))
            self.dc_list[selected_index] = (dc_type, value)
            self.update_dc_window.destroy()

    def _remove_all(self):
        self.dc_list = []
        self.controller.session[Utils.KEY_SESSION_DC] = []
        for record in self.table_dc.get_children():
            self.table_dc.delete(record)

    def _remove_selected(self):
        selected = self.table_dc.selection()
        for item_id in selected:
            selected_index = self.table_dc.index(item_id)
            self.table_dc.delete(item_id)
            self.dc_list.pop(selected_index)

    def check_data(self):
        ret = True
        level = self.level_var.get()
        if not level:
            messagebox.showwarning("Attenzione", "Per favore, compila il campo 'level'.")
            ret = False
        if not any(dc_element[0] == 'Identifier' for dc_element in self.dc_list):
            messagebox.showwarning("Attenzione", "Per favore, inserisci almeno un dc element che abbia come tipo "
                                                 "'Identifier'.")
            ret = False
        if ret:
            super().save_to_session(
                (Utils.KEY_SESSION_DC, self.dc_list)
            )
        return ret
