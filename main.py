import time

import matplotlib.pyplot as plt
import numpy as np

from data.Data import Data
from data.Earth import *
from data.Radiation import *
from data.SurfaceType import *
from data.Zone import *


# rzeczy do wykresu
plt.rcParams['font.size'] = 18
plt.ion()
x = [0]
y = np.arange(-90 + 7.5, 90, 15)


data = Data('data.csv')
cloud_cover = Data('zachmurzenie.csv')
data.load_zone_data()
cloud_cover.load_zone_cloud_coverage()
print(cloud_cover.get_data())

earth = Earth(12, data.get_data(), cloud_cover.get_data())
until = Date(year=3000, month=1)
temp = False
temperatures = []
while earth.DATE < until:
    # print('-----------------%s---------------------' % earth.DATE)
    if until - earth.DATE <= Date(year=1, month=1):
        temp = True
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        print(earth.average_temp())
        if temp:
            temperatures.append(zone.temperature)

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
        time.sleep(2)
        del temperatures[:]
    earth.DATE.step()


# calculate absorbed energy (radiation) for every zone -> temperature
# zone temperature -> calculate emitted energy (radiation) for every zone
# zones temperature -> energy flow between two adjacent zone
# calculate albedo changes (albedo<->temperature) ocean<->ice
