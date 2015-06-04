class SurfaceType():

    def __init__(self, name, albedo, percentage):
        self.name = name
        self.albedo = albedo
        self.percentage = percentage

    def __repr__(self):
        return '%s: (%s%%) (%s)' % (self.name, self.percentage, self.albedo)