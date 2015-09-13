import os
import time

import matplotlib.pyplot as plt
import numpy as np

from data.Earth import *
from data.Radiation import *
from data.Zone import *


# LOADING DATA FROM FILES
print('LOADING DATA FROM FILES...')
os.system("python3 Scripts/land_cover/land_coverage.py")
os.system("python3 Scripts/cloudiness/cloudiness.py")

# MODEL INITIALIZATION
print('MODEL INITIALIZATION...')
complex_data = Data('data/initial_model_data/land_coverage_type.csv')
cloud_cover = Data('data/initial_model_data/cloudiness.csv')
complex_data.load_complex_zone_data()
cloud_cover.load_zone_cloud_coverage()

# BUILDING STRUCTURE OF THE EARTH
print('BUILDING STRUCTURE OF THE EARTH...')
earth = Earth(12, complex_data.get_data(), cloud_cover.get_data())


# rzeczy do wykresu
plt.rcParams['font.size'] = 18
plt.ion()
x = [0]
y = np.arange(-90 + 7.5, 90, 15)
average_temp = []


# STARTING SIMULATION
print('STARTING SIMULATION...')
until = Date(year=constants.END_YEAR, month=1)
temp = False
temperatures = []
while earth.DATE < until:
    # print('-----------------%s---------------------' % earth.DATE)
    if until - earth.DATE <= Date(year=1, month=1):
        temp = True
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        earth.calculate_energy_flow_between_zones()
        earth.calculate_albedo_changes_due_to_water_phase_transitions()
        if temp:
            temperatures.append(zone.temperature)
    average_temp.append(earth.average_temp())

        #    rysuje interatywny wykres ostatniego roku
    if temp:
        linia, = plt.plot([], [], 'ob', ms=10)
        x = np.array(temperatures)
        print(x)
        linia.set_xdata(x)
        linia.set_ydata(y)
        plt.title(earth.DATE)
        plt.axis([np.min(x) * 1.05, np.max(x) * 1.05, -90, 90])
        plt.draw()  # ponowne rysowanie
        time.sleep(1)
        del temperatures[:]
    earth.DATE.step()
# print(average_temp[-1])
# years=np.arange(0, len(np.array(average_temp))/12, 1/12)
# plt.plot(years , np.array(average_temp), 'k-', lw=2)
# plt.show()
