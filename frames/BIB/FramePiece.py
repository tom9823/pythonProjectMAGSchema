from tkinter import ttk
import tkinter as tk

import Utils
from ToolTip import ToolTip
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
        #radiobutton
        self.var_selection = tk.IntVar()
        self.R1 = tk.Radiobutton(self.container_frame, text="dati relativi ad una pubblicazione seriale", variable=self.var_selection, value=0, command=self._on_select_radio_button)
        self.R1.pack(pady=10)
        self.R2 = tk.Radiobutton(self.container_frame, text="dati relativi all'unità componente di un'opera più vasta", variable=self.var_selection, value=1, command=self._on_select_radio_button)
        self.R2.pack(pady=10)
        self.label_selection = tk.Label(self.container_frame)
        self.label_selection.pack(pady=20)

        #frame pubblicazioni seriali
        self.frame_pubblicazioni_seriali = tk.Frame(self.container_frame)
        tk.Label(self.frame_pubblicazioni_seriali, text="Year:").pack(pady=(20, 5))
        self.entry_year_var = tk.StringVar()
        entry_year = tk.Entry(self.frame_pubblicazioni_seriali, width=50, textvariable=self.entry_year_var)
        entry_year.focus()
        entry_year.pack()
        ToolTip(entry_year,
                "contiene l'annata di copertura editoriale di una pubblicazione seriale nella forma in cui si trova sulla pubblicazione stessa; per esempio 1913-1914 o anche 1987.")

        tk.Label(self.frame_pubblicazioni_seriali, text="Issue:").pack(pady=(10, 5))
        self.entry_issue_var = tk.StringVar()
        entry_issue = tk.Entry(self.frame_pubblicazioni_seriali, width=50, textvariable=self.entry_issue_var)
        entry_issue.pack()
        ToolTip(entry_issue,"contiene gli estremi identificatori di un fascicolo di una pubblicazione seriale nella forma in cui si trova sulla pubblicazione stessa; per esempion.° 8.")

        tk.Label(self.frame_pubblicazioni_seriali, text="Stpiece Per:").pack(pady=(10, 5))
        self.entry_stpiec_per_var = tk.StringVar()
        entry_stpiec_per = tk.Entry(self.frame_pubblicazioni_seriali, width=50, textvariable=self.entry_stpiec_per_var)
        entry_stpiec_per.pack()
        ToolTip(entry_stpiec_per,"il campo permette di registrare in una forma normalizzata il riferimento a un fascicolo di un periodico; questo sia per poter scambiare i dati, sia per poter ordinare in modo automatico i vari record.")

        #frame unità componenti
        self.frame_unita_componenti = tk.Frame(self.container_frame)
        tk.Label(self.frame_unita_componenti, text="Part Number:").pack(pady=(20, 5))
        self.entry_part_number_var = tk.StringVar()
        entry_part_number = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_part_number_var)
        entry_part_number.focus()
        entry_part_number.pack()
        ToolTip(entry_part_number, "numero di unità componente. Per esempio: 2, IV, 4.5.")

        tk.Label(self.frame_unita_componenti, text="Part Name:").pack(pady=(10, 5))
        self.entry_part_name_var = tk.StringVar()
        entry_part_name = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_part_name_var)
        entry_part_name.pack()
        ToolTip(entry_part_name,"nome/titolo di una unità componente. Per esempio: Volume II; Parte III,Tomo 2.")

        tk.Label(self.frame_unita_componenti, text="Stpiece Vol:").pack(pady=(10, 5))
        self.entry_stpiece_vol_var = tk.StringVar()
        entry_stpiece_vol = tk.Entry(self.frame_unita_componenti, width=50, textvariable=self.entry_stpiece_vol_var)
        entry_stpiece_vol.pack()
        ToolTip(entry_stpiece_vol,"forma normalizzata del riferimento a una parte di una unità componente.")

        self.var_selection.set(0)
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
        self.label_selection.config(text=string_selection)

    def check_data(self):
        return True