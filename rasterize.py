from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst
from tkinter.filedialog import askopenfilename
from tkinter import filedialog


ndsm = filedialog.askopenfilename()
shp = filedialog.askopenfilename()
data = gdal.Open(ndsm, gdalconst.GA_ReadOnly)
geo_transform = data.GetGeoTransform()
#source_layer = data.GetLayer()
x_min = geo_transform[0]
y_max = geo_transform[3]
x_max = x_min + geo_transform[1] * data.RasterXSize
y_min = y_max + geo_transform[5] * data.RasterYSize
x_res = data.RasterXSize
y_res = data.RasterYSize
mb_v = ogr.Open(shp)
mb_l = mb_v.GetLayer()
pixel_width = geo_transform[1]
output_path = filedialog.askdirectory()
output = r"{0}/output.tif".format(output_path)
target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Float32)
target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
band = target_ds.GetRasterBand(1)
NoData_value = -999999
band.SetNoDataValue(NoData_value)
band.FlushCache()
gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=PH"])

target_ds = None