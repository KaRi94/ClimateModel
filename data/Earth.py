import datetime

import numpy as np


class Earth():

    DATE = datetime.datetime(year=2015, month=1, day=15)

    def __init__(self):
        self.radius = 6367444.7

    def get_area(self, lat1, lat2):
        return 2 * np.pi * self.radius ** 2 * np.abs(np.sin(lat1 * np.pi / 180) - np.sin(lat2 * np.pi / 180))

    def get_month(self):
        return Earth.DATE.month