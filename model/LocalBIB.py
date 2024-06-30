class LocalBIB:
    def __init__(self, local_bib_id, geo_coords=None, not_dates=None):
        self.local_bib_id = local_bib_id
        self.geo_coords = geo_coords if geo_coords is not None else dict()
        self.not_dates = not_dates if not_dates is not None else dict()

    def add_geo_coord(self, key, geo_coord):
        self.geo_coords[key] = geo_coord

    def add_not_date(self, key, not_date):
        self.not_dates[key] = not_date

    def to_dict(self):
        return {
            "local_bib_id": self.local_bib_id,
            "geo_coords": self.geo_coords,
            "not_dates": self.not_dates
        }

    def __str__(self):
        return f"LocalBIB(id={self.local_bib_id}, geo_coords={self.geo_coords}, not_dates={self.not_dates})"

