from data.SurfaceType import SurfaceType


class Zone():

    def __init__(self, start_latitude, end_latitude, surface_area, data):
        self.start_latitude = start_latitude
        self.end_latitude = end_latitude
        self.surface_area = surface_area
        self.temperature = 0
        self.surface_types = self.load_surface_types(data)

    def __repr__(self):
        return 'Lat: %s, Area: %s' % (self.latitude(), self.surface_area)

    def load_surface_types(self, data):
        surface_types = []
        for type in data.get(self.latitude(), []):
            surface_types.append(SurfaceType(type['name'], type['albedo'], type['percentage']))
        return surface_types

    def latitude(self):
        return (self.end_latitude+self.start_latitude)/2