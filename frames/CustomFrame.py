import tkinter as tk


class CustomFrame(tk.Frame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.container_frame = tk.Frame(self, bg='lightblue')

        self.container_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__init_frame_buttons(left_button_action, left_button_title, right_button_action, right_button_title)

    def __init_frame_buttons(self, left_button_action, left_button_title, right_button_action, right_button_title):
        button_page_frame = tk.Frame(self)
        button_page_frame.grid(sticky=tk.EW, padx=10)
        button_page_frame.columnconfigure((0, 1), weight=1)

        left_button = tk.Button(button_page_frame, text=left_button_title, command=left_button_action)
        left_button.grid(row=0, column=0, pady=10)

        right_button = tk.Button(button_page_frame, text=right_button_title,
                                 command=lambda: right_button_action() if self.check_data() else None)
        right_button.grid(row=0, column=1, pady=10)

    def check_data(self):
        raise NotImplementedError("Devi implementare il metodo nella sottoclasse")

    def save_to_session(self, *args):
        for coppia in args:
            if isinstance(coppia, tuple) and len(coppia) == 2:
                chiave, valore = coppia
                if isinstance(chiave, str):
                    self.controller.session[chiave] = valore
                else:
                    print(f"Chiave non valida: {coppia}")
            else:
                print(f"Coppia non valida: {coppia}")

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
