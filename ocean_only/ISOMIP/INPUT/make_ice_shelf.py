import matplotlib as mpl
mpl.use('Agg')

import netCDF4
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt


# read provided netcdf
x = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['x'][::2]
y = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['y'][::2]
upperSurface = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['upperSurface'][::2,::2]
lowerSurface = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['lowerSurface'][::2,::2]
[X,Y]=np.meshgrid(x/1.0e3,y/1.0e3)

# MOM file
icefile = netCDF4.Dataset('isomip_ice_shelf3.nc','r+')
#area = icefile.variables['area'][:] 
#height = icefile.variables['height'][:] 

#x2 = x[::2] 
#y2 = y[::2] 
#[X2,Y2]=np.meshgrid(x2/1.0e3,y2/1.0e3)

#f = interpolate.interp2d(x, y, upperSurface, kind='linear')
#tmp_upper = f(x2,y2)

plt.figure()
plt.contourf(X,Y,upperSurface)
plt.colorbar()
plt.savefig('upperSurface.png')

#f = interpolate.interp2d(x, y, lowerSurface, kind='linear')
#tmp_lower = f(x2,y2)

plt.figure()
plt.contourf(X,Y,lowerSurface)
plt.colorbar()
plt.savefig('lowerSurface.png')

thick = upperSurface - lowerSurface
area = np.ones((thick.shape))* (x[1]-x[0]) * (y[1]-y[0])
area[thick==0.0]=0.0

plt.figure()
plt.contourf(X,Y,area)
plt.colorbar()
plt.savefig('area.png')

plt.figure()
plt.contourf(X,Y,thick)
plt.colorbar()
plt.savefig('thick.png')

icefile.variables['area'][:] = area
icefile.variables['thick'][:] = thick
icefile.variables['height'][:] = tmp_lower

icefile.close()
print 'Done!'

