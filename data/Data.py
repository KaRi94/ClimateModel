import csv


class Data():

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