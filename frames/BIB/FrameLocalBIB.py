from tkinter import ttk, messagebox, simpledialog
import tkinter as tk
import Utils
from UI.TreeviewEditable import TreeviewEditable
from frames.CustomFrame import CustomFrame
from model.LocalBIB import LocalBIB


class FrameLocalBIB(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="""La sezione BIB prevede l'elemento <local_bib>: viene inteso come contenitore per il trasporto di informazioni
specialistiche raccolte durante il processo di digitalizzazione. L'elemento è opzionale e ripetibile.""",
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

        self.table_local_bibs = ttk.Treeview(tree_frame, yscrollcommand=tree_vertical_scroll_local_bibs.set)
        tree_vertical_scroll_local_bibs.config(command=self.table_local_bibs.yview)

        self.table_local_bibs['columns'] = ("geo_coords", "not_dates")
        self.table_local_bibs.column("#0", width=0, stretch=tk.NO)
        self.table_local_bibs.column("geo_coords", anchor=tk.W, width=300)
        self.table_local_bibs.column("not_dates", anchor=tk.W, width=300)

        # create headings
        self.table_local_bibs.heading("#0", text="Label", anchor=tk.W)
        self.table_local_bibs.heading("geo_coords", text="Geo Coords", anchor=tk.W)
        self.table_local_bibs.heading("not_dates", text="Not Dates", anchor=tk.W)

        # populate table
        self.local_bib_list = self.controller.session.get(Utils.KEY_SESSION_LOCAL_BIB, [])

        for local_bib in self.local_bib_list:
            geo_coords_str = local_bib.print_geo_coords()
            not_dates_str = local_bib.print_not_dates()
            row = (geo_coords_str, not_dates_str)
            self.table_local_bibs.insert(parent='', index=tk.END, text="Parent", values=row)

        self.table_local_bibs.pack()

        # buttons
        buttons_frame = tk.Frame(self.container_frame)
        buttons_frame.pack(pady=10)

        button_add_local_bib = tk.Button(buttons_frame, text="Aggiungi local bib", command=self._open_add_local_bib_window)
        button_add_local_bib.grid(row=0, column=0)

        button_remove_all = tk.Button(buttons_frame, text="Rimuovi tutto", command=self._remove_all)
        button_remove_all.grid(row=0, column=1)

        button_remove_local_bib = tk.Button(buttons_frame, text="Rimuovi local bib selezionati",
                                            command=self._remove_selected)
        button_remove_local_bib.grid(row=0, column=2)

        button_update_record = tk.Button(buttons_frame, text="Modifica local bib selezionato", command=self._open_update_local_bib_window)
        button_update_record.grid(row=0, column=3)

    def _open_add_local_bib_window(self):
        # Crea una nuova finestra di dialogo per aggiungere LocalBIB
        self.add_local_bib_window = tk.Toplevel(self)
        self.add_local_bib_window.update_idletasks()
        x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.add_local_bib_window.winfo_width() // 2
        y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.add_local_bib_window.winfo_height() // 2
        self.add_local_bib_window.geometry(f"+{x}+{y}")

        self.add_local_bib_window.title("Aggiungi LocalBIB")

        add_frame = tk.Frame(self.add_local_bib_window)
        add_frame.pack(pady=10)

        # Testo descrittivo
        description_label = tk.Label(
            add_frame,
            text=(
                "- <geo_coord> : di tipo xsd:string, contiene le coordinate geografiche relative a una\n"
                "carta o a una mappa. L'elemento è opzionale e ripetibile. Non sono definiti attributi.\n"
                "- <not_date> : di tipo xsd:string, contiene la data di notifica relativa a un bando o a un\n"
                "editto. L'elemento è opzionale e ripetibile. Non sono definiti attributi."
            ),
            justify=tk.LEFT,
            anchor="w"
        )
        description_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Table geo coord
        frame_geo_coord = tk.Frame(add_frame)
        frame_geo_coord.grid(row=1, column=0)
        tree_frame_geo_coord = tk.Frame(frame_geo_coord)
        tree_frame_geo_coord.pack()
        tree_vertical_scroll_geo_coord = tk.Scrollbar(tree_frame_geo_coord)
        tree_vertical_scroll_geo_coord.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_geo_coord = TreeviewEditable(tree_frame_geo_coord, yscrollcommand=tree_vertical_scroll_geo_coord.set)
        tree_vertical_scroll_geo_coord.config(command=self.table_geo_coord.yview)
        self.table_geo_coord['columns'] = ("geo_coord")
        self.table_geo_coord.column("#0", width=0, stretch=tk.NO)
        self.table_geo_coord.column("geo_coord", anchor=tk.W, width=300)

        self.table_geo_coord.heading("#0", text="Label", anchor=tk.W)
        self.table_geo_coord.heading("geo_coord", text="Geo Coord", anchor=tk.W)

        self.table_geo_coord.pack()
        button_add_geo_coord = tk.Button(frame_geo_coord, text="Aggiungi geo coord", command=self._add_geo_coord)
        button_add_geo_coord.pack(pady=10)

        # Table not date
        frame_not_date = tk.Frame(add_frame)
        frame_not_date.grid(row=1, column=1)
        tree_frame_not_date = tk.Frame(frame_not_date)
        tree_frame_not_date.pack()
        tree_vertical_scroll_not_date = tk.Scrollbar(tree_frame_not_date)
        tree_vertical_scroll_not_date.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_not_date = TreeviewEditable(tree_frame_not_date, yscrollcommand=tree_vertical_scroll_not_date.set)
        tree_vertical_scroll_not_date.config(command=self.table_not_date.yview)
        self.table_not_date['columns'] = ("not_date")
        self.table_not_date.column("#0", width=0, stretch=tk.NO)
        self.table_not_date.column("not_date", anchor=tk.W, width=300)

        self.table_not_date.heading("#0", text="Label", anchor=tk.W)
        self.table_not_date.heading("not_date", text="Not Date", anchor=tk.W)

        self.table_not_date.pack()
        button_add_not_date = tk.Button(frame_not_date, text="Aggiungi not date", command=self._add_not_date)
        button_add_not_date.pack(pady=10)

        # Bottoni per confermare o annullare l'aggiunta
        buttons_frame = tk.Frame(self.add_local_bib_window)
        buttons_frame.pack(pady=5)

        button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_add_local_bib)
        button_confirm.grid(row=0, column=0)

        button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.add_local_bib_window.destroy)
        button_cancel.grid(row=0, column=1)

    def _confirm_add_local_bib(self):
        local_bib = LocalBIB()
        for item in self.table_geo_coord.get_children():
            values = self.table_geo_coord.item(item, 'values')
            local_bib.add_geo_coord(values[0])
        for item in self.table_not_date.get_children():
            values = self.table_not_date.item(item, 'values')
            local_bib.add_not_date(values[0])

        row = (local_bib.print_geo_coords(), local_bib.print_not_dates())
        self.table_local_bibs.insert(parent='', index=tk.END, text="Parent", values=row)
        self.local_bib_list.append(local_bib)
        self.add_local_bib_window.destroy()

    def _open_update_local_bib_window(self):
        item_id = self.table_local_bibs.focus()
        if item_id is not None and item_id != '':
            selected_index = self.table_local_bibs.index(item_id)
            selected_local_bib = self.local_bib_list[selected_index]

            # Crea una nuova finestra di dialogo per l'aggiornamento
            self.update_local_bib_window = tk.Toplevel(self.container_frame.master)
            self.update_local_bib_window.update_idletasks()
            x = self.get_parent().winfo_x() + self.winfo_width() // 2 - self.update_local_bib_window.winfo_width() // 2
            y = self.get_parent().winfo_y() + self.winfo_height() // 2 - self.update_local_bib_window.winfo_height() // 2
            self.update_local_bib_window.geometry(f"+{x}+{y}")
            self.update_local_bib_window.title("Modifica LocalBIB")

            add_frame = tk.Frame(self.update_local_bib_window)
            add_frame.pack(pady=10)

            # Testo descrittivo
            description_label = tk.Label(
                add_frame,
                text=(
                    "- <geo_coord> : di tipo xsd:string, contiene le coordinate geografiche relative a una\n"
                    "carta o a una mappa. L'elemento è opzionale e ripetibile. Non sono definiti attributi.\n"
                    "- <not_date> : di tipo xsd:string, contiene la data di notifica relativa a un bando o a un\n"
                    "editto. L'elemento è opzionale e ripetibile. Non sono definiti attributi."
                ),
                justify=tk.LEFT,
                anchor="w"
            )
            description_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            # Table geo coord
            frame_geo_coord = tk.Frame(add_frame)
            frame_geo_coord.grid(row=1, column=0)
            tree_frame_geo_coord = tk.Frame(frame_geo_coord)
            tree_frame_geo_coord.pack()
            tree_vertical_scroll_geo_coord = tk.Scrollbar(tree_frame_geo_coord)
            tree_vertical_scroll_geo_coord.pack(side=tk.RIGHT, fill=tk.Y)

            self.table_geo_coord = TreeviewEditable(tree_frame_geo_coord, yscrollcommand=tree_vertical_scroll_geo_coord.set)
            tree_vertical_scroll_geo_coord.config(command=self.table_geo_coord.yview)
            self.table_geo_coord['columns'] = ("geo_coord")
            self.table_geo_coord.column("#0", width=0, stretch=tk.NO)
            self.table_geo_coord.column("geo_coord", anchor=tk.W, width=300)

            self.table_geo_coord.heading("#0", text="Label", anchor=tk.W)
            self.table_geo_coord.heading("geo_coord", text="Geo Coord", anchor=tk.W)

            self.table_geo_coord.pack()
            for geo_coord in selected_local_bib.get_geo_coords():
                self.table_geo_coord.insert(parent='', index=tk.END, values=[geo_coord])

            button_add_geo_coord = tk.Button(frame_geo_coord, text="Aggiungi geo coord", command=self._add_geo_coord)
            button_add_geo_coord.pack(pady=10)

            # Table not date
            frame_not_date = tk.Frame(add_frame)
            frame_not_date.grid(row=1, column=1)
            tree_frame_not_date = tk.Frame(frame_not_date)
            tree_frame_not_date.pack()
            tree_vertical_scroll_not_date = tk.Scrollbar(tree_frame_not_date)
            tree_vertical_scroll_not_date.pack(side=tk.RIGHT, fill=tk.Y)

            self.table_not_date = TreeviewEditable(tree_frame_not_date, yscrollcommand=tree_vertical_scroll_not_date.set)
            tree_vertical_scroll_not_date.config(command=self.table_not_date.yview)
            self.table_not_date['columns'] = ("not_date")
            self.table_not_date.column("#0", width=0, stretch=tk.NO)
            self.table_not_date.column("not_date", anchor=tk.W, width=300)

            self.table_not_date.heading("#0", text="Label", anchor=tk.W)
            self.table_not_date.heading("not_date", text="Not Date", anchor=tk.W)

            self.table_not_date.pack()
            for not_date in selected_local_bib.get_not_dates():
                self.table_not_date.insert(parent='', index=tk.END, values=[not_date])

            button_add_not_date = tk.Button(frame_not_date, text="Aggiungi not date", command=self._add_not_date)
            button_add_not_date.pack(pady=10)

            # Bottoni per confermare o annullare l'aggiornamento
            buttons_frame = tk.Frame(self.update_local_bib_window)
            buttons_frame.pack(pady=5)

            button_confirm = tk.Button(buttons_frame, text="Conferma", command=self._confirm_update_local_bib)
            button_confirm.grid(row=0, column=0)

            button_cancel = tk.Button(buttons_frame, text="Annulla", command=self.update_local_bib_window.destroy)
            button_cancel.grid(row=0, column=1)
        else:
            messagebox.showerror("Errore", "Seleziona una riga nella tabella dei local bib.")

    def _confirm_update_local_bib(self):
        item_id = self.table_local_bibs.focus()
        if item_id is not None and item_id != '':
            geo_coord_list = []
            for item in self.table_geo_coord.get_children():
                values = self.table_geo_coord.item(item, 'values')
                geo_coord_list.append(values[0])
            not_date_list = []
            for item in self.table_not_date.get_children():
                values = self.table_not_date.item(item, 'values')
                not_date_list.append(values[0])

            selected_index = self.table_local_bibs.index(item_id)
            selected_local_bib = self.local_bib_list[selected_index]
            selected_local_bib.set_geo_coords(geo_coord_list)
            selected_local_bib.set_not_dates(not_date_list)

            self.table_local_bibs.item(item_id, values=[selected_local_bib.print_geo_coords(),
                                                        selected_local_bib.print_not_dates()])
            self.update_local_bib_window.destroy()

    def _add_geo_coord(self):
        geo_coord = simpledialog.askstring("Input", "Inserisci Geo Coord:")
        if geo_coord:
            self.table_geo_coord.insert(parent='', index=tk.END, values=[geo_coord])

    def _add_not_date(self):
        not_date = simpledialog.askstring("Input", "Inserisci Not Date:")
        if not_date:
            self.table_not_date.insert(parent='', index=tk.END, values=[not_date])

    def _remove_all(self):
        for record in self.table_local_bibs.get_children():
            self.table_local_bibs.delete(record)
        self.controller.session[Utils.KEY_SESSION_LOCAL_BIB] = []
        self.local_bib_list.clear()

    def _remove_selected(self):
        selected = self.table_local_bibs.selection()
        for item_id in selected:
            selected_index = self.table_local_bibs.index(item_id)
            self.table_local_bibs.delete(item_id)
            self.local_bib_list.pop(selected_index)

    def check_data(self):
        super().save_to_session(
            (Utils.KEY_SESSION_LOCAL_BIB, self.local_bib_list)
        )
        return True