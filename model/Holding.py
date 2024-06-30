class Holding:
    def __init__(self, holding_id, library, inventory_number, shelfmark_values):
        self.holding_id = holding_id
        self.library = library
        self.inventory_number = inventory_number
        self.shelfmark_values = shelfmark_values

    def get_holding_id(self):
        return self.holding_id

    def set_holding_id(self, holding_id):
        self.holding_id = holding_id

    def get_library(self):
        return self.library

    def set_library(self, library):
        self.library = library

    def get_inventory_number(self):
        return self.inventory_number

    def set_inventory_number(self, inventory_number):
        self.inventory_number = inventory_number

    def get_shelfmark_values(self):
        return self.shelfmark_values

    def set_shelfmark_values(self, shelfmark_values):
        self.shelfmark_values = shelfmark_values

    def __str__(self):
        shelfmarks_str = ", ".join(str(shelfmark) for shelfmark in self.shelfmark_values)
        return f"Holding(ID: {self.holding_id}, Library: {self.library}, Inventory Number: {self.inventory_number}, Shelfmarks: [{shelfmarks_str}])"


class Shelfmark:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def __str__(self):
        return f"Shelfmark(Value: {self.value}, Type: {self.type})"
