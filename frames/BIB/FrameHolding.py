from tkinter import ttk, messagebox
from tkinter import simpledialog
import tkinter as tk
import Utils
from UI.EntryWithPlaceHolder import EntryWithPlaceholder
from UI.TreeviewEditable import TreeviewEditable
from frames.CustomFrame import CustomFrame
from model.Holding import Shelfmark, Holding


class FrameHolding(CustomFrame):
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
        tree_horizontal_scroll_holdings = tk.Scrollbar(tree_frame)
        tree_horizontal_scroll_holdings.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_holdings = ttk.Treeview(tree_frame, yscrollcommand=tree_vertical_scroll_holdings.set, xscrollcommand=tree_horizontal_scroll_holdings.set)
        tree_vertical_scroll_holdings.config(command=self.table_holdings.yview)
        tree_horizontal_scroll_holdings.config(command=self.table_holdings.xview)

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

        self.holding_list = self.controller.session.get(Utils.KEY_SESSION_HOLDING, [])

        for holding in self.holding_list:
            row = (holding.id, holding.library, holding.inventory, holding.get_string_shelfmarks())
            self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row)

        self.table_holdings.pack()
        add_frame = tk.Frame(self.container_frame)
        add_frame.pack(pady=10)

        # entries
        self.id_entry = EntryWithPlaceholder(add_frame, placeholder="Holding ID")
        self.id_entry.grid(row=0, column=0)

        self.library_entry = EntryWithPlaceholder(add_frame, placeholder="Library")
        self.library_entry.grid(row=0, column=1)

        self.inventory_entry = EntryWithPlaceholder(add_frame, placeholder="Inventory")
        self.inventory_entry.grid(row=0, column=2)

        #table shelfmarks
        frame_shelfmarks = tk.Frame(add_frame)
        frame_shelfmarks.grid(row=0, column=3)
        tree_frame_shelfmarks = tk.Frame(frame_shelfmarks)
        tree_frame_shelfmarks.pack(pady=10)
        tree_vertical_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
        tree_vertical_scroll_shelfmarks.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
        tree_horizontal_scroll_shelfmarks.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_shelfmarks = TreeviewEditable(tree_frame_shelfmarks, yscrollcommand=tree_vertical_scroll_shelfmarks.set, xscrollcommand=tree_horizontal_scroll_shelfmarks.set)
        tree_vertical_scroll_shelfmarks.config(command=self.table_shelfmarks.yview)
        tree_horizontal_scroll_shelfmarks.config(command=self.table_shelfmarks.xview)
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

        # buttons
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=5)

        button_add_holding = tk.Button(buttons_frame, text="Aggiungi holding", command=self._add_holding)
        button_add_holding.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_holding = tk.Button(buttons_frame, text="Rimuovi holding selezionati", command=self._remove_selected)
        button_remove_holding.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Aggiorna holding", command=self._update_holding)
        button_update_record.grid(row=0, column=3)

        self.table_holdings.bind("<Double-1>", self._clicker)
        self.table_holdings.bind("<ButtonRelease-1>", self._clicker)

    def _add_holding(self):
        shelfmarks = []
        for item in self.table_shelfmarks.get_children():
            values = self.table_shelfmarks.item(item, 'values')
            shelfmark = Shelfmark(values[0],values[1])
            shelfmarks.append(shelfmark)
        holding = Holding(self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), shelfmarks)
        row = (holding.get_holding_id(), holding.get_library(), holding.get_inventory_number(), holding.get_string_shelfmarks())
        self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row)
        self.holding_list.append(holding)
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())

    def _add_shelfmark(self):
        type = simpledialog.askstring("Input", "Inserisci Shelfmark Type:")
        value = simpledialog.askstring("Input", "Inserisci Shelfmark Value:")
        self.table_shelfmarks.insert(parent='', index=tk.END, values=(type, value))

    def _remove_all(self):
        for record in self.table_holdings.get_children():
            self.table_holdings.delete(record)
        self.controller.session[Utils.KEY_SESSION_HOLDING] = []
        self.holding_list.clear()

    def _remove_selected(self):
        selected = self.table_holdings.selection()
        for item_id in selected:
            selected_index = self.table_holdings.index(item_id)
            self.table_holdings.delete(item_id)
            self.holding_list.pop(selected_index)

    def check_data(self):
        super().save_to_session(
            (Utils.KEY_SESSION_HOLDING, self.holding_list)
        )
        return True

    def _update_holding(self):
        item_id = self.table_holdings.focus()
        if item_id is not None and item_id != '':
            shelfmark_list = []
            shelfmarks_str = ''
            for item in self.table_shelfmarks.get_children():
                values = self.table_shelfmarks.item(item, 'values')
                shelfmark = Shelfmark(values[0], values[1])
                shelfmarks_str += (str(shelfmark) + " - ")
                shelfmark_list.append(shelfmark)
            selected_index = self.table_holdings.index(item_id)
            selected_holding = self.holding_list[selected_index]
            selected_holding.set_holding_id(self.id_entry.get())
            selected_holding.set_library(self.library_entry.get())
            selected_holding.set_inventory_number(self.inventory_entry.get())
            selected_holding.set_shelfmarks(shelfmark_list)
            self.table_holdings.item(item_id,
                                     text="Parent",
                                     values=(
                                         self.id_entry.get(),
                                         self.library_entry.get(),
                                         self.inventory_entry.get(),
                                         shelfmarks_str)
                                     )
            self.id_entry.delete(0, tk.END)
            self.library_entry.delete(0, tk.END)
            self.inventory_entry.delete(0, tk.END)
            self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())
        else:
            messagebox.showerror("Errore", "Seleziona una riga nella tabella degli holdings")

    def _select_holding(self):
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())

        item_id = self.table_holdings.focus()
        selected_index = self.table_holdings.index(item_id)
        selected_holding = self.holding_list[selected_index]
        if selected_holding is not None:
            self.id_entry.insert(0, selected_holding.get_holding_id())
            self.library_entry.insert(0, selected_holding.get_library())
            self.inventory_entry.insert(0, selected_holding.get_inventory_number())
            for shelfmark in selected_holding.get_shelfmarks():
                self.table_shelfmarks.insert(parent='', index=tk.END, values=(shelfmark.type, shelfmark.value))


    def _clicker(self, event):
        self._select_holding()