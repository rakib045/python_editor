import xarray as xr

ds = xr.open_dataset("CMC_hrdps_continental_TMP_TGL_2_ps2.5km_2021031900_P000-00.grib2", engine="pyonio")

for v in ds:
    print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))