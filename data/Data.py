import csv
from data.SurfaceType import SurfaceType


class Data:

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = {}

    def load_zone_data(self):
        with open(self.file_name, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            for row in list(rows)[1:]:
                if not self.data.get(float(row[0])):
                    self.data[float(row[0])] = []
                self.data[float(row[0])].append({
                    'name': row[1],
                    'albedo': float(row[2]),
                    'percentage': float(row[3]),
                })

    def load_complex_zone_data(self):
        with open(self.file_name, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            rows = list(rows)
            surfaces = rows[0][1:]
            for row in list(rows)[1:]:
                if not self.data.get(float(row[0])):
                    self.data[float(row[0])] = []
                for i in range(1, len(row)-1):
                    self.data[float(row[0])].append({
                        'name': surfaces[i-1],
                        'albedo': float(SurfaceType.SURFACE_TYPES.get(surfaces[i-1], 0)),
                        'percentage': float(row[i])*100,
                    })

    def load_zone_cloud_coverage(self):
        with open(self.file_name, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            for row in list(rows)[1:]:
                self.data[float(row[0])] = {
                    'average': row[1],
                    'rms': float(row[2]),
                }

    def load_insolation_data(self):
        with open(self.file_name, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=' ')
            for row in list(rows)[2:]:
                if not self.data.get(float(row[0])):
                    self.data[float(row[0])] = []
                self.data[float(row[0])] = [float(x) for x in row[1:-1]]
            l = sorted([(key, value) for key, value in self.data.items()], key=lambda x: x[0])
            self.data = {}
            for i in range(len(l)-1):
                self.data[(l[i][0]+l[i+1][0])/2] = [(x+y)/2 for x, y in zip(l[i][1], l[i+1][1])]
                i += 2

    def get_data(self):
        return self.data