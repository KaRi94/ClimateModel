import numpy as np
import constants

from data.Date import Date
from data.Zone import Zone


class Earth:
    def __init__(self, division, surface_data, cloud_coverage):
        self.radius = constants.EARTH_RADIUS
        self.division = division
        self.zones = self.create_zones(surface_data, cloud_coverage)
        self.total_area = self.get_area(-90, 90)
        self.DATE = Date(year=0, month=1)

    def get_circumference(self, lat):
        return self.radius * np.cos(lat * np.pi / 180)

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
        """
        Calculates energy flow between all zones
        Method iterates over all zones and using knowledge about thermal conductivity of earth calculates
        energy flow between each zone
        :return None:
        """
        for i in range(1, len(self.zones)-1):
            bottom_zone = self.zones[i-1]
            middle_zone = self.zones[i]
            top_zone = self.zones[i+1]

            delta_temp = bottom_zone.temperature - middle_zone.temperature
            delta_power = constants.THERMAL_CONDUCTIVITY * self.get_circumference(middle_zone.start_latitude) * delta_temp

            middle_zone.calculate_temperature(delta_power)
            bottom_zone.calculate_temperature(-delta_power)

            delta_temp = top_zone.temperature - middle_zone.temperature
            delta_power = constants.THERMAL_CONDUCTIVITY * self.get_circumference(middle_zone.end_latitude) * delta_temp

            middle_zone.calculate_temperature(delta_power)
            top_zone.calculate_temperature(-delta_power)

    def calculate_albedo_changes_due_to_water_phase_transitions(self):
        """
        Calculates how much albedo has changed when the temperature dropped below zero
        It take into consideration only transition between water and ice and vice versa
        :return None:
        """
        for zone in self.zones:
            calculated = False
            if zone.temperature > constants.MELTING_POINT:
                ice = zone.get_ice_surface()
                if ice and ice.percentage:
                    water = zone.get_water_surface()
                    delta_percentage = constants.WATER_LATENT_HEAT_PERCENTAGE_COEFFICIENT / zone.surface_area
                    water.percentage += delta_percentage
                    ice.percentage -= delta_percentage
                    calculated = True
            else:
                water = zone.get_water_surface()
                if water and water.percentage:
                    ice = zone.get_ice_surface()
                    delta_percentage = constants.WATER_LATENT_HEAT_PERCENTAGE_COEFFICIENT / zone.surface_area
                    water.percentage -= delta_percentage
                    ice.percentage += delta_percentage
                    calculated = True

            if calculated:
                if water.percentage < 0.0:
                    water.percentage = 0.0
                if water.percentage > 100.0:
                    water.percentage = 100.0
                if ice.percentage < 0.0:
                    ice.percentage = 0.0
                if ice.percentage > 100.0:
                    ice.percentage = 100.0

