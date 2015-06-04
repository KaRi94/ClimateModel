from data.Earth import *
from data.Radiation import *
from data.SurfaceType import *
from data.Zone import *

earth = Earth()

#test
print(earth.radius)

# calculate absorbed energy (radiation) for every zone -> temperature
# zone temperature -> calculate emitted energy (radiation) for every zone
# zones temperature -> energy flow between two adjacent zone
# calculate albedo changes (albedo<->temperature) ocean<->ice