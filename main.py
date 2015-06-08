import matplotlib.pyplot as plt
import numpy as np
from data.Data import Data
from data.Earth import *
from data.Radiation import *
from data.SurfaceType import *
from data.Zone import *


# rzeczy do wykresu
plt.rcParams['font.size'] = 18
# plt.ion()
x = [0]
y = np.arange(-90 + 7.5, 90, 15)
average_temp = []

data = Data('surface_data.csv')
cloud_cover = Data('zachmurzenie.csv')
data.load_zone_data()
cloud_cover.load_zone_cloud_coverage()

earth = Earth(12, data.get_data(), cloud_cover.get_data())
until = Date(year=1000, month=1)
temp = False
temperatures = []
while earth.DATE < until:
    # print('-----------------%s---------------------' % earth.DATE)
    if until - earth.DATE <= Date(year=1, month=1):
        temp = True
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        if temp:
            temperatures.append(zone.temperature)
        average_temp.append(earth.average_temp())

        #    rysuje interatywny wykres ostatniego roku
    if temp:
        # linia, = plt.plot([], [], 'ob', ms=10)
        # x = np.array(temperatures)
        # print(x)
        # linia.set_xdata(x)
        # linia.set_ydata(y)
        # plt.title(earth.DATE)
        # plt.axis([np.min(x) * 1.05, np.max(x) * 1.05, -90, 90])
        # plt.draw()  # ponowne rysowanie
        # time.sleep(0.5)
        del temperatures[:]
    earth.DATE.step()
print(len(np.array(average_temp)))
plt.plot((np.arange(0, len(np.array(average_temp)), 1) / 12), np.array(average_temp), 'k-', lw=2)
plt.show()


# TODO: calculate albedo changes (albedo<->temperature) ocean<->ice
# TODO: zones temperature -> energy flow between two adjacent zone
