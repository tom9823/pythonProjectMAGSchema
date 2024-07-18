import tkinter as tk
from tkinter import ttk, messagebox

import Utils
from frames.CustomFrame import CustomFrame

# Lista dei tipi di elementi DC (Dublin Core)
DC_TYPES = [
    'Identifier', 'Title', 'Creator', 'Publisher',
    'Subject', 'Description', 'Contributor', 'Date', 'Type',
    'Format', 'Source', 'Language', 'Relation', 'Coverage', 'Rights'
]


class FrameDC(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
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
        self.level_menu_options = {"a: spoglio": "a", "m: monografia": "a", "s: seriale": "s",
                                   "c: raccolta prodotta dall'istituzione": "c"}
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

        # Frame per l'aggiunta di un nuovo record
        add_frame = tk.Frame(self.container_frame)
        add_frame.pack(pady=10)

        # Etichetta per il DC Type
        dc_type_label = tk.Label(add_frame, text="DC Type")
        dc_type_label.grid(row=0, column=0)

        # Etichetta e campo di input per il valore
        value_label = tk.Label(add_frame, text="Value")
        value_label.grid(row=0, column=1)

        # Menu a discesa per selezionare il DC Type
        self.dc_type_var = tk.StringVar()
        self.dc_type_var.set(DC_TYPES[0])  # Imposta il valore predefinito
        self.dc_type_menu = tk.OptionMenu(add_frame, self.dc_type_var, *DC_TYPES)
        self.dc_type_menu.grid(row=1, column=0)

        self.value_entry = tk.Entry(add_frame)
        self.value_entry.grid(row=1, column=1)

        # Pulsanti
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_record = tk.Button(buttons_frame, text="Aggiungi DC", command=self._add_dc)
        button_add_record.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_record = tk.Button(buttons_frame, text="Rimuovi DC selezionato", command=self._remove_selected)
        button_remove_record.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Aggiorna DC", command=self._update_dc)
        button_update_record.grid(row=0, column=3)

        self.table_dc.bind("<Double-1>", self._clicker)
        self.table_dc.bind("<ButtonRelease-1>", self._clicker)

        self.dc_list = self.controller.session.get(Utils.KEY_SESSION_DC, [])
        for dc_element in self.dc_list:
            dc_element_key, dc_element_value = dc_element
            row = [dc_element_key, dc_element_value]
            self.table_dc.insert(parent='', index=tk.END, text="Parent", values=row)

    def _add_dc(self):
        dc_type = self.dc_type_var.get()
        value = self.value_entry.get()
        self.table_dc.insert(parent='', index=tk.END, text="Parent", values=(dc_type, value))
        self.dc_list.append((dc_type, value))
        self.value_entry.delete(0, tk.END)

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

    def _update_dc(self):
        # ad esempio I001
        item_id = self.table_dc.focus()
        if item_id is not None and item_id != '':
            selected_index = self.table_dc.index(item_id)
            dc_type = self.dc_type_var.get()
            value = self.value_entry.get()
            self.table_dc.item(item_id, values=(dc_type, value))
            self.dc_list[selected_index] = (dc_type, value)
        else:
            messagebox.showerror("Errore", "Seleziona una riga nella tabella dei dublin core elements")

    def _select_dc(self):
        selected = self.table_dc.focus()
        if selected:
            values = self.table_dc.item(selected, 'values')
            dc_type, value = values
            if dc_type and value:
                self.dc_type_var.set(dc_type)
                self.value_entry.delete(0, tk.END)
                self.value_entry.insert(0, value)

    def _clicker(self, event):
        self._select_dc()

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