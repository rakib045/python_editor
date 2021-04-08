import netCDF4 as nc
import numpy as np

filename = 'D:\OneDrive_USask\OneDrive - University of Saskatchewan\PravinShervan\hybrid_test.mizuRoute.h.1997-01-01-00000.nc'

ds = nc.Dataset(filename)
print(ds)
#for dim in ds.dimensions.values():
#    print(dim)0

#print(ds['IRFroutedRunoff'][0][250]) 3002007
index = np.where(ds['reachID'][:] == 3002596)[0][0]
print(index)
print(ds['IRFroutedRunoff'][0][index])