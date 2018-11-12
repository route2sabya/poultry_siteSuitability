from osgeo import gdal
import numpy


def createRAT():
    ds = gdal.Open(r'D:\cag_poultry\test\data\result\test_review5.tif')
    rb = ds.GetRasterBand(1)
    #print (rb)
    u = numpy.unique(rb.ReadAsArray())
    #print (len(u))

    #print (u.size)
    r = numpy.random.uniform(0,1000, size=u.size)

    rat = gdal.RasterAttributeTable()
    rat.CreateColumn("Value", gdal.GFT_Real, gdal.GFU_Generic)
    rat.CreateColumn("RANDOM", gdal.GFT_Real, gdal.GFU_Generic)
    for i in range(u.size):
        #print (float(r[i]))
        #print (float(u[i]))
        rat.SetValueAsDouble(i,0,float(u[i]))
        rat.SetValueAsDouble(i,1,float(r[i]))
    rb.SetDefaultRAT(rat)




    ds = None
createRAT()