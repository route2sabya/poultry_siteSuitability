import gdal
from osgeo import osr
from osgeo import ogr
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os

raster_path = filedialog.askdirectory()
os.chdir(raster_path)
raster_path = r"{0}/raster.tif".format(raster_path)
print (raster_path)
shapefile = filedialog.askopenfilename()


# 1) opening the shapefile

source_ds = ogr.Open(shapefile)
source_layer = source_ds.GetLayer()


# 2) Creating the destination raster data source

pixelWidth = pixelHeight = 0.0001 # depending how fine you want your raster ##COMMENT 1
x_min, x_max, y_min, y_max = source_layer.GetExtent()
print (x_max,x_min,y_max,y_min)
cols = int((x_max - x_min) / pixelHeight)
rows = int((y_max - y_min) / pixelWidth)

target_ds = gdal.GetDriverByName('GTiff').Create(raster_path, cols, rows, 1,gdal.GDT_Float32) ##COMMENT 2
print (target_ds)

target_ds.SetGeoTransform((x_min, pixelHeight, 0, y_max, 0, -pixelHeight))##COMMENT 3

# 5) Adding a spatial reference ##COMMENT 4


target_dss = osr.SpatialReference()
target_dss.ImportFromEPSG(32643)
target_ds.SetProjection(target_dss.ExportToWkt())

band = target_ds.GetRasterBand(1)
band.SetNoDataValue(-9999) ##COMMENT 5

gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE = PH"]) ##COMMENT 6

target_ds = None ##COMMENT 7