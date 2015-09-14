import os
import time
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
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



average_temp = []

# STARTING SIMULATION
print('STARTING SIMULATION...')
until = Date(year=constants.END_YEAR, month=1)
temp = False
temperatures = []
results=open('results_and_plots/results.dat','w')
results.write(constants.constants_print())
results.write('date ')
for zone in earth.zones:
    results.write(str(zone.latitude())+' ')
results.write('avg\n')
while earth.DATE < until:
    # print('-----------------%s---------------------' % earth.DATE)
    if until - earth.DATE <= Date(year=1, month=0):
        temp = True
    results.write(str(earth.DATE.year)+'/'+str(earth.DATE.month)+' ')
    for zone in earth.zones:
        zone.calculate_temperature(Radiation.calculate_absorbed_radiation(zone))
        zone.calculate_temperature(Radiation.calculate_emmited_radiation(zone))
        earth.calculate_energy_flow_between_zones()
        earth.calculate_albedo_changes_due_to_water_phase_transitions()
        results.write('%.1f'%zone.temperature+' ')
        if temp:
            temperatures.append(zone.temperature)
    average_temp.append(earth.average_temp())
    results.write("%.1f"%average_temp[-1]+'\n')
    if temp:
       m = Basemap(width=12000000,height=9000000,projection='kav7',lat_0=0,lon_0=-0.)
       # draw a boundary around the map, fill the background.
       # this background will end up being the ocean color, since
       # the continents will be drawn on top.
       m.drawmapboundary(fill_color='aqua')
       # fill continents, set lake color same as ocean color.
       m.fillcontinents(color='coral',lake_color='aqua')
       # draw parallels and meridians.
       # label parallels on right and top
       # meridians on bottom and left
       m.drawparallels(np.arange(-90.,99.,15.),labels=[0,1,0,0])
       # labels = [left,right,top,bottom]

       # put some text next to the dot, offset a little bit
       # (the offset is in map projection coordinates)
       for i in range(0,12):
           lon, lat = 0, -90+i*15 # Location of Boulder
           # convert to map projection coords.
           # Note that lon,lat can be scalars, lists or numpy arrays.
           xpt,ypt = m(lon,lat)
           # convert back to lat/lon
           lonpt, latpt = m(xpt,ypt,inverse=True)
           plt.text(xpt+100000,ypt+100000,"%.1f" % temperatures[i])
       plt.title(str(earth.DATE)+' Avg temp: %.1f' % average_temp[-1])
       name='results_and_plots/temperature_'+str(earth.DATE.get_month())+'-'+str(earth.DATE.year)+'r.pdf'
       plt.savefig(name,format='pdf',bbox_inches='tight', pad_inches=0.05)
       plt.close()
       del temperatures[:]
    earth.DATE.step()
results.close()
# print(average_temp[-1])
# years=np.arange(0, len(np.array(average_temp))/12, 1/12)
# plt.plot(years , np.array(average_temp), 'k-', lw=2)
# plt.show()
