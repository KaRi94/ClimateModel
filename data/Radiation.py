import numpy as np

import constants
from data.Data import Data


class Radiation:
    data = Data('data/initial_model_data/insolation.csv')
    data.load_insolation_data()
    MONTHLY_INSOLATION = data.get_data()

    @classmethod
    def get_incoming_radiation(cls, zone):
        """
        Calculates incoming radiation on particular zone
        It takes into account radiation reflected from the atmosphere and clouds
        :param zone:
        :return float: insolation of particular zone:
        """
        insolation = Radiation.MONTHLY_INSOLATION[zone.latitude()][zone.earth.get_month()-1]*constants.SOLAR_CONSTANT/1367

        insolation -= insolation * ( constants.CLOUD_ALBEDO * np.random.normal(
            zone.average_cloud_coverage['average'], zone.average_cloud_coverage['rms']))
        insolation -= insolation * constants.ATMOSPHERE_REFLECTED_COEFFICIENT
        return insolation

    @classmethod
    def calculate_absorbed_radiation(cls, zone):
        """
        Calculates absorbed radiation on particular zone
        Firstly method calculate incoming radiation and next it determines how much radiation is being absorbed
        based on zone content
        :param zone:
        :return absorbed radiation:
        """
        radiation = Radiation.get_incoming_radiation(zone)
        absorbed_radiation = sum([zone.surface_area*surface.percentage/100*radiation*(1-surface.albedo) for surface in zone.surface_types])
        return absorbed_radiation

    # TODO wpływ zachmurzenia na emisje promieniowania podczerwonego (narazie zaniedbujemy)
    @classmethod
    def calculate_emmited_radiation(cls, zone):
        """
        Calculates how much radiation is being emmited
        It uses Stefan-Boltzmann law and also take into consideration green house effect
        :param zone:
        :return emmited radiation:
        """
        return -(1 - constants.GREEN_HOUSE_EFFECT_COEFFICIENT) * \
               constants.STEFAN_BOLTZMAN_CONSTANT * \
               zone.surface_area * \
               zone.temperature **4
