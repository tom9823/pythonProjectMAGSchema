from tkinter import ttk, messagebox
import tkinter as tk

import Utils
from ToolTip import ToolTip
from frames.CustomFrame import CustomFrame
from model.IMG import Scanning, Target
from model.Piece import Piece


class FrameIMG2(CustomFrame):
    def __init__(self, parent, controller, left_button_action, left_button_title, right_button_action,
                 right_button_title, **kwargs):
        super().__init__(
            parent=parent,
            controller=controller,
            title_frame="La sezione IMG raccoglie i metadati amministrativi e gestionali relativi alle immagini "
                        "statiche.\nAlcuni di questi dati, in realtà, possono essere raccolti direttamente "
                        "all\'interno della sezione GEN, grazie all\'elemento <img_group>.\nLa sezione IMG utilizza il "
                        "namespace niso: che fa riferimento a uno schema che traduce le linee guida del Data "
                        "Dictionary NISO.\nLa sezione IMG è costituita di una sequenza di elementi <img>, "
                        "uno per ciascuna immagine digitale descritta da MAG.",
            left_button_action=left_button_action,
            left_button_title=left_button_title,
            right_button_action=right_button_action,
            right_button_title=right_button_title,
            **kwargs
        )

        self._init_widgets()

    def _init_widgets(self):
        self.var_selected_millimetric_scale = tk.IntVar(value=0)
        checkbox_millimetric_scale = tk.Checkbutton(self.container_frame,
                                                    text="è presente una scala millimetrica",
                                                    variable=self.var_selected_millimetric_scale, onvalue=1, offvalue=0,
                                                    )
        checkbox_millimetric_scale.pack(pady=(5, 20))

        ttk.Separator(self.container_frame, orient='horizontal').pack(fill='x', padx=20, pady=20)

        self.var_is_target_enabled = tk.IntVar()
        checkbox_target = tk.Checkbutton(self.container_frame,
                                         text="Desidero valorizzare il campo <niso:target> ossia l'eventuale "
                                              "presenza, la tipologia e le modalità d'utilizzo di un target (o scala "
                                              "cromatica) \n durante la scansione dell'oggetto analogico",
                                         variable=self.var_is_target_enabled, onvalue=1, offvalue=0,
                                         command=self.on_checkbox_target_selection)
        checkbox_target.pack()
        self.init_frame_target()

    def check_data(self):
        ret = True
        if self.var_selected_millimetric_scale.get() is not None and self.var_selected_millimetric_scale.get() == 1:
            super().save_to_session((Utils.KEY_SESSION_SCALE, self.var_selected_millimetric_scale.get()))
        if self.var_is_target_enabled.get() is not None and self.var_is_target_enabled.get() == 1:
            target_type = None
            target_id = None
            image_data = None
            performance_data = None
            profiles = None

            # Validate and get target type
            if self.targettype_var.get() == "Esterno":
                target_type = 0
            elif self.targettype_var.get() == "Interno":
                target_type = 1

            # Validate and get target ID
            if self.targetid_entry.get() is not None and self.targetid_entry.get():
                target_id = self.targetid_entry.get()
            else:
                ret = False

            if target_type == 0 and self.imagedata_entry.get() is not None and self.imagedata_entry.get():
                image_data = self.imagedata_entry.get()

            if self.performancedata_entry.get() is not None and self.performancedata_entry.get():
                performance_data = self.performancedata_entry.get()

            if self.profiles_entry.get() is not None and self.profiles_entry.get():
                profiles = self.profiles_entry.get()
            if ret:
                target = Target(
                    target_type=target_type,
                    target_id=target_id,
                    image_data=image_data,
                    performance_data=performance_data,
                    profiles=profiles
                )
                super().save_to_session((Utils.KEY_SESSION_TARGET, target))
            else:
                messagebox.showerror("Errore", "Devi inserire un target ID.")
        return ret

    def init_frame_target(self):
        self.frame_target = ttk.Frame(self.container_frame)

        targettype_label = ttk.Label(self.frame_target, text="<niso:targetType>:")
        targettype_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        targettype_options = ["Esterno", "Interno"]
        self.targettype_var = tk.StringVar()

        targettype_dropdown = ttk.OptionMenu(
            self.frame_target,
            self.targettype_var,
            *targettype_options
        )
        targettype_dropdown.grid(row=0, column=1, pady=5, sticky=tk.EW)
        ToolTip(targettype_dropdown, "Opzionale e non ripetibile, dichiara se il target è interno o esterno.")

        # Create a label and entry for <niso:targetID>
        targetid_label = ttk.Label(self.frame_target, text="<niso:targetID>:")
        targetid_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.targetid_entry = ttk.Entry(self.frame_target)
        self.targetid_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.targetid_entry,
                "Obbligatorio e non ripetibile, identifica il nome del target, produttore o organizzazione, "
                "il numero della versione o il media.")

        # Create a label and entry for <niso:imageData>
        imagedata_label = ttk.Label(self.frame_target, text="<niso:imageData>:")
        imagedata_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.imagedata_entry = ttk.Entry(self.frame_target)
        self.imagedata_entry.grid(row=2, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.imagedata_entry,
                "Opzionale e non ripetibile, identifica il percorso dell'immagine digitale che funge da target "
                "esterno. Si usa solo se <niso:targetType> è uguale a 0 (esterno).")

        # Create a label and entry for <niso:performanceData>
        performancedata_label = ttk.Label(self.frame_target, text="<niso:performanceData>:")
        performancedata_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.performancedata_entry = ttk.Entry(self.frame_target)
        self.performancedata_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.performancedata_entry,
                "Opzionale e non ripetibile, identifica il percorso del file che contiene i dati dell'immagine "
                "performance relativa al target identificato da <niso:targetID>.")

        # Create a label and entry for <niso:profiles>
        profiles_label = ttk.Label(self.frame_target, text="<niso:profiles>:")
        profiles_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        self.profiles_entry = ttk.Entry(self.frame_target)
        self.profiles_entry.grid(row=4, column=1, pady=5, sticky=tk.EW)
        ToolTip(self.profiles_entry,
                "Opzionale e non ripetibile, identifica il percorso del file che contiene il profilo dei colori ICC o "
                "un altro profilo di gestione.")

        # Configure grid to allow column resizing
        self.frame_target.columnconfigure(1, weight=1)

    def on_checkbox_target_selection(self):
        if self.var_is_target_enabled.get() == 1:
            self.frame_target.pack(expand=True, fill=tk.BOTH)
        else:
            self.frame_target.pack_forget()
        self.container_frame.update_idletasks()
