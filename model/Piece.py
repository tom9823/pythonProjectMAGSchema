class Piece:
    def __init__(self, year=None, issue=None, stpiece_per=None, part_number=None, part_name=None, stpiece_vol=None, is_pubblicazioni_seriali=True):
        self._year = year
        self._issue = issue
        self._stpiece_per = stpiece_per
        self._part_number = part_number
        self._part_name = part_name
        self._stpiece_vol = stpiece_vol
        self._is_pubblicazioni_seriali = is_pubblicazioni_seriali

    def get_year(self):
        return self._year

    def set_year(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("year deve essere di tipo string o None")
        self._year = value

    def get_issue(self):
        return self._issue

    def set_issue(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("issue deve essere di tipo string o None")
        self._issue = value

    def get_stpiece_per(self):
        return self._stpiece_per

    def set_stpiece_per(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("stpiece_per deve essere di tipo string o None")
        self._stpiece_per = value

    def get_part_number(self):
        return self._part_number

    def set_part_number(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("part_number deve essere di tipo string o None")
        self._part_number = value

    def get_part_name(self):
        return self._part_name

    def set_part_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("part_name deve essere di tipo string o None")
        self._part_name = value

    def get_stpiece_vol(self):
        return self._stpiece_vol

    def set_stpiece_vol(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("stpiece_vol deve essere di tipo string o None")
        self._stpiece_vol = value

    def get_is_pubblicazioni_seriali(self):
        return self._is_pubblicazioni_seriali

    def set_is_pubblicazioni_seriali(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_pubblicazioni_seriali deve essere di tipo bool")
        self._is_pubblicazioni_seriali = value

    def __str__(self):
        return (
            f"Piece("
            f"year={self.get_year()}, "
            f"issue={self.get_issue()}, "
            f"stpiece_per={self.get_stpiece_per()}, "
            f"part_number={self.get_part_number()}, "
            f"part_name={self.get_part_name()}, "
            f"stpiece_vol={self.get_stpiece_vol()}, "
            f"is_pubblicazioni_seriali={self.get_is_pubblicazioni_seriali()})"
        )
