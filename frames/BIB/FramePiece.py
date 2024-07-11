from tkinter import ttk
import tkinter as tk

import Utils
from frames.CustomFrame import CustomFrame


class FramePiece(CustomFrame):
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
        tree_frame = tk.Frame(self.container_frame)
        tree_frame.pack()

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_holdings = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.table_holdings.yview)
        self.table_holdings['columns'] = ("id", "library", "inventory", "shelfmarks")
        self.table_holdings.column("#0", width=0, stretch=tk.NO)
        self.table_holdings.column("id", anchor=tk.W, width=120)
        self.table_holdings.column("library", anchor=tk.W, width=120)
        self.table_holdings.column("inventory", anchor=tk.W, width=120)
        self.table_holdings.column("shelfmarks", anchor=tk.W, width=120)

        # create headings
        self.table_holdings.heading("#0", text="Label", anchor=tk.W)
        self.table_holdings.heading("id", text="Id", anchor=tk.W)
        self.table_holdings.heading("library", text="Library", anchor=tk.W)
        self.table_holdings.heading("inventory", text="Inventory", anchor=tk.W)
        self.table_holdings.heading("shelfmarks", text="Shelfmarks", anchor=tk.W)
        # populate table

        self.count = 0
        self.holdings = self.controller.session.get(Utils.KEY_SESSION_HOLDING, [])

        for holding in self.holdings:
            row = (holding.id, holding.library, holding.inventory, holding.shelfmark_values)
            self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row, iid=self.count)
            self.count += 1

        self.table_holdings.pack()

        add_frame = tk.Frame(self.container_frame)
        add_frame.pack(pady=10)
        # label
        id_label = tk.Label(add_frame, text="Id")
        id_label.grid(row=0, column=0)

        library_label = tk.Label(add_frame, text="Library")
        library_label.grid(row=0, column=1)

        inventory_label = tk.Label(add_frame, text="Inventory")
        inventory_label.grid(row=0, column=2)

        # entry
        self.id_entry_var = tk.StringVar()
        self.id_entry = tk.Entry(add_frame)
        self.id_entry.grid(row=1, column=0)

        self.library_entry = tk.Entry(add_frame)
        self.library_entry.grid(row=1, column=1)

        self.inventory_entry = tk.Entry(add_frame)
        self.inventory_entry.grid(row=1, column=2)

        # buttons
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_record = tk.Button(buttons_frame, text="Aggiungi holding", command=self._add_holding)
        button_add_record.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_record = tk.Button(buttons_frame, text="Rimuovi holding selezionati", command=self._remove_selected)
        button_remove_record.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Aggiorna holding", command=self._update_holding)
        button_update_record.grid(row=0, column=3)

        self.table_holdings.bind("<Double-1>", self._clicker)
        self.table_holdings.bind("<ButtonRelease-1>", self._clicker)

    def _add_holding(self):
        row = (self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), "shelfmark")
        self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row, iid=self.count)
        self.count += 1
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)

    def _remove_all(self):
        for record in self.table_holdings.get_children():
            self.table_holdings.delete(record)
        self.controller.session[Utils.KEY_SESSION_HOLDING] = []

    def _remove_selected(self):
        selected = self.table_holdings.selection()
        for holding in selected:
            self.table_holdings.delete(holding)

    def check_data(self):
        super().save_to_session(
            (Utils.KEY_SESSION_HOLDING, self.holdings)
        )

    def _update_holding(self):
        selected = self.table_holdings.focus()
        self.table_holdings.item(selected, text="Parent", values=(self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), "update shelfmark"))
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)

    def _select_holding(self):
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)

        selected = self.table_holdings.focus()
        values = self.table_holdings.item(selected, 'values')

        self.id_entry.insert(0, values[0])
        self.library_entry.insert(0, values[1])
        self.inventory_entry.insert(0, values[2])

    def _clicker(self, event):
        self._select_holding()