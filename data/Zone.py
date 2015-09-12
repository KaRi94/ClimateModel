import constants
from data.Date import Date
from data.SurfaceType import SurfaceType


class Zone:
    def __init__(self, earth, start_latitude, end_latitude, surface_area, data, avg_cloud_coverage):
        self.earth = earth
        self.start_latitude = start_latitude
        self.end_latitude = end_latitude
        self.surface_area = surface_area
        self.average_cloud_coverage = avg_cloud_coverage
        self.temperature = constants.INITIAL_EARTH_TEMPERATURE

        self.surface_types = self.load_surface_types(data)

    def __repr__(self):
        return 'Lat: %s, Area: %s (%f K)' % (self.latitude(), self.surface_area, self.temperature)

    def load_surface_types(self, data):
        """
        Loads data from file and use this data for creating surface of zone
        :param data:
        :return:
        """
        surface_types = []
        for surface_type in data.get(self.latitude(), []):
            surface_types.append(SurfaceType(surface_type['name'], surface_type['albedo'], surface_type['percentage']))
        return surface_types

    def latitude(self):
        return (self.end_latitude+self.start_latitude)/2

    def calculate_temperature(self, power):
        """
        Calculates temperature change corresponding to the transmitted energy
        It also changes temperature of particular zone
        :param power:
        :return None:
        """
        self.temperature += power*Date.get_month_duration()/(constants.AVERAGE_HEAT_CAPACITY*self.surface_area)

    def get_water_surface(self):
        for surface in self.surface_types:
            if surface.name == 'Water':
                return surface
        return None

    def get_ice_surface(self):
        for surface in self.surface_types:
            if surface.name == 'Snow_and_ice':
                return surface
        return None
