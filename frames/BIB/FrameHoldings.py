from tkinter import ttk, messagebox
from tkinter import simpledialog
import tkinter as tk
import Utils
from ToolTip import ToolTip
from UI.TreeviewEditable import TreeviewEditable
from frames.CustomFrame import CustomFrame
from model.Holdings import Shelfmark, Holdings


class FrameHoldings(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="""La sezione BIB prevede l'elemento <holdings> :raccoglie le informazioni relative all'Istituzione che possiede l'oggetto
analogico. L'elemento è opzionale e ripetibile.""",
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )

        self._init_widgets()

    def _init_widgets(self):
        tree_frame = tk.Frame(self.container_frame)
        tree_frame.pack()

        tree_vertical_scroll_holdings = tk.Scrollbar(tree_frame)
        tree_vertical_scroll_holdings.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_holdings = ttk.Treeview(tree_frame, yscrollcommand=tree_vertical_scroll_holdings.set)
        tree_vertical_scroll_holdings.config(command=self.table_holdings.yview)

        self.table_holdings['columns'] = ("id", "library", "inventory", "shelfmarks")
        self.table_holdings.column("#0", width=0, stretch=tk.NO)
        self.table_holdings.column("id", anchor=tk.W, width=240)
        self.table_holdings.column("library", anchor=tk.W, width=240)
        self.table_holdings.column("inventory", anchor=tk.W, width=240)
        self.table_holdings.column("shelfmarks", anchor=tk.W, width=240)

        # create headings
        self.table_holdings.heading("#0", text="Label", anchor=tk.W)
        self.table_holdings.heading("id", text="Id", anchor=tk.W)
        self.table_holdings.heading("library", text="Library", anchor=tk.W)
        self.table_holdings.heading("inventory", text="Inventory", anchor=tk.W)
        self.table_holdings.heading("shelfmarks", text="Shelfmarks", anchor=tk.W)
        # populate table

        self.holdings_list = self.controller.session.get(Utils.KEY_SESSION_HOLDINGS, [])

        for holding in self.holdings_list:
            row = (holding.id, holding.library, holding.inventory, holding.get_string_shelfmarks())
            self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row)

        self.table_holdings.pack()

        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=5)

        button_add_holding = tk.Button(buttons_frame, text="Aggiungi holding", command=self._open_add_holdings_window)
        button_add_holding.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_holding = tk.Button(buttons_frame, text="Rimuovi holding selezionati",
                                          command=self._remove_selected)
        button_remove_holding.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Modifica holding selezionato",
                                         command=self._open_update_holdings_window)
        button_update_record.grid(row=0, column=3)

    def _open_add_holdings_window(self):
        # Crea una nuova finestra di dialogo per aggiungere holding
        self.add_holdings_window = tk.Toplevel(self)
        self.add_holdings_window.update_idletasks()
        x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.add_holdings_window.winfo_width() // 2
        y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.add_holdings_window.winfo_height() // 2
        self.add_holdings_window.geometry(f"+{x}+{y}")

        self.add_holdings_window.title("Aggiungi Holding")

        # Copia il contenuto di add_frame nella nuova finestra
        add_frame = tk.Frame(self.add_holdings_window)
        add_frame.pack(pady=10)

        # Descrizione dell'elemento <holdings>
        description_label = tk.Label(
            add_frame,
            text="Il contenuto dell'elemento <holdings> è di tipo xsd:sequence, vale a dire che è\n"
                 "costituito da una sequenza di elementi. Nello specifico, l'elemento <holdings> contiene i\n"
                 "seguenti elementi, tutti opzionali.",
            justify=tk.LEFT
        )
        description_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # labels and entries
        id_label = tk.Label(add_frame, text="Holdings ID")
        id_label.grid(row=1, column=0, sticky=tk.W)
        self.id_entry = tk.Entry(add_frame)
        self.id_entry.grid(row=2, column=0)
        ToolTip(self.id_entry, text="ID: di tipo xsd:ID, serve a definire un identificatore univoco all'interno del \n"
                                    "record MAG cui è possibile fare riferimento da altri luoghi del medesimo record. \n"
                                    "L'attributo trova la sua utilità qualora vi sia la necessità di dichiarare \n"
                                    "diversi <holdings>.")

        library_label = tk.Label(add_frame, text="Library")
        library_label.grid(row=1, column=1, sticky=tk.W)
        self.library_entry = tk.Entry(add_frame)
        self.library_entry.grid(row=2, column=1)
        ToolTip(self.library_entry,
                text="Library: contiene il nome dell'istituzione proprietaria dell'oggetto analogico o \n"
                     "di parte dell'oggetto analogico. Di tipo xsd:string, è opzionale e non \n"
                     "ripetibile.")

        inventory_label = tk.Label(add_frame, text="Inventory")
        inventory_label.grid(row=1, column=2, sticky=tk.W)
        self.inventory_entry = tk.Entry(add_frame)
        self.inventory_entry.grid(row=2, column=2)
        ToolTip(self.inventory_entry,
                text="Inventory: contiene il numero di inventario attribuito all'oggetto analogico \n"
                     "dall'istituzione che lo possiede. Di tipo xsd:string, è opzionale e non \n"
                     "ripetibile.")

        # table shelfmarks
        frame_shelfmarks = tk.Frame(add_frame)
        frame_shelfmarks.grid(row=2, column=3)
        ToolTip(frame_shelfmarks, text="Shelfmark : contiene la collocazione dell'oggetto digitale \n"
                                       "all'interno del catalogo dell'istituzione che lo possiede. Di tipo \n"
                                       "xsd:string, è opzionale e ripetibile. Per l'elemento è definito un \n"
                                       "attributo: - type : si usa per definire il tipo di collocazione nel \n"
                                       "caso di collocazioni plurime, per esempio quando si vuole registrare "
                                       "\n"
                                       "una collocazione antica e una moderna. L'attributo è opzionale e il \n"
                                       "suo contenuto è xsd:string.")
        tree_frame_shelfmarks = tk.Frame(frame_shelfmarks)
        tree_frame_shelfmarks.pack(pady=10)
        tree_vertical_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
        tree_vertical_scroll_shelfmarks.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_shelfmarks = TreeviewEditable(tree_frame_shelfmarks,
                                                 yscrollcommand=tree_vertical_scroll_shelfmarks.set)
        tree_vertical_scroll_shelfmarks.config(command=self.table_shelfmarks.yview)
        self.table_shelfmarks['columns'] = ("type", "value")
        self.table_shelfmarks.column("#0", width=0, stretch=tk.NO)
        self.table_shelfmarks.column("type", anchor=tk.W, width=120)
        self.table_shelfmarks.column("value", anchor=tk.W, width=120)

        # create headings
        self.table_shelfmarks.heading("#0", text="Label", anchor=tk.W)
        self.table_shelfmarks.heading("type", text="Type", anchor=tk.W)
        self.table_shelfmarks.heading("value", text="Value", anchor=tk.W)
        self.table_shelfmarks.pack()

        button_add_shelfmark = tk.Button(frame_shelfmarks, text="Aggiungi shelfmark", command=self._add_shelfmark)
        button_add_shelfmark.pack(pady=5)

        # Bottoni per confermare o annullare l'aggiunta
        buttons_frame = tk.Frame(self.add_holdings_window)
        buttons_frame.pack(pady=5)

        button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_add_holdings)
        button_confirm.grid(row=0, column=0)

        button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.add_holdings_window.destroy)
        button_cancel.grid(row=0, column=1)

    def _confirm_add_holdings(self):
        if not self.id_entry.get() and self.holdings_list and len(self.holdings_list) > 0:
            messagebox.showerror("Attenzione", "Data la presenza di più holdings è necessario definire un holdings id")
        else:
            # Aggiunge l'holdings e chiude la finestra
            shelfmarks = []
            for item in self.table_shelfmarks.get_children():
                values = self.table_shelfmarks.item(item, 'values')
                shelfmark = Shelfmark(values[0], values[1])
                shelfmarks.append(shelfmark)
            holdings = Holdings(self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), shelfmarks)
            row = (holdings.get_holdings_id(), holdings.get_library(), holdings.get_inventory_number(),
                   holdings.get_string_shelfmarks())
            self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row)
            self.holdings_list.append(holdings)
            self.add_holdings_window.destroy()

    def _open_update_holdings_window(self):
        item_id = self.table_holdings.focus()
        if item_id is not None and item_id != '':
            selected_index = self.table_holdings.index(item_id)
            selected_holdings = self.holdings_list[selected_index]

            self.update_holdings_window = tk.Toplevel(self)
            self.update_holdings_window.update_idletasks()
            x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.update_holdings_window.winfo_width() // 2
            y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.update_holdings_window.winfo_height() // 2
            self.update_holdings_window.geometry(f"+{x}+{y}")

            self.update_holdings_window.title("Modifica Holdings")

            # Copia il contenuto di add_frame nella nuova finestra
            add_frame = tk.Frame(self.update_holdings_window)
            add_frame.pack(pady=10)

            # Descrizione dell'elemento <holdings>
            description_label = tk.Label(
                add_frame,
                text="Il contenuto dell'elemento <holdings> è di tipo xsd:sequence, vale a dire che è\n"
                     "costituito da una sequenza di elementi. Nello specifico, l'elemento <holdings> contiene i\n"
                     "seguenti elementi, tutti opzionali.",
                justify=tk.LEFT,
            )
            description_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

            id_label = tk.Label(add_frame, text="Holdings ID")
            id_label.grid(row=1, column=0, sticky=tk.W)
            self.id_entry = tk.Entry(add_frame)
            self.id_entry.grid(row=2, column=0)
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, selected_holdings.get_holdings_id())
            ToolTip(self.id_entry,
                    text="ID: di tipo xsd:ID, serve a definire un identificatore univoco all'interno del \n"
                         "record MAG cui è possibile fare riferimento da altri luoghi del medesimo record. \n"
                         "L'attributo trova la sua utilità qualora vi sia la necessità di dichiarare \n"
                         "diversi <holdings>.")

            library_label = tk.Label(add_frame, text="Library")
            library_label.grid(row=1, column=1, sticky=tk.W)
            self.library_entry = tk.Entry(add_frame)
            self.library_entry.grid(row=2, column=1)
            self.library_entry.delete(0, tk.END)
            self.library_entry.insert(0, selected_holdings.get_library())
            ToolTip(self.library_entry,
                    text="Library: contiene il nome dell'istituzione proprietaria dell'oggetto analogico o \n"
                         "di parte dell'oggetto analogico. Di tipo xsd:string, è opzionale e non \n"
                         "ripetibile.")

            inventory_label = tk.Label(add_frame, text="Inventory")
            inventory_label.grid(row=1, column=2, sticky=tk.W)
            self.inventory_entry = tk.Entry(add_frame)
            self.inventory_entry.grid(row=2, column=2)
            self.inventory_entry.delete(0, tk.END)
            self.inventory_entry.insert(0, selected_holdings.get_inventory_number())
            ToolTip(self.inventory_entry,
                    text="Inventory: contiene il numero di inventario attribuito all'oggetto analogico \n"
                         "dall'istituzione che lo possiede. Di tipo xsd:string, è opzionale e non \n"
                         "ripetibile.")

            # table shelfmarks pre-filled
            frame_shelfmarks = tk.Frame(add_frame)
            frame_shelfmarks.grid(row=2, column=3)
            tree_frame_shelfmarks = tk.Frame(frame_shelfmarks)
            tree_frame_shelfmarks.pack(pady=10)
            ToolTip(tree_frame_shelfmarks, text="Shelfmark: contiene la collocazione dell'oggetto digitale \n"
                                                "all'interno del catalogo dell'istituzione che lo possiede. Di tipo \n"
                                                "xsd:string, è opzionale e ripetibile. Per l'elemento è definito un \n"
                                                "attributo: - type : si usa per definire il tipo di collocazione nel \n"
                                                "caso di collocazioni plurime, per esempio quando si vuole registrare "
                                                "\n"
                                                "una collocazione antica e una moderna. L'attributo è opzionale e il \n"
                                                "suo contenuto è xsd:string.")
            tree_vertical_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
            tree_vertical_scroll_shelfmarks.pack(side=tk.RIGHT, fill=tk.Y)

            self.table_shelfmarks = TreeviewEditable(tree_frame_shelfmarks,
                                                     yscrollcommand=tree_vertical_scroll_shelfmarks.set)
            tree_vertical_scroll_shelfmarks.config(command=self.table_shelfmarks.yview)
            self.table_shelfmarks['columns'] = ("type", "value")
            self.table_shelfmarks.column("#0", width=0, stretch=tk.NO)
            self.table_shelfmarks.column("type", anchor=tk.W, width=120)
            self.table_shelfmarks.column("value", anchor=tk.W, width=120)

            # create headings
            self.table_shelfmarks.heading("#0", text="Label", anchor=tk.W)
            self.table_shelfmarks.heading("type", text="Type", anchor=tk.W)
            self.table_shelfmarks.heading("value", text="Value", anchor=tk.W)
            self.table_shelfmarks.pack()

            for shelfmark in selected_holdings.get_shelfmarks():
                self.table_shelfmarks.insert(parent='', index=tk.END, values=(shelfmark.type, shelfmark.value))

            button_add_shelfmark = tk.Button(frame_shelfmarks, text="Aggiungi shelfmark", command=self._add_shelfmark)
            button_add_shelfmark.pack(pady=5)

            # Bottoni per confermare o annullare l'aggiornamento
            buttons_frame = tk.Frame(self.update_holdings_window)
            buttons_frame.pack(pady=5)

            button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_update_holdings)
            button_confirm.grid(row=0, column=0)

            button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.update_holdings_window.destroy)
            button_cancel.grid(row=0, column=1)
        else:
            messagebox.showerror("Errore", "Seleziona una riga nella tabella degli holdings")

    def _confirm_update_holdings(self):
        if not self.id_entry.get() and self.holdings_list and len(self.holdings_list) > 1:
            messagebox.showerror("Attenzione", "Data la presenza di più holdings è necessario definire un holdings id")
        else:
            item_id = self.table_holdings.focus()
            if item_id is not None and item_id != '':
                shelfmarks = []
                shelfmarks_str = ''
                for item in self.table_shelfmarks.get_children():
                    values = self.table_shelfmarks.item(item, 'values')
                    shelfmark = Shelfmark(values[0], values[1])
                    shelfmarks.append(shelfmark)
                    shelfmarks_str += f"{str(shelfmark)} - "
                selected_index = self.table_holdings.index(item_id)
                selected_holdings = self.holdings_list[selected_index]
                selected_holdings.set_holdings_id(self.id_entry.get())
                selected_holdings.set_library(self.library_entry.get())
                selected_holdings.set_inventory_number(self.inventory_entry.get())
                selected_holdings.set_shelfmarks(shelfmarks)
                self.table_holdings.item(item_id,
                                         text="Parent",
                                         values=(
                                             self.id_entry.get(),
                                             self.library_entry.get(),
                                             self.inventory_entry.get(),
                                             shelfmarks_str)
                                         )
                self.update_holdings_window.destroy()

    def _add_shelfmark(self):
        type = simpledialog.askstring("Input", "Inserisci Shelfmark Type:")
        value = simpledialog.askstring("Input", "Inserisci Shelfmark Value:")
        self.table_shelfmarks.insert(parent='', index=tk.END, values=(type, value))

    def _remove_all(self):
        for record in self.table_holdings.get_children():
            self.table_holdings.delete(record)
        self.controller.session[Utils.KEY_SESSION_HOLDINGS] = []
        self.holdings_list.clear()

    def _remove_selected(self):
        selected = self.table_holdings.selection()
        for item_id in selected:
            selected_index = self.table_holdings.index(item_id)
            self.table_holdings.delete(item_id)
            self.holdings_list.pop(selected_index)

    def check_data(self):
        ret = True
        if len(self.holdings_list) > 1:
            for holdings in self.holdings_list:
                ret &= (holdings.get_holdings_id() != "")
        if ret:
            super().save_to_session(
                (Utils.KEY_SESSION_HOLDINGS, self.holdings_list)
            )
        else:
            messagebox.showerror("Attenzione",
                                 "Data la presenza di più holdings è necessario per ciascuno specificare un holdings id")
        return ret
