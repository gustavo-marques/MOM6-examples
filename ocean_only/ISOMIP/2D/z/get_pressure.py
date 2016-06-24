import numpy as np
import netCDF4

def get_rho(S,T):
    rho0=1027.51; Sref=34.2; Tref=-1.0
    alpha = 3.733e-5; beta = 7.843e-4
    rho = rho0 * (1 - alpha * (T-Tref) + beta * (S-Sref))
    return rho

salt=netCDF4.Dataset('ISOMIP_IC.nc').variables['Salt'][:]
temp=netCDF4.Dataset('ISOMIP_IC.nc').variables['Temp'][:]
rho=get_rho(salt[0,:,0,-1],temp[0,:,0,-1])
eta=netCDF4.Dataset('ISOMIP_IC.nc').variables['eta'][:]
z=0.5*(eta[0,0:-1,0,-1]+eta[0,1::,0,-1])
P=-916.7 * 9.8 * z
