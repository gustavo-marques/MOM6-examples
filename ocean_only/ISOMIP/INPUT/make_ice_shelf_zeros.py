import matplotlib as mpl
mpl.use('Agg')

import netCDF4
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt


# read provided netcdf
x = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['x'][:]
y = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['y'][:]
upperSurface = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['upperSurface'][:]
lowerSurface = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['lowerSurface'][:]
[X,Y]=np.meshgrid(x/1.0e3,y/1.0e3)

# MOM file
icefile = netCDF4.Dataset('isomip_ice_shelf2.nc','r+')
area = icefile.variables['area'][:] 

x2 = x[::2] 
y2 = y[::2] 
[X2,Y2]=np.meshgrid(x2/1.0e3,y2/1.0e3)

f = interpolate.interp2d(x, y, upperSurface, kind='linear')
tmp_upper = f(x2,y2)

plt.figure()
plt.contourf(X2,Y2,tmp_upper)
plt.colorbar()
plt.savefig('upperSurface.png')

f = interpolate.interp2d(x, y, lowerSurface, kind='linear')
tmp_lower = f(x2,y2)

plt.figure()
plt.contourf(X2,Y2,tmp_lower)
plt.colorbar()
plt.savefig('lowerSurface.png')

thick = tmp_upper - tmp_lower
area = np.ones((thick.shape))* (x2[1]-x2[0]) * (y2[1]-y2[0])
area[thick==0.0]=0.0

plt.figure()
plt.contourf(X2,Y2,area)
plt.colorbar()
plt.savefig('area.png')

plt.figure()
plt.contourf(X2,Y2,thick)
plt.colorbar()
plt.savefig('thick.png')

icefile.variables['area'][:] = 0.0 #area
icefile.variables['thick'][:] = 0.0 #thick
icefile.close()
print 'Done!'

