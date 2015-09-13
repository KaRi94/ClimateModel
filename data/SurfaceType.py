class SurfaceType:
    SURFACE_TYPES = {
        'Water': 0.06,
        'Evergreen_Needleleaf_forest': 0.13,
        'Evergreen_Broadleaf_forest': 0.13,
        'Deciduous_Needleleaf_forest': 0.165,
        'Deciduous_Broadleaf_forest': 0.165,
        'Mixed_forest': 0.15,
        'Closed_shrublands': 0.19,
        'Open_shrublands': 0.19,
        'Woody_savannas': 0.13,
        'Savannas': 0.14,
        'Grasslands': 0.3,
        'Permanent_wetlands': 0.2,
        'Croplands': 0.3,
        'Urban_and_built-up': 0.2,
        'Cropland/Natural_vegetation_mosaic': 0.16,
        'Snow_and_ice': 0.8,
        'Barren_or_sparsely_vegetated': 0.3,
    }

    def __init__(self, name, albedo, percentage):
        self.name = name
        self.albedo = albedo
        self.percentage = percentage

    def __repr__(self):
        return '%s: (%s%%) (%s)' % (self.name, self.percentage, self.albedo)