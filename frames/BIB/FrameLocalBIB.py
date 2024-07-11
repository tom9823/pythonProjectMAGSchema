from tkinter import ttk, messagebox, simpledialog

import Utils
from UI.TreeviewEdit import TreeviewEdit
from frames.CustomFrame import CustomFrame
import tkinter as tk

from model.LocalBIB import LocalBIB


class FrameLocalBIB(CustomFrame):
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

        tree_vertical_scroll_local_bibs = tk.Scrollbar(tree_frame)
        tree_vertical_scroll_local_bibs.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_local_bibs = tk.Scrollbar(tree_frame)
        tree_horizontal_scroll_local_bibs.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_local_bibs = ttk.Treeview(tree_frame, yscrollcommand=tree_vertical_scroll_local_bibs.set,
                                             xscrollcommand=tree_horizontal_scroll_local_bibs.set)
        tree_vertical_scroll_local_bibs.config(command=self.table_local_bibs.yview)
        tree_horizontal_scroll_local_bibs.config(command=self.table_local_bibs.xview)

        self.table_local_bibs['columns'] = ("geo_coords", "not_dates")
        self.table_local_bibs.column("#0", width=0, stretch=tk.NO)
        self.table_local_bibs.column("geo_coords", anchor=tk.W, width=120)
        self.table_local_bibs.column("not_dates", anchor=tk.W, width=120)

        # create headings
        self.table_local_bibs.heading("#0", text="Label", anchor=tk.W)
        self.table_local_bibs.heading("geo_coords", text="Geo Coords", anchor=tk.W)
        self.table_local_bibs.heading("not_dates", text="Not Dates", anchor=tk.W)
        # populate table
        self.count = 0
        self.local_bibs = self.controller.session.get(Utils.KEY_SESSION_LOCAL_BIB, [])

        for local_bib in self.local_bibs:
            geo_coords_str = local_bib.print_geo_coords()
            not_dates_str = local_bib.print_not_dates()
            row = (geo_coords_str, not_dates_str)
            self.table_local_bibs.insert(parent='', index=tk.END, text="Parent", values=row, iid=self.count)
            self.count += 1

        self.table_local_bibs.pack()
        #add frame
        add_frame = tk.Frame(self.container_frame)
        add_frame.pack(pady=10)

        # table geo coord
        frame_geo_coord = tk.Frame(add_frame)
        frame_geo_coord.grid(row=0, column=0)
        tree_frame_geo_coord = tk.Frame(frame_geo_coord)
        tree_frame_geo_coord.pack()
        tree_vertical_scroll_geo_coord = tk.Scrollbar(tree_frame_geo_coord)
        tree_vertical_scroll_geo_coord.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_geo_coord = tk.Scrollbar(tree_frame_geo_coord)
        tree_horizontal_scroll_geo_coord.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_geo_coord = TreeviewEdit(tree_frame_geo_coord, yscrollcommand=tree_vertical_scroll_geo_coord.set,
                                            xscrollcommand=tree_horizontal_scroll_geo_coord.set)
        tree_vertical_scroll_geo_coord.config(command=self.table_geo_coord.yview)
        tree_horizontal_scroll_geo_coord.config(command=self.table_geo_coord.xview)
        self.table_geo_coord['columns'] = ("geo_coord")
        self.table_geo_coord.column("#0", width=0, stretch=tk.NO)
        self.table_geo_coord.column("geo_coord", anchor=tk.W, width=120)

        # create headings
        self.table_geo_coord.heading("#0", text="Label", anchor=tk.W)
        self.table_geo_coord.heading("geo_coord", text="Geo Coord", anchor=tk.W)

        self.table_geo_coord.pack()
        button_add_geo_coord = tk.Button(frame_geo_coord, text="Aggiungi geo coord", command=self._add_geo_coord)
        button_add_geo_coord.pack(pady=10)

        # table not date
        frame_not_date = tk.Frame(add_frame)
        frame_not_date.grid(row=0, column=1)
        tree_frame_not_date = tk.Frame(frame_not_date)
        tree_frame_not_date.pack()
        tree_vertical_scroll_not_date = tk.Scrollbar(tree_frame_not_date)
        tree_vertical_scroll_not_date.pack(side=tk.RIGHT, fill=tk.Y)
        tree_horizontal_scroll_not_date = tk.Scrollbar(tree_frame_not_date)
        tree_horizontal_scroll_not_date.pack(side=tk.BOTTOM, fill=tk.X)

        self.table_not_date = TreeviewEdit(tree_frame_not_date, yscrollcommand=tree_vertical_scroll_not_date.set,
                                            xscrollcommand=tree_horizontal_scroll_not_date.set)
        tree_vertical_scroll_not_date.config(command=self.table_not_date.yview)
        tree_horizontal_scroll_not_date.config(command=self.table_not_date.xview)
        self.table_not_date['columns'] = ("not_date")
        self.table_not_date.column("#0", width=0, stretch=tk.NO)
        self.table_not_date.column("not_date", anchor=tk.W, width=120)

        # create headings
        self.table_not_date.heading("#0", text="Label", anchor=tk.W)
        self.table_not_date.heading("not_date", text="Not Date", anchor=tk.W)

        self.table_not_date.pack()
        button_add_not_date = tk.Button(frame_not_date, text="Aggiungi not date", command=self._add_not_date)
        button_add_not_date.pack(pady=10)

        # buttons
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_local_bib = tk.Button(buttons_frame, text="Aggiungi local bib", command=self._add_local_bib)
        button_add_local_bib.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_local_bib = tk.Button(buttons_frame, text="Rimuovi local bib selezionati", command=self._remove_selected)
        button_remove_local_bib.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Aggiorna local bib", command=self._update_local_bib)
        button_update_record.grid(row=0, column=3)

        self.table_local_bibs.bind("<Double-1>", self._clicker)
        self.table_local_bibs.bind("<ButtonRelease-1>", self._clicker)

    def _add_local_bib(self):
        local_bib = LocalBIB()
        for item in self.table_geo_coord.get_children():
            values = self.table_geo_coord.item(item, 'values')
            local_bib.add_geo_coord(values[0])
        for item in self.table_not_date.get_children():
            values = self.table_geo_coord.item(item, 'values')
            local_bib.add_not_date(values[0])

        row = (local_bib.print_geo_coords(), local_bib.print_not_dates())
        self.table_local_bibs.insert(parent='', index=tk.END, text="Parent", values=row, iid=self.count)
        self.local_bibs.append(local_bib)
        self.count += 1
        self.table_geo_coord.delete(*self.table_geo_coord.get_children())
        self.table_not_date.delete(*self.table_not_date.get_children())

    def _add_geo_coord(self):
        geo_coord = simpledialog.askstring("Input", "Inserisci Geo Coord:")
        self.table_geo_coord.insert(parent='', index=tk.END, values=(geo_coord))

    def _add_not_date(self):
        not_date = simpledialog.askstring("Input", "Inserisci Not Date:")
        self.table_not_date.insert(parent='', index=tk.END, values=(not_date))

    def _remove_all(self):
        for record in self.table_local_bibs.get_children():
            self.table_local_bibs.delete(record)
        self.controller.session[Utils.KEY_SESSION_HOLDING] = []

    def _remove_selected(self):
        selected = self.table_local_bibs.selection()
        for holding in selected:
            self.table_local_bibs.delete(holding)

    def check_data(self):
        super().save_to_session(
            (Utils.KEY_SESSION_LOCAL_BIB, self.local_bibs)
        )
        return True

    def _update_local_bib(self):
        item_id = self.table_local_bibs.focus()
        selected_index = self.table_local_bibs.index(item_id)
        selected_local_bib = self.local_bibs[selected_index]
        self.table_local_bibs.item(item_id, text="", values=(selected_local_bib.print_geo_coords(), selected_local_bib.print_not_dates()))

    def _select_local_bib(self):
        self.table_geo_coord.delete(*self.table_geo_coord.get_children())
        self.table_not_date.delete(*self.table_not_date.get_children())

        item_id = self.table_local_bibs.focus()
        selected_index = self.table_local_bibs.index(item_id)  # Ottieni l'indice dell'elemento
        selected_local_bib = self.local_bibs[selected_index]
        if selected_local_bib is not None:
            for geo_coord in selected_local_bib.get_geo_coords():
                self.table_geo_coord.insert(parent='', index=tk.END, values=(geo_coord))
            for not_date in selected_local_bib.get_not_dates():
                self.table_not_date.insert(parent='', index=tk.END, values=(not_date))

    def _clicker(self, event):
        self._select_local_bib()