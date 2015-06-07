import datetime

import numpy as np

from data.Zone import Zone


class Earth():
    AVERAGE_HEAT_CAPACITY = 5.3e8 * (1 - (1 - 100 / 6367444.7) ** 3)

    def __init__(self, division, data):
        self.radius = 6367444.7
        self.division = division
        self.initial_data = data
        self.zones = self.create_zones()
        self.total_area = self.get_area(-90, 90)
        self.DATE = datetime.datetime(year=2015, month=6, day=15)


    def get_area(self, lat1, lat2):
        return 2 * np.pi * self.radius ** 2 * np.abs(np.sin(lat1 * np.pi / 180) - np.sin(lat2 * np.pi / 180))

    def get_month(self):
        return self.DATE.month

    def average_temp(self):
        return sum([z.temperature * z.surface_area for z in self.zones]) / self.total_area

    def create_zones(self):
        step = 180/self.division
        zones = []
        start = -90
        while start < 90:
            zones.append(Zone(self, start, start+step, self.get_area(start, start+step), self.initial_data))
            start += step
        return zones