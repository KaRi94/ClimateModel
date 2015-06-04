import datetime

class Earth():

    DATE = datetime.datetime(year=2015, month=1, day=15)

    def __init__(self):
        self.radius = 6371

    def get_area(self, lat1, lat2):
        pass

    def get_month(self):
        return Earth.DATE.month