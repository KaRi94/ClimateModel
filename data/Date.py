class Date:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month > other.month:
                return True
        return False

    def __ge__(self, other):
        if self.year > other.year:
            return True
        elif self.year == other.year:
            if self.month >= other.month:
                return True
        return False

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
        return False

    def __le__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month <= other.month:
                return True
        return False

    def __add__(self, other):
        month = self.month + other.month
        year = self.year + other.year
        if month > 12:
            month -= 12
            year += 1
        return Date(year=year, month=month)

    def __sub__(self, other):
        if self.month > other.month:
            year = self.year - other.year
            month = self.month - other.month
        else:
            year = self.year - other.year - 1
            month = 12 + self.month - other.month
        return Date(year=year, month=month)

    def __repr__(self):
        return 'Year: %s Month: %s' % (self.year, self.month)

    def get_month(self):
        return self.month

    def step(self):
        self.month += 1
        if self.month == 13:
            self.year += 1
            self.month = 1

    @classmethod
    def get_month_duration(cls):
        # statystyczna dlugość miesiąca w sekundach
        return 2629743.8235498336