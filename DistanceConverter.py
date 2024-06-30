import tkinter as tk
from tkinter import ttk


class DistanceConverter(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Distance Converter")
        self.frames = dict()

        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky=tk.EW)
        feet_to_metres = FeetToMetres(container, self)
        feet_to_metres.grid(row=0, column=0, sticky=tk.NSEW )
        self.frames[FeetToMetres] = feet_to_metres

        metres_to_feet = MetresToFeet(container, self)
        metres_to_feet.grid(row=0, column=0, sticky=tk.NSEW)
        self.frames[MetresToFeet] = metres_to_feet


    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class MetresToFeet(tk.Frame):
    def __init__(self, container, controller,  **kwargs):
        super().__init__(container, **kwargs)
        self.controller = controller

        self.metres_value = tk.StringVar()
        self.feet_value = tk.StringVar(value="Feet shown here")

        metres_label = ttk.Label(self, text="Metres:")
        metres_input = ttk.Entry(self, width=10, textvariable=self.metres_value)
        feet_label = ttk.Label(self, text="Feet:")
        feet_display = ttk.Label(self, textvariable=self.feet_value)
        calc_button = ttk.Button(self, text="Calculate", command=self.calculate)

        metres_label.grid(column=0, row=0, sticky=tk.W)
        metres_input.grid(column=1, row=0, sticky=tk.EW)
        metres_input.focus()

        feet_label.grid(column=0, row=1, sticky=tk.W)
        feet_display.grid(column=1, row=1, sticky=tk.EW)

        calc_button.grid(column=0, row=2, columnspan=2)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        switch_page_button = ttk.Button(self,
                                        text="Switch to metres conversion",
                                        command=lambda: self.controller.show_frame(FeetToMetres))
        switch_page_button.grid(column=0, row=3, columnspan=2, sticky=tk.EW)

    def calculate(self, *args):
        try:
            metres = float(self.metres_value.get())
            feet = metres * 3.28084
            print(f'{metres} metres are equal to {feet: .3f} feet.')
            self.feet_value.set(f'{feet: .3f}')
        except ValueError:
            pass

class FeetToMetres(tk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        self.controller = controller
        self.feet_value = tk.StringVar()
        self.metres_value = tk.StringVar(value="Metres shown here")

        feet_label = ttk.Label(self, text="Feet:")
        feet_input = ttk.Entry(self, width=10, textvariable=self.feet_value)
        metres_label = ttk.Label(self, text="Metres:")
        metres_display = ttk.Label(self, textvariable=self.metres_value)
        calc_button = ttk.Button(self, text="Calculate", command=self.calculate)

        feet_label.grid(column=0, row=0, sticky=tk.W)
        feet_input.grid(column=1, row=0, sticky=tk.EW)
        feet_input.focus()

        metres_label.grid(column=0, row=1, sticky=tk.W)
        metres_display.grid(column=1, row=1, sticky=tk.EW)

        calc_button.grid(column=0, row=2, columnspan=2)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        switch_page_button = ttk.Button(self,
                                        text="Switch to feet conversion",
                                        command=lambda: self.controller.show_frame(MetresToFeet))
        switch_page_button.grid(column=0, row=3, columnspan=2, sticky=tk.EW)

    def calculate(self, *args):
        try:
            feet = float(self.feet_value.get())
            metres = feet / 3.28084
            print(f'{feet} feet is equal to {metres: .3f} metres.')
            self.metres_value.set(f'{metres: .3f}')
        except ValueError:
            pass


root = DistanceConverter()
root.mainloop()
