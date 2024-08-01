import tkinter as tk
from tkinter import ttk


class CustomFrame(tk.Frame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.container_frame = tk.Frame(self)

        self.container_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__init_frame_buttons(left_button_action, left_button_title, right_button_action, right_button_title)

    def __init_frame_buttons(self, left_button_action, left_button_title, right_button_action, right_button_title):
        button_page_frame = tk.Frame(self)
        button_page_frame.grid(sticky=tk.EW, padx=10)
        button_page_frame.columnconfigure((0, 1), weight=1)

        self.left_button = ttk.Button(button_page_frame, text=left_button_title, command=left_button_action)
        self.left_button.grid(row=0, column=0, pady=10)

        self.right_button = ttk.Button(button_page_frame, text=right_button_title,
                                       command=lambda: right_button_action() if self.check_data() else None)
        self.right_button.grid(row=0, column=1, pady=10)

    def check_data(self):
        raise NotImplementedError("Devi implementare il metodo nella sottoclasse")

    def save_to_session(self, *args):
        for coppia in args:
            if isinstance(coppia, tuple) and len(coppia) == 2:
                chiave, valore = coppia
                if isinstance(chiave, str):
                    self.controller.session[chiave] = valore
                    print(f"Coppia salvata: {coppia}")
                else:
                    print(f"Chiave non valida: {coppia}")
            else:
                print(f"Coppia non valida: {coppia}")

    def disable_right_button(self):
        self.right_button['state'] = "disabled"

    def enable_right_button(self):
        self.right_button['state'] = "enabled"
