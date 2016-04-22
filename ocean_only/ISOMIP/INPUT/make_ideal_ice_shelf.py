#import matplotlib as mpl
#mpl.use('Agg')

import netCDF4
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt


# read provided netcdf
x1 = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['x'][:]
y1 = netCDF4.Dataset('Ocean1_input_geom_v1.01.nc').variables['y'][:]
[X1,Y1]=np.meshgrid(x1/1.0e3,y1/1.0e3)

# ideal file
icefile = netCDF4.Dataset('idealized.nc','r+')
height = icefile.variables['height'][:] 
x = x1[::2]/1.0e3
y = y1[::2]/1.0e3
[X,Y]=np.meshgrid(x,y)

for i in range(len(x)):
    if x[i]<=400.:
       height[:,i] = -100. #-720.
#    elif (x[i]>400.) and (x[i]<=500.):
#       height[:,i] = 31./5. * x[i] -3200 # hight goes from -620 to -100
#    elif (x[i]>500.) and (x[i]<=550.):
#       height[:,i] = 2.02022 * x[i] -1111.12 # hight goes from -100 to zero
    else:
       height[:,i] = 0.0


plt.figure()
plt.contourf(X,Y,height)
plt.colorbar()
#plt.show()
icefile.variables['height'][:] = height
icefile.close()
print 'Done!'

