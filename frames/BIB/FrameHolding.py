from tkinter import ttk
from tkinter import simpledialog
import tkinter as tk
import Utils
from UI.TreeviewEdit import TreeviewEdit
from frames.CustomFrame import CustomFrame
from model.Holding import Shelfmark, Holding


class FrameHolding(CustomFrame):
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

        tree_vertical_scroll_holdings = tk.Scrollbar(tree_frame)
        tree_vertical_scroll_holdings.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_holdings = tk.Scrollbar(tree_frame)
        tree_horizontal_scroll_holdings.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_holdings = ttk.Treeview(tree_frame, yscrollcommand=tree_vertical_scroll_holdings.set, xscrollcommand=tree_horizontal_scroll_holdings.set)
        tree_vertical_scroll_holdings.config(command=self.table_holdings.yview)
        tree_horizontal_scroll_holdings.config(command=self.table_holdings.xview)

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
            row = (holding.id, holding.library, holding.inventory, holding.get_string_shelfmarks())
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

        shelfmarks_label = tk.Label(add_frame, text="Shelfmarks")
        shelfmarks_label.grid(row=0, column=3)

        # entry
        self.id_entry_var = tk.StringVar()
        self.id_entry = tk.Entry(add_frame)
        self.id_entry.grid(row=1, column=0)

        self.library_entry = tk.Entry(add_frame)
        self.library_entry.grid(row=1, column=1)

        self.inventory_entry = tk.Entry(add_frame)
        self.inventory_entry.grid(row=1, column=2)

        #table shelfmarks
        tree_frame_shelfmarks = tk.Frame(add_frame)
        tree_frame_shelfmarks.grid(row=1, column=3)
        tree_vertical_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
        tree_vertical_scroll_shelfmarks.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_shelfmarks = tk.Scrollbar(tree_frame_shelfmarks)
        tree_horizontal_scroll_shelfmarks.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_shelfmarks = TreeviewEdit(tree_frame_shelfmarks, yscrollcommand=tree_vertical_scroll_shelfmarks.set, xscrollcommand=tree_horizontal_scroll_shelfmarks.set)
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

        # buttons
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_holding = tk.Button(buttons_frame, text="Aggiungi holding", command=self._add_holding)
        button_add_holding.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_holding = tk.Button(buttons_frame, text="Rimuovi holding selezionati", command=self._remove_selected)
        button_remove_holding.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Aggiorna holding", command=self._update_holding)
        button_update_record.grid(row=0, column=3)

        button_add_shelfmark = tk.Button(buttons_frame, text="Aggiungi shelfmark", command=self._add_shelfmark)
        button_add_shelfmark.grid(row=0, column=4)

        self.table_holdings.bind("<Double-1>", self._clicker)
        self.table_holdings.bind("<ButtonRelease-1>", self._clicker)

    def _add_holding(self):
        shelfmarks = []
        shelfmarks_str = ""
        for item in self.table_shelfmarks.get_children():
            values = self.table_shelfmarks.item(item, 'values')
            shelfmark = Shelfmark(values[0],values[1])
            shelfmarks_str += (str(shelfmark) + " - ")
            shelfmarks.append(shelfmark)

        row = (self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), shelfmarks_str)
        holding = Holding(self.id_entry.get(), self.library_entry.get(), self.inventory_entry.get(), shelfmarks)
        self.table_holdings.insert(parent='', index=tk.END, text="Parent", values=row, iid=self.count)
        self.holdings.append(holding)
        self.count += 1
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())

    def _add_shelfmark(self):
        type = simpledialog.askstring("Input", "Enter Shelfmark Type:")
        value = simpledialog.askstring("Input", "Enter Shelfmark Value:")
        self.table_shelfmarks.insert(parent='', index=tk.END, values=(type, value))

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
        return True

    def _update_holding(self):
        item_id = self.table_holdings.focus()
        selected_index = self.table_holdings.index(item_id)  # Ottieni l'indice dell'elemento
        selected_holding = self.holdings[selected_index]
        self.table_holdings.item(item_id,
                                 text="Parent",
                                 values=(
                                     self.id_entry.get(),
                                     self.library_entry.get(),
                                     self.inventory_entry.get(),
                                     selected_holding.get_string_shelfmarks()))
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())

    def _select_holding(self):
        self.id_entry.delete(0, tk.END)
        self.library_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.table_shelfmarks.delete(*self.table_shelfmarks.get_children())

        item_id = self.table_holdings.focus()
        selected_index = self.table_holdings.index(item_id)  # Ottieni l'indice dell'elemento
        selected_holding = self.holdings[selected_index]
        if selected_holding is not None:
            self.id_entry.insert(0, selected_holding.get_holding_id())
            self.library_entry.insert(0, selected_holding.get_library())
            self.inventory_entry.insert(0, selected_holding.get_inventory_number())
            for shelfmark in selected_holding.get_shelfmarks():
                self.table_shelfmarks.insert(parent='', index=tk.END, values=(shelfmark.type, shelfmark.value))


    def _clicker(self, event):
        self._select_holding()