import netCDF4

icefile = netCDF4.Dataset('isomip_ice_shelf1.nc','r+')
icefile.variables['area'][:] = 0.0
icefile.variables['thick'][:] = 0.0
icefile.close()
print 'Done!'
