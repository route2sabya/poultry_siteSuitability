#Import gdal
from osgeo import gdal
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog


src_filename = filedialog.askopenfilename()
#Open existing dataset
src_ds = gdal.Open( src_filename )

#Open output format driver, see gdal_translate --formats for list
format = "CSV"
driver = gdal.GetDriverByName( format )

#Output to new format
dst_ds = driver.CreateCopy( r'D:\cag_poultry\test\data\result\otgtiff.csv', src_ds, 0 )

#Properly close the datasets to flush to disk
dst_ds = None
src_ds = None