import tkinter as tk
from tkinter import messagebox, ttk

from frames.CustomFrame import CustomFrame
from model.Holding import Holding, Shelfmark


class FrameDC(CustomFrame):
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
        self.entry_identifier_var = tk.StringVar()
        self.level_var = tk.StringVar()
        self.entry_title_var = tk.StringVar()
        self.entry_creator_var = tk.StringVar()
        self.entry_publisher_var = tk.StringVar()
        self.entry_subject_var = tk.StringVar()
        self.entry_description_var = tk.StringVar()
        self.entry_contributor_var = tk.StringVar()
        self.entry_date_var = tk.StringVar()
        self.entry_type_var = tk.StringVar()
        self.entry_format_var = tk.StringVar()
        self.entry_source_var = tk.StringVar()
        self.entry_language_var = tk.StringVar()
        self.entry_relation_var = tk.StringVar()
        self.entry_coverage_var = tk.StringVar()
        self.entry_rights_var = tk.StringVar()

        self.scrollable_frame = super()._init_scrollbar(self.container_frame)

        label_level = tk.Label(self.scrollable_frame, text="Level (*):")
        label_level.grid(row=0, column=0)
        self.level_menu_options = {"a: spoglio": "a", "m: monografia": "a", "s: seriale": "s",
                                   "c: raccolta prodotta dall'istituzione": "c"}
        level_menu = tk.OptionMenu(self.scrollable_frame, self.level_var, *self.level_menu_options.keys())
        level_menu.grid(row=0, column=1)

        label_identifier = tk.Label(self.scrollable_frame, text="Identifier (*):")
        label_identifier.grid(row=1, column=0)
        entry_identifier = tk.Entry(self.scrollable_frame, textvariable=self.entry_identifier_var)
        entry_identifier.grid(row=1, column=1)

        label_title = tk.Label(self.scrollable_frame, text="Title:")
        label_title.grid(row=2, column=0)
        entry_title = tk.Entry(self.scrollable_frame, textvariable=self.entry_title_var)
        entry_title.grid(row=2, column=1)

        label_creator = tk.Label(self.scrollable_frame, text="Creator:")
        label_creator.grid(row=3, column=0)
        entry_creator = tk.Entry(self.scrollable_frame, textvariable=self.entry_creator_var)
        entry_creator.grid(row=3, column=1)

        label_publisher = tk.Label(self.scrollable_frame, text="Publisher:")
        label_publisher.grid(row=4, column=0)
        entry_publisher = tk.Entry(self.scrollable_frame, textvariable=self.entry_publisher_var)
        entry_publisher.grid(row=4, column=1)

        label_subject = tk.Label(self.scrollable_frame, text="Subject:")
        label_subject.grid(row=5, column=0)
        entry_subject = tk.Entry(self.scrollable_frame, textvariable=self.entry_subject_var)
        entry_subject.grid(row=5, column=1)

        label_description = tk.Label(self.scrollable_frame, text="Description:")
        label_description.grid(row=6, column=0)
        entry_description = tk.Entry(self.scrollable_frame, textvariable=self.entry_description_var)
        entry_description.grid(row=6, column=1)

        label_contributor = tk.Label(self.scrollable_frame, text="Contributor:")
        label_contributor.grid(row=7, column=0)
        entry_contributor = tk.Entry(self.scrollable_frame, textvariable=self.entry_contributor_var)
        entry_contributor.grid(row=7, column=1)

        label_date = tk.Label(self.scrollable_frame, text="Date:")
        label_date.grid(row=8, column=0)
        entry_date = tk.Entry(self.scrollable_frame, textvariable=self.entry_date_var)
        entry_date.grid(row=8, column=1)

        label_type = tk.Label(self.scrollable_frame, text="Type:")
        label_type.grid(row=9, column=0)
        entry_type = tk.Entry(self.scrollable_frame, textvariable=self.entry_type_var)
        entry_type.grid(row=9, column=1)

        label_format = tk.Label(self.scrollable_frame, text="Format:")
        label_format.grid(row=10, column=0)
        entry_format = tk.Entry(self.scrollable_frame, textvariable=self.entry_format_var)
        entry_format.grid(row=10, column=1)

        label_source = tk.Label(self.scrollable_frame, text="Source:")
        label_source.grid(row=11, column=0)
        entry_source = tk.Entry(self.scrollable_frame, textvariable=self.entry_source_var)
        entry_source.grid(row=11, column=1)

        label_language = tk.Label(self.scrollable_frame, text="Language:")
        label_language.grid(row=12, column=0)
        entry_language = tk.Entry(self.scrollable_frame, textvariable=self.entry_language_var)
        entry_language.grid(row=12, column=1)

        label_relation = tk.Label(self.scrollable_frame, text="Relation:")
        label_relation.grid(row=13, column=0)
        entry_relation = tk.Entry(self.scrollable_frame, textvariable=self.entry_relation_var)
        entry_relation.grid(row=13, column=1)

        label_coverage = tk.Label(self.scrollable_frame, text="Coverage:")
        label_coverage.grid(row=14, column=0)
        entry_coverage = tk.Entry(self.scrollable_frame, textvariable=self.entry_coverage_var)
        entry_coverage.grid(row=14, column=1)

        label_rights = tk.Label(self.scrollable_frame, text="Rights:")
        label_rights.grid(row=15, column=0)
        entry_rights = tk.Entry(self.scrollable_frame, textvariable=self.entry_rights_var)
        entry_rights.grid(row=15, column=1)

    def check_data(self):
        ret = True
        identifier = self.entry_identifier_var.get()
        level = self.level_var.get()
        if not identifier:
            messagebox.showwarning("Attenzione", "Per favore, compila il campo 'dc identifier'.")
            ret = False
        if not level:
            messagebox.showwarning("Attenzione", "Per favore, compila il campo 'level'.")
            ret = False

        if ret:
            super().save_to_session(
                ('Level', self.level_menu_options[self.level_var.get()]),
                ('Identifier', self.entry_identifier_var.get()),
                ('Title', self.entry_title_var.get()),
                ('Creator', self.entry_creator_var.get()),
                ('Publisher', self.entry_publisher_var.get()),
                ('Subject', self.entry_subject_var.get()),
                ('Description', self.entry_description_var.get()),
                ('Contributor', self.entry_contributor_var.get()),
                ('Date', self.entry_date_var.get()),
                ('Type', self.entry_type_var.get()),
                ('Format', self.entry_format_var.get()),
                ('Source', self.entry_source_var.get()),
                ('Language', self.entry_language_var.get()),
                ('Relation', self.entry_relation_var.get()),
                ('Coverage', self.entry_coverage_var.get()),
                ('Rights', self.entry_rights_var.get()),
            )
        return ret
