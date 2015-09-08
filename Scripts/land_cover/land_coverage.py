import re

with open('land_cover/global_2012_hd.asc', 'r') as plik:
    nrows = int(re.search(r'\d+', str(plik.readline())).group())
    ncol = int(re.search(r'\d+', str(plik.readline())).group())
    xllcorner = float(re.findall(r"[-+]?\d*\.\d+|\d+", str(plik.readline()))[0])
    yllcorner = float(re.findall(r"[-+]?\d*\.\d+|\d+", str(plik.readline()))[0])
    cellsize = float(re.findall(r"\d*\.\d+|\d+", str(plik.readline()))[0])
    x = [int(liczba) for liczba in plik.readlines()[1].split()]

pk = open('land_cover/land_coverage_type.csv', 'w')
number_of_y = int(360 / cellsize)

for i in range(0, len(x), number_of_y):
    tekst = ""
    tekst += str(yllcorner)
    for j in range(0, 17):
        tekst += " " + str(x[i:i + number_of_y].count(j) / number_of_y)
    pk.write(tekst + "\n")
    yllcorner += cellsize
pk.close()
