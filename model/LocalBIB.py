class LocalBIB:
    def __init__(self, geo_coords=None, not_dates=None):
        self.geo_coords = geo_coords if geo_coords is not None else []
        self.not_dates = not_dates if not_dates is not None else []

    def add_geo_coord(self, geo_coord):
        self.geo_coords.append(geo_coord)

    def add_not_date(self, not_date):
        self.not_dates.append(not_date)

    def get_geo_coords(self):
        return self.geo_coords

    def set_geo_coords(self, geo_coords):
        self.geo_coords = geo_coords

    # Getter and Setter for not_dates
    def get_not_dates(self):
        return self.not_dates

    def set_not_dates(self, not_dates):
        self.not_dates = not_dates

    # Method to print geo_coords
    def print_geo_coords(self):
        ret = ''
        for coord in self.geo_coords:
            ret += str(coord) + ' - '
        return ret

    # Method to print not_dates
    def print_not_dates(self):
        ret = ''
        for date in self.not_dates:
            ret += str(date) + ' - '
        return ret
