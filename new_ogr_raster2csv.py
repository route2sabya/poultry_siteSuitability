#from osgeo import gdal,ogr

#fc=r'D:\cag_poultry\test\data\result\out_csv.csv'
#rast=r'‪D:\cag_poultry\test\data\result\otgtiff.tiff'

import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform
#from tkinter import *
#from tkinter.filedialog import askopenfilename
from tkinter import filedialog

fname = filedialog.askopenfilename()

# Read raster
with rasterio.open(fname) as r:
    T0 = r.transform# upper-left pixel corner affine transform
    p1 = Proj(r.crs)
    A = r.read()  # pixel values
    print (A)

# All rows and columns
cols, rows = np.meshgrid(np.arange(A.shape[2]), np.arange(A.shape[1]))

# Get affine transform for pixel centres
T1 = T0 * Affine.translation(0.5, 0.5)
# Function to convert pixel row/column index (from 0) to easting/northing at centre
rc2en = lambda r, c: (c, r) * T1

# All eastings and northings (there is probably a faster way to do this)
eastings, northings = np.vectorize(rc2en, otypes=[np.float, np.float])(rows, cols)

# Project all longitudes, latitudes
p2 = Proj(proj='latlong',datum='WGS84')
longs, lats = transform(p1,p2, eastings, northings)
print (longs[0], lats[0])





"""
def GetCentroidValue(fc,rast):
    #open vector layer
    drv=ogr.GetDriverByName('CSV') #assuming shapefile?
    ds=drv.Open(fc,True) #open for editing
    lyr=ds.GetLayer(0)

    #open raster layer
    src_ds=gdal.Open(rast)
    gt=src_ds.GetGeoTransform()
    rb=src_ds.GetRasterBand(1)
    gdal.UseExceptions() #so it doesn't print to screen everytime point is outside grid

    for feat in lyr:
        geom=feat.GetGeometryRef()
        mx=geom.Centroid().GetX()
        my=geom.Centroid().GetY()

        px = int((mx - gt[0]) / gt[1]) #x pixel
        py = int((my - gt[3]) / gt[5]) #y pixel
        try: #in case raster isnt full extent
            structval=rb.ReadRaster(px,py,1,1,buf_type=gdal.GDT_Float32) #Assumes 32 bit int- 'float'
            intval = struct.unpack('f' , structval) #assume float
            val=intval[0]
        except:
            val=-9999 #or some value to indicate a fail

        feat.SetField('YOURFIELD',val)
        lyr.SetFeature(feat)

    src_ds=None
    ds=None

GetCentroidValue(fc,rast)
"""