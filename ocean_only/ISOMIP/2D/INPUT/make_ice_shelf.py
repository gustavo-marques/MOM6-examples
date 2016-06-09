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
icefile = netCDF4.Dataset('2D_IC_zeros.nc','r+')

thick = upperSurface - lowerSurface
area = np.ones((thick.shape))* (x[1]-x[0]) * (y[1]-y[0])
area[thick==0.0]=0.0

icefile.variables['area'][0,:] = area[20,:]
icefile.variables['area'][1,:] = area[20,:]

icefile.variables['thick'][0,:] = 0.0 #thick[20,:]
icefile.variables['thick'][1,:] = 0.0 #thick[20,:]

icefile.variables['height'][0,:] = 0.0 #lowerSurface[20,:]
icefile.variables['height'][1,:] = 0.0 #lowerSurface[20,:]

icefile.close()
print 'Done!'

