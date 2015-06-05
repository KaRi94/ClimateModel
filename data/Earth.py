import datetime
from data.Zone import Zone
import numpy as np


class Earth():

    DATE = datetime.datetime(year=2015, month=6, day=15)
    AVERAGE_HEAT_CAPACITY = 5.3e8

    def __init__(self, division, data):
        self.radius = 6367444.7
        self.division = division
        self.initial_data = data
        self.zones = self.create_zones()

    def get_area(self, lat1, lat2):
        return 2 * np.pi * self.radius ** 2 * np.abs(np.sin(lat1 * np.pi / 180) - np.sin(lat2 * np.pi / 180))

    @classmethod
    def get_month(cls):
        return Earth.DATE.month

    def create_zones(self):
        step = 180/self.division
        zones = []
        start = -90
        while start < 90:
            zones.append(Zone(start, start+step, self.get_area(start, start+step), self.initial_data))
            start += step
        return zones