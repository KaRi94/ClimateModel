from data.SurfaceType import SurfaceType


class Zone():

    def __init__(self, earth, start_latitude, end_latitude, surface_area, data):
        self.earth = earth
        self.start_latitude = start_latitude
        self.end_latitude = end_latitude
        self.surface_area = surface_area
        self.temperature = 0
        self.surface_types = self.load_surface_types(data)

    def __repr__(self):
        return 'Lat: %s, Area: %s (%f K)' % (self.latitude(), self.surface_area, self.temperature)

    def load_surface_types(self, data):
        surface_types = []
        for surface_type in data.get(self.latitude(), []):
            surface_types.append(SurfaceType(surface_type['name'], surface_type['albedo'], surface_type['percentage']))
        return surface_types

    def latitude(self):
        return (self.end_latitude+self.start_latitude)/2

    def calculate_temperature(self, energy):
        from data.Earth import Earth
        self.temperature += energy/(Earth.AVERAGE_HEAT_CAPACITY*self.surface_area)