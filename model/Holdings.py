class Holdings:
    def __init__(self, holdings_id, library, inventory_number, shelfmarks):
        self.holdings_id = holdings_id
        self.library = library
        self.inventory_number = inventory_number
        self.shelfmarks = shelfmarks

    def get_holdings_id(self):
        return self.holdings_id

    def set_holdings_id(self, holding_id):
        self.holdings_id = holding_id

    def get_library(self):
        return self.library

    def set_library(self, library):
        self.library = library

    def get_inventory_number(self):
        return self.inventory_number

    def set_inventory_number(self, inventory_number):
        self.inventory_number = inventory_number

    def get_shelfmarks(self):
        return self.shelfmarks

    def set_shelfmarks(self, shelfmarks):
        self.shelfmarks = shelfmarks

    def add_shelfmark(self, shelfmark):
        self.shelfmarks.append(shelfmark)

    def get_string_shelfmarks(self):
        shelfmarks_str = ''
        for shelfmark in self.shelfmarks:
            shelfmarks_str += (str(shelfmark) + " - ")
        return shelfmarks_str

    def __str__(self):
        return f"Holding(ID: {self.holdings_id}, Library: {self.library}, Inventory Number: {self.inventory_number}, Shelfmarks: [{self.get_string_shelfmarks()}])"


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
        return f"(Value: {self.value}, Type: {self.type})"
