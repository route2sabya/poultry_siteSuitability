import numpy
from osgeo import gdal

InputImage = 'ImageName'
OutputImage = 'OutImageName'

Image = gdal.Open(InputImage, gdal.GA_ReadOnly)
Driver = gdal.GetDriverByName(Image.GetDriver().ShortName)
X_Size = Image.RasterXSize
Y_Size = Image.RasterYSize
Projection = Image.GetProjectionRef()
GeoTransform = Image.GetGeoTransform()

# Read the first band as a numpy array
Band1 = Image.GetRasterBand(1).ReadAsArray()

# Create a new array of the same shape and fill with zeros
NewClass = numpy.zeros_like(Band1).astype('uint8')

# Reclassify using numpy.where
NewClass = numpy.where(((Band1 > 0) & (Band1 < 10)), 1, NewClass) # Reclassify as 1
NewClass = numpy.where(((Band1 >= 10) & (Band1 < 20)), 2, NewClass) # Reclassify as 2
NewClass = numpy.where(((NewClass == 0) & (Band1 >= 20)), 3, NewClass) # Reclassify as 3
del Band1

# Export the new classification to an image:
OutImage = Driver.Create(OutputImage, X_Size, Y_Size, 1, gdal.GDT_Byte)
OutImage.SetProjection(Projection)
OutImage.SetGeoTransform(GeoTransform)
OutBand = OutImage.GetRasterBand(1)
OutBand.SetNoDataValue(0)
OutBand.WriteArray(NewClass)
OutImage = None
del NewClass
print("Done.")