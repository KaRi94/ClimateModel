class Zone():

    def __init__(self, start_latitude, end_latitude, surface_area):
        self.start_latitude = start_latitude
        self.end_latitude = end_latitude
        self.surface_area = surface_area
        self.temperature = 0
        self.surface_types = []

    def latitude(self):
        return (self.end_latitude+self.start_latitude)/2