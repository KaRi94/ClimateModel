import numpy as np

from data.Date import Date
from data.Zone import Zone


class Earth():
    EARTH_RADIUS = 6364000
    LAYER_SIZE = 6367444.7
    AVERAGE_HEAT_CAPACITY = 5.3e8 * (1 - (1 - LAYER_SIZE / 6367444.7) ** 3)
    THERMAL_CONDUCTIVITY = 1e8
    WATER_LATENT_HEAT_PERCENTAGE_COEFFICIENT = 334000 * 100
    MELTING_POINT = 273.13
    INITIAL_EARTH_TEMPERATURE = 0

    def __init__(self, division, surface_data, cloud_coverage):
        self.radius = 6367444.7
        self.division = division
        self.zones = self.create_zones(surface_data, cloud_coverage)
        self.total_area = self.get_area(-90, 90)
        self.DATE = Date(year=0, month=1)

    def get_circumference(self, lat):
        return Earth.EARTH_RADIUS * np.cos(lat * np.pi / 180)

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

    def calculate_energy_flow_between_zones(self):
        for i in range(1, len(self.zones)-1):
            bottom_zone = self.zones[i-1]
            middle_zone = self.zones[i]
            top_zone = self.zones[i+1]

            delta_temp = bottom_zone.temperature - middle_zone.temperature
            delta_power = Earth.THERMAL_CONDUCTIVITY * self.get_circumference(middle_zone.start_latitude) * delta_temp

            middle_zone.calculate_temperature(delta_power)
            bottom_zone.calculate_temperature(-delta_power)

            delta_temp = top_zone.temperature - middle_zone.temperature
            delta_power = Earth.THERMAL_CONDUCTIVITY * self.get_circumference(middle_zone.end_latitude) * delta_temp

            middle_zone.calculate_temperature(delta_power)
            top_zone.calculate_temperature(-delta_power)

    def calculate_albedo_changes_due_to_water_phase_transitions(self):
        for zone in self.zones:
            if zone.temperature > Earth.MELTING_POINT:
                ice = zone.get_ice_surface()
                if ice and ice.percentage:
                    water = zone.get_water_surface()
                    delta_percentage = Earth.WATER_LATENT_HEAT_PERCENTAGE_COEFFICIENT / zone.surface_area
                    water.percentage += delta_percentage
                    ice.percentage -= delta_percentage
            else:
                water = zone.get_water_surface()
                if water and water.percentage:
                    ice = zone.get_ice_surface()
                    delta_percentage = Earth.WATER_LATENT_HEAT_PERCENTAGE_COEFFICIENT / zone.surface_area
                    water.percentage -= delta_percentage
                    ice.percentage += delta_percentage

            if water.percentage < 0.0:
                water.percentage = 0.0
            if water.percentage > 100.0:
                water.percentage = 100.0
            if ice.percentage < 0.0:
                ice.percentage = 0.0
            if ice.percentage > 100.0:
                ice.percentage = 100.0

