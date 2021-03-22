from osgeo import gdal
import numpy as np

dataset = gdal.Open('CMC_hrdps_continental_TMP_TGL_2_ps2.5km_2021031900_P000-00.grb2', gdal.GA_ReadOnly)
message_count = dataset.RasterCount
