import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET


class XMLTreeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XML Tree Editor")
        self.geometry("800x600")

        # Setup the Treeview widget
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)

        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x")

        # Buttons to open/save XML and modify nodes
        open_button = tk.Button(button_frame, text="Open XML", command=self.open_xml)
        open_button.pack(side="left", padx=5, pady=5)

        save_button = tk.Button(button_frame, text="Save XML", command=self.save_xml)
        save_button.pack(side="left", padx=5, pady=5)

        edit_button = tk.Button(button_frame, text="Edit Selected", command=self.edit_selected)
        edit_button.pack(side="left", padx=5, pady=5)

        self.xml_tree = None
        self.xml_file_path = None

    def open_xml(self):
        """Open an XML file and display it in the Treeview"""
        self.xml_file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not self.xml_file_path:
            return

        self.xml_tree = ET.parse(self.xml_file_path)
        root = self.xml_tree.getroot()

        # Clear the treeview first
        self.tree.delete(*self.tree.get_children())

        # Populate the Treeview with XML elements
        self.build_tree(self.tree, root)

    def build_tree(self, parent, element, parent_id=""):
        """Recursively build the tree for the Treeview"""
        # Insert element into the tree
        node_id = self.tree.insert(parent_id, "end", text=element.tag, values=[element.text])

        # Add attributes of the element as children nodes
        for key, value in element.attrib.items():
            self.tree.insert(node_id, "end", text=f"@{key}", values=[value])

        # Recursively process child elements
        for child in element:
            self.build_tree(node_id, child)

    def edit_selected(self):
        """Edit the selected node in the Treeview"""
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("No selection", "Please select an item to edit.")
            return

        # Get selected node
        node = self.tree.item(selected_item[0])
        node_text = node["text"]
        node_value = node["values"][0] if node["values"] else ""

        # Open a dialog to edit the element or attribute
        editor_window = tk.Toplevel(self)
        editor_window.title("Edit XML Node")

        # Labels and entry fields
        tk.Label(editor_window, text="Element/Attribute:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(editor_window)
        name_entry.insert(0, node_text)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(editor_window, text="Value:").grid(row=1, column=0, padx=10, pady=10)
        value_entry = tk.Entry(editor_window)
        value_entry.insert(0, node_value)
        value_entry.grid(row=1, column=1, padx=10, pady=10)

        # Save button
        def save_edit():
            new_name = name_entry.get()
            new_value = value_entry.get()

            if node_text.startswith("@"):
                # Attribute modification
                parent_item = self.tree.parent(selected_item[0])
                parent_node = self.tree.item(parent_item)
                parent_element = self.find_element_by_tag(self.xml_tree.getroot(), parent_node['text'])
                if parent_element is not None:
                    attr_name = node_text[1:]
                    parent_element.attrib[attr_name] = new_value
            else:
                # Element text modification
                element = self.find_element_by_tag(self.xml_tree.getroot(), node_text)
                if element is not None:
                    element.text = new_value

            # Update treeview display
            self.tree.item(selected_item[0], text=new_name, values=[new_value])
            editor_window.destroy()

        tk.Button(editor_window, text="Save", command=save_edit).grid(row=2, column=0, columnspan=2, pady=10)

    def find_element_by_tag(self, root, tag):
        """Find element by tag in the XML tree"""
        for elem in root.iter():
            if elem.tag == tag:
                return elem
        return None

    def save_xml(self):
        """Save the modified XML back to a file"""
        if self.xml_tree is None:
            messagebox.showwarning("No XML loaded", "Please load an XML file first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if save_path:
            self.xml_tree.write(save_path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Save Successful", f"XML saved to {save_path}")


if __name__ == "__main__":
    app = XMLTreeEditor()
    app.mainloop()
