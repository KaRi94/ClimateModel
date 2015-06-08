import numpy as np
from data.Data import Data


class Radiation():

    SOLAR_CONSTANT = 1367
    ATMOSPHERE_REFLECTED_COEFFICIENT = 0.0  # zwiazwiane z gazami atmosfery ale nie z zachmurzeniem
    GREEN_HOUSE_EFFECT_COEFFICIENT = 0.4
    STEFAN_BOLTZMAN_CONSTANT = 5.670e-8
    CLOUD_ALBEDO = 0.10
    data = Data('insolation.csv')
    data.load_insolation_data()
    MONTHLY_INSOLATION = data.get_data()

    @classmethod
    def get_incoming_radiation(cls, zone):
        insolation = Radiation.MONTHLY_INSOLATION[zone.latitude()][zone.earth.get_month()-1]

        insolation -= insolation * (Radiation.CLOUD_ALBEDO * np.random.normal(
            zone.average_cloud_coverage['average'], zone.average_cloud_coverage['rms']))
        insolation -= insolation * Radiation.ATMOSPHERE_REFLECTED_COEFFICIENT
        return insolation

    @classmethod
    def calculate_absorbed_radiation(cls, zone):
        radiation = Radiation.get_incoming_radiation(zone)
        absorbed_radiation = sum([zone.surface_area*surface.percentage/100*radiation*(1-surface.albedo) for surface in zone.surface_types])/len(zone.surface_types)
        return absorbed_radiation

    # TODO wpływ zachmurzenia na emisje promieniowania podczerwonego (narazie zaniedbujemy)
    @classmethod
    def calculate_emmited_radiation(cls, zone):
        return -(1 - Radiation.GREEN_HOUSE_EFFECT_COEFFICIENT) * \
               Radiation.STEFAN_BOLTZMAN_CONSTANT * \
               zone.surface_area * \
               zone.temperature **4
