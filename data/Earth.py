import numpy as np

from data.Date import Date
from data.Zone import Zone


class Earth():
    LAYER_SIZE = 6367444.7
    AVERAGE_HEAT_CAPACITY = 5.3e8 * (1 - (1 - LAYER_SIZE / 6367444.7) ** 3)

    def __init__(self, division, surface_data, cloud_coverage):
        self.radius = 6367444.7
        self.division = division
        self.zones = self.create_zones(surface_data, cloud_coverage)
        self.total_area = self.get_area(-90, 90)
        self.DATE = Date(year=0, month=1)


    def get_area(self, lat1, lat2):
        return 2 * np.pi * self.radius ** 2 * np.abs(np.sin(lat1 * np.pi / 180) - np.sin(lat2 * np.pi / 180))

    def get_month(self):
        return self.DATE.month

    def average_temp(self):
        return sum([z.temperature * z.surface_area for z in self.zones]) / self.total_area

    def create_zones(self, surface_data, cloud_coverage):
        step = 180/self.division
        zones = []
        start = -90
        while start < 90:
            zones.append(Zone(self,
                              start, start + step,
                              self.get_area(start, start + step),
                              surface_data,
                              cloud_coverage[(start + step / 2)])
            )
            start += step
        return zones