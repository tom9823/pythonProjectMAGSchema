from tkinter import ttk, messagebox
import tkinter as tk

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
        self.holdings = dict()

        self.scrollable_frame = self._init_scrollbar(self.container_frame)

        button_holding_frame = tk.Frame(self.scrollable_frame)
        button_holding_frame.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)
        button_holding_frame.columnconfigure((0, 1), weight=1)
        add_holding_button = tk.Button(button_holding_frame, text="Aggiungi Holding", command=self._add_holding)
        add_holding_button.grid(column=0, row=0)
        modify_holding_button = tk.Button(button_holding_frame, text="Modifica Holding", command=self._modify_holding)
        modify_holding_button.grid(column=1, row=0)

        # Treeview per gli holdings
        self.holdings_tree = ttk.Treeview(self.scrollable_frame,
                                          columns=("ID", "Library", "Inventory Number", "Shelfmarks"),
                                          show="headings")
        self.holdings_tree.heading("ID", text="Holding ID")
        self.holdings_tree.heading("Library", text="Library")
        self.holdings_tree.heading("Inventory Number", text="Inventory Number")
        self.holdings_tree.heading("Shelfmarks", text="Shelfmarks")
        self.holdings_tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def _add_holding(self):
        ModalDialog(self)

    def _modify_holding(self):
        selected_item = self.holdings_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Per favore, seleziona un holding da modificare.")
            return

        item = self.holdings_tree.item(selected_item)
        values = item['values']

        # Find the holding object based on holding ID
        holding_id = str(values[0])
        holding_obj = self.holdings.get(holding_id)
        if holding_obj:
            ModalDialog(self, holding_obj, selected_item)

    def add_holding_to_treeview(self, holding_obj):
        self.holdings[holding_obj.holding_id] = holding_obj
        self.holdings_tree.insert("", "end", values=(
            holding_obj.holding_id, holding_obj.library, holding_obj.inventory_number,
            ", ".join([str(shelfmark) for shelfmark in holding_obj.shelfmark_values])
        ))

    def update_holding_in_treeview(self, holding_obj, item):
        self.holdings[holding_obj.holding_id] = holding_obj
        self.holdings_tree.item(item, values=(
            holding_obj.holding_id, holding_obj.library, holding_obj.inventory_number,
            ", ".join([str(shelfmark) for shelfmark in holding_obj.shelfmark_values])
        ))

