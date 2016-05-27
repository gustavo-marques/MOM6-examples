import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from misc_mom import *

data=netCDF4.Dataset('ocean_geometry.nc')
D=data.variables['D'][:]
lonh=data.variables['lonh'][:]
lath=data.variables['lath'][:]
[lon,lat]=np.meshgrid(lonh,lath)
plt.figure()
plt.contourf(lon,lat,D)
plt.colorbar()
plt.xlabel('x [km]')
plt.ylabel('y [km]')
plt.savefig('MOM6_geometry.png')
#plt.show()

icfile= netCDF4.Dataset('Initial_state.nc')
salt = icfile.variables['Salt'][:]
temp = icfile.variables['Temp'][:]
u = icfile.variables['u'][:]
v = icfile.variables['v'][:]
e = icfile.variables['eta'][:]
h = icfile.variables['h'][:]

slev=np.linspace(salt.min(),salt.max(),50)
hlev=np.linspace(10,100,50)
nt,nz,ny,nx = temp.shape

for t in range(nt):
    X,Z,S=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], salt[t,:,ny/2,0:-1], representation='linear')
    X,Z,H=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], h[t,:,ny/2,0:-1], representation='linear')
    plt_vsection(X,Z,S,'salt','[psu]',slev,0.0,t)
    plt_vsection(X,Z,H,'h','[m]',hlev,0.0,t)



pfile=netCDF4.Dataset('prog.nc')
salt = pfile.variables['salt'][:]
temp = pfile.variables['temp'][:]
u = pfile.variables['u'][:]
v = pfile.variables['v'][:]
e = pfile.variables['e'][:]
h = pfile.variables['h'][:]
time=pfile.variables['Time'][:]*24. # time in hours

nt,nz,ny,nx = temp.shape

for t in range(nt):
    print 'Time is:',t
    X,Z,S=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], salt[t,:,ny/2,0:-1], representation='linear')
    X,Z,H=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], h[t,:,ny/2,0:-1], representation='linear')
    plt_vsection(X,Z,S,'salt','[psu]',slev,time[t],t+1)
    plt_vsection(X,Z,H,'h','[m]',hlev,time[t],t+1)

print 'Done!'
