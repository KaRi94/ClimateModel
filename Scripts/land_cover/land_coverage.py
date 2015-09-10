import re
import sys
import os

import numpy as np


def get_area(lat1, lat2, radius):
    return 2 * np.pi * radius ** 2 * np.abs(np.sin(lat1 * np.pi / 180) - np.sin(lat2 * np.pi / 180))


zone_size = 15.0

# TODO import data from file
with open('global_2012_hd.asc', 'r') as plik:
    nrows = int(re.search(r'\d+', str(plik.readline())).group())
    ncol = int(re.search(r'\d+', str(plik.readline())).group())
    xllcorner = float(re.findall(r"[-+]?\d*\.\d+|\d+", str(plik.readline()))[0])
    yllcorner = float(re.findall(r"[-+]?\d*\.\d+|\d+", str(plik.readline()))[0])
    cellsize = float(re.findall(r"\d*\.\d+|\d+", str(plik.readline()))[0])
    x = [int(liczba) for liczba in plik.readlines()[1].split()]

pk = open('land_coverage_type.csv', 'w')

number_of_y = int(360 / cellsize)
step = 0.02
h2o = 0

# TODO Antarctica (ice and snow) -90.0 to -83.0
for i in range(-900, -830, int(cellsize * 10)):
    temp = ""
    temp += str(i / 10)
    for j in range(0, 15):
        temp += " " + str(0.0)
    temp += " " + str(1.0)
    temp += " " + str(0.0)
    pk.write(temp + "\n")

# TODO Antarctica with Ocean from -83.0 to -64.0
for i in range(-830, -640, int(cellsize * 10)):
    temp = ""
    temp += str(i / 10)
    temp += " " + str(h2o)
    for j in range(1, 15):
        temp += " " + str(0.0)
    temp += " " + str(1.0 - h2o)
    temp += " " + str(0.0)
    h2o += step
    pk.write(temp + "\n")

# TODO data from GLCF database -64.0 to 84.0
for i in range(0, len(x), number_of_y):
    temp = ""
    temp += str(yllcorner)
    for j in range(0, 17):
        temp += " " + str(x[i:i + number_of_y].count(j) / number_of_y)
    pk.write(temp + "\n")
    yllcorner += cellsize

h2o = 1.0
step = 0.03

# TODO North Pole 84.0 to 90.0
for i in range(840, 900, int(cellsize * 10)):
    temp = ""
    temp += str(i / 10)
    temp += " " + str(h2o)
    for j in range(1, 15):
        temp += " " + str(0.0)
    temp += " " + str(1.0 - h2o)
    temp += " " + str(0.0)
    h2o -= step
    pk.write(temp + "\n")
    
pk.close()

try:
    if (int(10 * zone_size) % int(10 * cellsize) is not 0) or (90 % int(zone_size) is not 0):
        raise Exception()
except Exception as e:
    print('Wrong zone width\n')
    sys.exit()
x = np.loadtxt('land_coverage_type.csv')
os.remove('land_coverage_type.csv')
radius = 6367444.7
f_handle = open('land_coverage_type.csv', 'ab')
earth_area = get_area(-90, 90, radius)
for i in range(-90, 90, int(zone_size)):
    zone_area = get_area(i, i + int(zone_size), radius)
    l = np.zeros(x[2 * i + 180].size)
    for j in range(10 * i, 10 * (i + int(zone_size)), int(cellsize * 10)):
        k = get_area(x[(2 * j) // 10 + 180][0], x[(2 * j) // 10 + 180][0] + cellsize, radius) / zone_area
        l += k * x[(2 * j) // 10 + 180]
    l[0] = (i + zone_size / 2)
    np.savetxt(f_handle, l, fmt='%.7e', delimiter=',', newline=',', header='\n', comments='')
f_handle.close()
