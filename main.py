from data.Data import Data
from data.Earth import *
from data.Radiation import *
from data.SurfaceType import *
from data.Zone import *
from dateutil.relativedelta import relativedelta

data = Data('data.csv')
earth = Earth(12, data.get_data())
until = datetime.datetime(year=2100, month=1, day=15)

while earth.DATE < until:
    #DO STH
    earth.DATE += relativedelta(months=1)

# calculate absorbed energy (radiation) for every zone -> temperature
# zone temperature -> calculate emitted energy (radiation) for every zone
# zones temperature -> energy flow between two adjacent zone
# calculate albedo changes (albedo<->temperature) ocean<->ice
# czy komity dzialaja
