from tkinter import ttk
import tkinter as tk


class TreeviewEditable(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        #bind double click
        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ['cell', 'tree']:
            return

        column = self.identify_column(event.x)
        #per esempio #0 diventa -1, #1 diventa 0
        column_index = int(column[1:]) - 1
        #per esempio I001
        selected_iid = self.focus()
        #ottengo l'tem pari alla riga
        selected_values = self.item(selected_iid)
        if column == '#0':
            selected_text = selected_values.get('text')
        else:
            selected_text = selected_values.get('values')[column_index]

        column_box = self.bbox(selected_iid, column)
        entry_edit = ttk.Entry(self, width=column_box[2])
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid
        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)
        entry_edit.focus()
        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)
        entry_edit.place(x=column_box[0], y=column_box[1], width=column_box[2], height=column_box[3])

    def on_enter_pressed(self, event):
        new_text = event.widget.get()
        #ad esempio I002
        selected_iid = event.widget.editing_item_iid
        #ad esempio -1,0
        column_index = event.widget.editing_column_index
        if column_index == -1:
            self.item(selected_iid, text=new_text)
        else:
            current_values = self.item(selected_iid).get('values')
            current_values[column_index] = new_text
            self.item(selected_iid, values=current_values)

        event.widget.destroy()
    def on_focus_out(self, event):
        event.widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    column_name = ("vehicle_name" , "year", "colour")
    treeview = TreeviewEditable(root, columns=column_name)
    treeview.heading("#0", text="Vehicle Type")
    treeview.heading("vehicle_name", text="Vehicle Name")
    treeview.heading("year", text="Year")
    treeview.heading("colour", text="Colour")

    sedan_row = treeview.insert(parent="", index="end", text="Sedan")
    treeview.insert(parent=sedan_row, index="end", values=("Nissan Versa","2010","Silver"))
    treeview.insert(parent=sedan_row, index="end", values=("Toyota camry","2012","Blue"))
    treeview.pack(fill=tk.BOTH, expand=1)

    root.mainloop()