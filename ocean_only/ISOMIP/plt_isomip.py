import matplotlib as mpl
mpl.use('Agg')

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from misc_mom import *

def get_rho(S,T):
    rho0=1027.51; Sref=34.2; Tref=-1.0
    alpha = 3.733e-5; beta = 7.843e-4
    rho = rho0 * (1 - alpha * (T-Tref) + beta * (S-Sref))
    return rho

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

icfile= netCDF4.Dataset('ISOMIP_IC.nc')
salt = icfile.variables['Salt'][:]
temp = icfile.variables['Temp'][:]
u = icfile.variables['u'][:]
v = icfile.variables['v'][:]
e = icfile.variables['eta'][:]
h = icfile.variables['h'][:]
rho = get_rho(salt,temp) - 1000

rlev=np.linspace(rho.min(),rho.max(),50)
tlev=np.linspace(temp.min(),1.1,50)
slev=np.linspace(salt.min(),salt.max(),50)
hlev=np.linspace(10,100,50)
nt,nz,ny,nx = temp.shape

for t in range(nt):
    X,Z,T=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], temp[t,:,ny/2,0:-1], representation='linear')
    X,Z,S=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], salt[t,:,ny/2,0:-1], representation='linear')
    X,Z,R=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], rho[t,:,ny/2,0:-1], representation='linear')
    X,Z,H=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], h[t,:,ny/2,0:-1], representation='linear')
    plt_vsection(X,Z,T,'temp','[$^o$C]',tlev,0.0,t)
    plt_vsection(X,Z,S,'salt','[psu]',slev,0.0,t)
    plt_vsection(X,Z,R,'rho','[kg m$^{-3}$]',rlev,0.0,t)
    plt_vsection(X,Z,H,'h','[m]',hlev,0.0,t)



pfile=netCDF4.Dataset('prog__0001_001.nc')
n = 1
salt = pfile.variables['salt'][::n,:]
temp = pfile.variables['temp'][::n,:]
u = pfile.variables['u'][::n,:]
v = pfile.variables['v'][::n,:]
e = pfile.variables['e'][::n,:]
h = pfile.variables['h'][::n,:]
rho = get_rho(salt,temp) - 1000
time=pfile.variables['Time'][::n]/24. # time in days

nt,nz,ny,nx = temp.shape

for t in range(nt):
    print 'Day:',t
    X,Z,T=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], temp[t,:,ny/2,0:-1], representation='linear')
    X,Z,S=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], salt[t,:,ny/2,0:-1], representation='linear')
    X,Z,R=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], rho[t,:,ny/2,0:-1], representation='linear')
    X,Z,H=section2quadmesh(lon[ny/2,:],e[t,:,ny/2,0:-1], h[t,:,ny/2,0:-1], representation='linear')
    plt_vsection(X,Z,T,'temp','[$^o$C]',tlev,time[t],t+1)
    plt_vsection(X,Z,S,'salt','[psu]',slev,time[t],t+1)
    plt_vsection(X,Z,R,'rho','[kg m$^{-3}$]',rlev,time[t],t+1)
    plt_vsection(X,Z,H,'h','[m]',hlev,time[t],t+1)

print 'Done!'
