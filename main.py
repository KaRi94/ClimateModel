import time

from dateutil.relativedelta import relativedelta
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
linia, = plt.plot([], [], 'ob', ms=10)

data = Data('data.csv')
data.load_zone_data()
earth = Earth(12, data.get_data())
until = datetime.datetime(year=5000, month=1, day=15)

temp = False
while earth.DATE < until:
    # print('-----------------%s---------------------' % earth.DATE)
    temperatury = []
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        print(zone)
        temperatury.append(zone.temperature)

        #    rysuje interatywny wykres ostatniego roku
    if until - earth.DATE <= datetime.timedelta(370) or temp:
        x = np.array(temperatury)
        print(x)
        linia.set_xdata(x)
        linia.set_ydata(y)
        plt.title(earth.DATE)
        plt.axis([np.min(x) * 1.05, np.max(x) * 1.05, -90, 90])
        plt.draw()  # ponowne rysowanie
        time.sleep(2)
        temp = True
    del temperatury[:]
    earth.DATE += relativedelta(months=1)


# calculate absorbed energy (radiation) for every zone -> temperature
# zone temperature -> calculate emitted energy (radiation) for every zone
# zones temperature -> energy flow between two adjacent zone
# calculate albedo changes (albedo<->temperature) ocean<->ice
