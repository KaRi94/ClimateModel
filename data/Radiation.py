from data.Data import Data


class Radiation():

    SOLAR_CONSTANT = 1367
    ATMOSPHERE_EMITTED_COEFFICIENT = 0.1
    STEFAN_BOLTZMAN_CONSTANT = 5.670e-8

    data = Data('insolation.csv')
    data.load_insolation_data()
    MONTHLY_INSOLATION = data.get_data()

    @classmethod
    def get_incoming_radiation(cls, zone):
        from data.Earth import Earth
        insolation = Radiation.MONTHLY_INSOLATION[zone.latitude()][Earth.get_month()-1]
        insolation -= insolation*Radiation.ATMOSPHERE_EMITTED_COEFFICIENT
        # TODO read cloud reflectivity from CSV - narazie jeblem 0.1
        insolation -= insolation*0.1
        return insolation

    @classmethod
    def calculate_absorbed_radiation(cls, zone):
        radiation = Radiation.get_incoming_radiation(zone)
        absorbed_radiation = sum([zone.surface_area*surface.percentage/100*radiation*(1-surface.albedo) for surface in zone.surface_types])/len(zone.surface_types)
        return absorbed_radiation

    @classmethod
    def calculate_emmited_radiation(cls, zone):
        return -Radiation.STEFAN_BOLTZMAN_CONSTANT*zone.temperature**4