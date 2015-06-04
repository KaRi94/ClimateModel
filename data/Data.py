import csv


class Data():

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = {}
        self.load_data()

    def load_data(self):
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

    def get_data(self):
        return self.data