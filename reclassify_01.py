from osgeo import gdal
from tkinter import filedialog
import numpy as np

def reclassify(filecounter):

    #filename = filedialog.askopenfilename()
    driver = gdal.GetDriverByName('GTiff')
    raster = gdal.Open(r'D:\cag_poultry\test\data\result\test_review6{0}.tif'.format(filecounter))
    band = raster.GetRasterBand()
    lista = band.ReadAsArray()

    if filecounter == 0:


        lista[np.where( lista <= 6 )] = 5
        lista[np.where((6 < lista) & (lista <= 7)) ] = 4
        lista[np.where((7 < lista) & (lista <= 8)) ] = 3
        lista[np.where((8 < lista) & (lista <= 9)) ] = 2
        lista[np.where( lista >= 9 )] = 1
    elif filecounter == 1:
        lista[np.where(lista <= 5)] = 5
        lista[np.where((5 < lista) & (lista <= 10))] = 4
        lista[np.where((10 < lista) & (lista <= 15))] = 3
        lista[np.where((15 < lista) & (lista <= 20))] = 2
        lista[np.where(lista >= 20)] = 1
    """
    # reclassification
    for j in  range(file.RasterXSize):
        for i in  range(file.RasterYSize):
            if lista[i,j] <= 6:
                lista[i,j] = 1
            elif 6 < lista[i,j] <= 7:
                lista[i,j] = 2
            elif 7 < lista[i,j] <= 8:
                lista[i,j] = 3
            elif 8 < lista[i,j] <= 9:
                lista[i,j] = 4
            else:
                lista[i,j] = 5
    """
    # create new file
    file2 = driver.Create( r'D:\cag_poultry\test\data\result\reclassified_ras{0}.tif'.format(filecounter), file.RasterXSize , file.RasterYSize , 1)
    file2.GetRasterBand(1).WriteArray(lista)

    # spatial ref system
    proj = raster.GetProjection()
    georef = raster.GetGeoTransform()
    file2.SetProjection(proj)
    file2.SetGeoTransform(georef)
    file2.FlushCache()
#reclassify()
