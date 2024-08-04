from tkinter import ttk, messagebox
import tkinter as tk

import Utils
from ToolTip import ToolTip
from frames.CustomFrame import CustomFrame
from model.Piece import Piece


class FramePiece(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="""La sezione BIB prevede l'elemento <piece>: contiene dati relativi a un'unità fisica componente di un'unità superiore (es.:
fascicolo di un seriale, parte di una unità bibliografica). L'elemento è opzionale e non ripetibile.""",
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )

        self._init_widgets()

    def _init_widgets(self):
        # radiobutton
        self.var_selection = tk.IntVar()
        self.R1 = tk.Radiobutton(self.container_frame, text="Dati relativi ad una pubblicazione seriale",
                                 variable=self.var_selection, value=0, command=self._on_select_radio_button)
        self.R1.pack(pady=10)
        self.R2 = tk.Radiobutton(self.container_frame, text="Dati relativi all'unità componente di un'opera più vasta",
                                 variable=self.var_selection, value=1, command=self._on_select_radio_button)
        self.R2.pack(pady=10)
        self.R3 = tk.Radiobutton(self.container_frame, text="Nessuna selezione",
                                 variable=self.var_selection, value=2, command=self._on_select_radio_button)
        self.R3.pack(pady=10)
        self.label_selection = tk.Label(self.container_frame)
        self.label_selection.pack(pady=20)

        # frame pubblicazioni seriali
        self.frame_pubblicazioni_seriali = tk.Frame(self.container_frame)
        tk.Label(self.frame_pubblicazioni_seriali, text="Year(*):").pack(pady=(20, 5))
        self.entry_year_var = tk.StringVar()
        entry_year = tk.Entry(self.frame_pubblicazioni_seriali, width=50, textvariable=self.entry_year_var)
        entry_year.focus()
        entry_year.pack()
        ToolTip(entry_year,
                "contiene l'annata di copertura editoriale di una pubblicazione seriale nella forma in cui si trova sulla pubblicazione stessa; per esempio 1913-1914 o anche 1987.")

        tk.Label(self.frame_pubblicazioni_seriali, text="Issue(*):").pack(pady=(10, 5))
        self.entry_issue_var = tk.StringVar()
        entry_issue = tk.Entry(self.frame_pubblicazioni_seriali, width=50, textvariable=self.entry_issue_var)
        entry_issue.pack()
        ToolTip(entry_issue,
                "contiene gli estremi identificatori di un fascicolo di una pubblicazione seriale nella forma in cui si trova sulla pubblicazione stessa; per esempion.° 8.")

        tk.Label(self.frame_pubblicazioni_seriali, text="Stpiece Per(facoltativo):").pack(pady=(10, 5))
        self.entry_stpiece_per_var = tk.StringVar()
        entry_stpiece_per = tk.Entry(self.frame_pubblicazioni_seriali, width=50,
                                     textvariable=self.entry_stpiece_per_var)
        entry_stpiece_per.pack()
        ToolTip(entry_stpiece_per,
                "il campo permette di registrare in una forma normalizzata il riferimento a un fascicolo di un periodico; questo sia per poter scambiare i dati, sia per poter ordinare in modo automatico i vari record.")

        # frame unità componenti
        self.frame_unita_componenti = tk.Frame(self.container_frame)
        tk.Label(self.frame_unita_componenti, text="Part Number(*):").pack(pady=(20, 5))
        self.entry_part_number_var = tk.StringVar()
        entry_part_number = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_part_number_var)
        entry_part_number.focus()
        entry_part_number.pack()
        ToolTip(entry_part_number, "numero di unità componente. Per esempio: 2, IV, 4.5.")

        tk.Label(self.frame_unita_componenti, text="Part Name(*):").pack(pady=(10, 5))
        self.entry_part_name_var = tk.StringVar()
        entry_part_name = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_part_name_var)
        entry_part_name.pack()
        ToolTip(entry_part_name, "nome/titolo di una unità componente. Per esempio: Volume II; Parte III,Tomo 2.")

        tk.Label(self.frame_unita_componenti, text="Stpiece Vol(facoltativo):").pack(pady=(10, 5))
        self.entry_stpiece_vol_var = tk.StringVar()
        entry_stpiece_vol = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_stpiece_vol_var)
        entry_stpiece_vol.pack()
        ToolTip(entry_stpiece_vol, "forma normalizzata del riferimento a una parte di una unità componente.")

        self.var_selection.set(2)
        self._on_select_radio_button()

    def _on_select_radio_button(self):
        string_selection = "Hai selezionato che l'elemento piece contenga dati relativi "
        if self.var_selection.get() == 0:
            string_selection += "ad una pubblicazione seriale"
            self.frame_pubblicazioni_seriali.pack()
            self.frame_unita_componenti.pack_forget()
        elif self.var_selection.get() == 1:
            string_selection += "all'unità componente di un'opera più vasta"
            self.frame_unita_componenti.pack()
            self.frame_pubblicazioni_seriali.pack_forget()
        elif self.var_selection.get() == 2:
            string_selection = "Non hai valorizzato l'elemento piece"
            self.frame_unita_componenti.pack_forget()
            self.frame_pubblicazioni_seriali.pack_forget()
        self.label_selection.config(text=string_selection)

    def check_data(self):
        ret = True
        if self.var_selection.get() == 0:
            if not self.entry_year_var.get():
                messagebox.showerror("Errore", "Il campo 'Year' è obbligatorio.")
                ret = False
            if not self.entry_issue_var.get():
                messagebox.showerror("Errore", "Il campo 'Issue' è obbligatorio.")
                ret = False
            if self.entry_stpiece_per_var.get() and not Utils.validate_sici(self.entry_stpiece_per_var.get()):
                messagebox.showerror("Errore", "Il campo 'Stpiece Per' deve essere conforme al formato SICI.")
                ret = False
            if ret:
                piece = Piece(year=self.entry_year_var.get(), issue=self.entry_issue_var.get(),
                              stpiece_per=self.entry_stpiece_per_var.get())
                super().save_to_session(('Piece', piece))
        elif self.var_selection.get() == 1:
            if not self.entry_part_number_var.get():
                messagebox.showerror("Errore", "Il campo 'Part Number' è obbligatorio.")
                ret = False
            if not self.entry_part_name_var.get():
                messagebox.showerror("Errore", "Il campo 'Part Name' è obbligatorio.")
                ret = False
            if self.entry_stpiece_vol_var.get() and not Utils.validate_bici(self.entry_stpiece_vol_var.get()):
                messagebox.showerror("Errore", "Il campo 'Stpiece Vol' deve essere conforme al formato BICI.")
                ret = False
            if ret:
                piece = Piece(is_pubblicazioni_seriali=self.var_selection.get() == 0,
                              part_number=self.entry_part_number_var.get(), part_name=self.entry_part_name_var.get(),
                              stpiece_vol=self.entry_stpiece_vol_var.get())
                super().save_to_session(('Piece', piece))
        return ret