class ModalDialog(tk.Toplevel):
    def __init__(self, parent, holding=None, treeview_item=None):
        super().__init__(parent)
        self.parent = parent
        self.holding = holding
        self.treeview_item = treeview_item
        self.title("Add Holding" if holding is None else "Modify Holding")
        self.transient(parent)
        self.grab_set()

        holding_frame = tk.Frame(self)
        holding_frame.pack(fill=tk.X, padx=5, pady=5)
        scrollable_frame = self._init_scrollbar(holding_frame)

        self.holding_id_var = tk.StringVar()
        self.library_var = tk.StringVar()
        self.inventory_number_var = tk.StringVar()
        self.shelfmark_vars = []

        tk.Label(scrollable_frame, text="Holding ID:").grid(row=0, column=0, padx=5, pady=2)
        tk.Entry(scrollable_frame, textvariable=self.holding_id_var).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(scrollable_frame, text="Library:").grid(row=1, column=0, padx=5, pady=2)
        tk.Entry(scrollable_frame, textvariable=self.library_var).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(scrollable_frame, text="Inventory Number:").grid(row=2, column=0, padx=5, pady=2)
        tk.Entry(scrollable_frame, textvariable=self.inventory_number_var).grid(row=2, column=1, padx=5, pady=2)

        self.shelfmarks_container = tk.Frame(scrollable_frame)
        self.shelfmarks_container.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.shelfmark_entries = []
        self._populate_shelfmarks_entries()

        add_shelfmark_button = tk.Button(scrollable_frame, text="Add Shelfmark", command=self._add_shelfmark)
        add_shelfmark_button.grid(row=4, column=0, columnspan=2, pady=5)

        save_button = tk.Button(scrollable_frame, text="Save", command=self._save_holding)
        save_button.grid(row=4, column=1, columnspan=2, pady=5)

        # Populate fields if holding is provided
        if holding:
            self.holding_id_var.set(holding.holding_id)
            self.library_var.set(holding.library)
            self.inventory_number_var.set(holding.inventory_number)

            # Populate shelfmarks entries
            for index, shelfmark in enumerate(holding.shelfmark_values):
                if index < len(self.shelfmark_entries):
                    self.shelfmark_entries[index][0].set(shelfmark.type)
                    self.shelfmark_entries[index][1].set(shelfmark.value)
                else:
                    # If more shelfmarks are present in holding than in UI, add new entries
                    shelfmark_type_var = tk.StringVar()
                    shelfmark_value_var = tk.StringVar()
                    shelfmark_type_var.set(shelfmark.type)
                    shelfmark_value_var.set(shelfmark.value)
                    self.shelfmark_vars.append((shelfmark_type_var, shelfmark_value_var))
                    self._add_shelfmark(shelfmark_type_var, shelfmark_value_var)

    def _populate_shelfmarks_entries(self):
        self._clear_frame(self.shelfmarks_container)
        for index, (type_var, value_var) in enumerate(self.shelfmark_vars):
            shelfmark_frame = tk.Frame(self.shelfmarks_container)
            shelfmark_frame.pack(fill=tk.X, padx=5, pady=2)

            tk.Label(shelfmark_frame, text="Type:").pack(side=tk.LEFT)
            type_entry = tk.Entry(shelfmark_frame, textvariable=type_var)
            type_entry.pack(side=tk.LEFT, padx=5)

            tk.Label(shelfmark_frame, text="Value:").pack(side=tk.LEFT)
            value_entry = tk.Entry(shelfmark_frame, textvariable=value_var)
            value_entry.pack(side=tk.LEFT, padx=5)

            self.shelfmark_entries.append((type_var, value_var))

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _add_shelfmark(self, type_var=None, value_var=None):
        if not type_var:
            type_var = tk.StringVar()
        if not value_var:
            value_var = tk.StringVar()
        self.shelfmark_vars.append((type_var, value_var))
        self._populate_shelfmarks_entries()


    def _save_holding(self):
        holding_id = self.holding_id_var.get()
        library = self.library_var.get()
        inventory_number = self.inventory_number_var.get()
        shelfmarks = [Shelfmark(type_var.get(), value_var.get()) for type_var, value_var in self.shelfmark_vars]

        if not (holding_id or library or inventory_number):
            messagebox.showwarning("Warning", "Stai aggiungendo un holding non valorizzato")
            return

        new_holding = Holding(holding_id, library, inventory_number, shelfmarks)

        if self.holding:
            # Modify existing holding
            self.holding.set_holding_id(holding_id)
            self.holding.set_library(library)
            self.holding.set_inventory_number(inventory_number)
            self.holding.set_shelfmark_values(shelfmarks)

            # Update Treeview
            self.parent.update_holding_in_treeview(self.holding, self.treeview_item)
            messagebox.showinfo("Success", "Holding modificato con successo")
        else:
            # Add new holding
            self.parent.add_local_bib_to_treeview(new_holding)
            messagebox.showinfo("Success", "Holding aggiunto con successo")

        self.destroy()

    def _init_scrollbar(self, container_frame):
        canvas = tk.Canvas(container_frame)
        scrollable_frame = tk.Frame(canvas, bg='red')
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def configure_window_size(event):
            canvas.itemconfig(self.scrollable_window, width=canvas.winfo_width())

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_window_size)

        scrollbar = tk.Scrollbar(container_frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0,column=0, sticky=tk.NSEW)

        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.yview_moveto(1.0)
        return scrollable_frame