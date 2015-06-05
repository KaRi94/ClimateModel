from data.Data import Data
from data.Earth import *
from data.Radiation import *
from data.SurfaceType import *
from data.Zone import *
from dateutil.relativedelta import relativedelta

data = Data('data.csv')
data.load_zone_data()
earth = Earth(12, data.get_data())
until = datetime.datetime(year=3100, month=1, day=15)

while earth.DATE < until:
    print('-----------------%s---------------------' % earth.DATE)
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        print(zone)
    earth.DATE += relativedelta(months=1)

# calculate absorbed energy (radiation) for every zone -> temperature
# zone temperature -> calculate emitted energy (radiation) for every zone
# zones temperature -> energy flow between two adjacent zone
# calculate albedo changes (albedo<->temperature) ocean<->ice
