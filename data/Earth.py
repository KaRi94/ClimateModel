import datetime
from data.Zone import Zone


class Earth():

    DATE = datetime.datetime(year=2015, month=1, day=15)

    def __init__(self, division):
        self.radius = 6371
        self.division = division
        self.zones = self.create_zones()

    def get_area(self, lat1, lat2):
        pass

    def get_month(self):
        return Earth.DATE.month

    def create_zones(self):
        step = 180/self.division
        zones = []
        start = -90
        while start < 90:
            zones.append(Zone(start, start+step, self.get_area(start, start+step)))
            start += step
        return zones