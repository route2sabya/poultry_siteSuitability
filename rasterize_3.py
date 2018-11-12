import random
from osgeo import gdal, ogr,osr, gdalconst
from tkinter import *
#from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os
import time
import numpy as np
#import pandas as pd
import threading

def make_dir(directory_name):
    if not os.path.exists(directory_name):
        print ("path doesn't exist. trying to make")
        os.makedirs(directory_name)
        print ("directory created. ")


def rasterize_reclassify(pixel_size=50.5591322649074):
    param_input = input("input the desired field precisely separated by commas:      ")
    i_ele = [(x.strip()) for x in param_input.split(',')]

    test_shp = filedialog.askopenfilename()

    for ele in i_ele:

        #ele = param_input
        #global RCF,filecounter,pixel_size

        #for ele in keep_params:

        #counter = 1
        #for ele in keep_params:

        #test_shp = filedialog.askopenfilename()
        # Open the data source
        orig_data_source = ogr.Open(test_shp)
        # Make a copy of the layer's data source because we'll need to
        # modify its attributes table

        source_ds = ogr.GetDriverByName("Memory").CopyDataSource(
            orig_data_source, "")
        source_layer = source_ds.GetLayer(0)
        # srs = osr.SpatialReference()
        # source_srs = srs.ImportFromEPSG(32643)
        source_srs = source_layer.GetSpatialRef()
        #print(source_srs)
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        # Create a field in the source layer to hold the features colors

        # for ele in keep_params:

        field_def = ogr.FieldDefn(ele, ogr.OFTReal)
        source_layer.CreateField(field_def)
        source_layer_def = source_layer.GetLayerDefn()
        field_index = source_layer_def.GetFieldIndex(ele)
        # Generate random values for the color field (it's here that the value
        # of the attribute should be used, but you get the idea)
        # counter = 0
        for feature in source_layer:
            ph_data = float(feature[ele])
            # print (str(feature))
            # for ik in  feature:
            #    print (ik[RASTERIZE_COLOR_FIELD])
            feature.SetField(field_index, ph_data)
            source_layer.SetFeature(feature)
            # Create the destination data source
        x_res = int((x_max - x_min) / pixel_size)
        y_res = int((y_max - y_min) / pixel_size)
        target_ds = gdal.GetDriverByName('GTiff').Create(r'processor\test_review_{0}.tif'.format(ele),
                                                             x_res,
                                                             y_res, 3, gdal.GDT_Float32)
        target_ds.SetGeoTransform((
                x_min, pixel_size, 0,
                y_max, 0, -pixel_size,
            ))

        if source_srs:
            # Make the target raster have the same projection as the source
            target_ds.SetProjection(source_srs.ExportToWkt())
        else:
            # Source has no projection (needs GDAL >= 1.7.0 to work)
            target_ds.SetProjection('LOCAL_CS["arbitrary"]')
            # Rasterize
        err = gdal.RasterizeLayer(target_ds, (3, 2, 1), source_layer,
                                      burn_values=(0, 0, 0),
                                      options=["ATTRIBUTE=%s" % ele])
        if err != 0:
            raise Exception("error rasterizing layer: %s" % err)
        # return err

        time.sleep(3)
        # target_ds2 = target_ds
        driver = gdal.GetDriverByName('GTiff')
        # raster = gdal.Open(r'\processor\test_review_{0}.tif'.format(ele))
        band = target_ds.GetRasterBand(1)
        lista = band.ReadAsArray()

        if ele == "PH":

            lista[np.where(lista <= 6)] = 5.0
            lista[np.where((6 < lista) & (lista <= 7))] = 4.0
            lista[np.where((7 < lista) & (lista <= 8))] = 3.0
            lista[np.where((8 < lista) & (lista <= 9))] = 2.0
            lista[np.where(lista >= 9)] = 1.0
            ph_band = lista
        elif ele == "SOIL_DEPTH":
            lista[np.where(lista <= 5)] = 5.0
            lista[np.where((5 < lista) & (lista <= 10))] = 4.0
            lista[np.where((10 < lista) & (lista <= 15))] = 3.0
            lista[np.where((15 < lista) & (lista <= 20))] = 2.0
            lista[np.where(lista >= 20)] = 1.0
            sd_band = lista

        elif ele == "CLAY_PER":
            lista[np.where(lista <= 10)] = 1.0
            lista[np.where((10 < lista) & (lista <= 20))] = 2.0
            lista[np.where((20 < lista) & (lista <= 30))] = 3.0
            lista[np.where((30 < lista) & (lista <= 40))] = 2.0
            lista[np.where(lista >= 40)] = 1.0
            cp_band = lista



        #result_band = (ph_band * 0.5) + (sd_band * 0.25) + (cp_band * 0.25)
        file2 = driver.Create(r'processor\reclassified_ras_{0}.tif'.format(ele),
                              target_ds.RasterXSize, target_ds.RasterYSize, 1)
        file2.GetRasterBand(1).WriteArray(lista)

        # spatial ref system
        proj = target_ds.GetProjection()
        print (proj)
        georef = target_ds.GetGeoTransform()
        file2.SetProjection(proj)
        file2.SetGeoTransform(georef)
        source_ds = None
        file2 = None
        err = None


    make_dir(r"output_raster_directory")

    driver_result = gdal.GetDriverByName('GTiff')
    result_band = (ph_band * 0.5) + (sd_band * 0.3) +(cp_band * 0.2)
    file_raster = driver_result.Create(r'output_raster_directory\result_raster.tif',
                          target_ds.RasterXSize, target_ds.RasterYSize, 1)
    file_raster.GetRasterBand(1).WriteArray(result_band)

    # spatial ref system
    proj_raster = target_ds.GetProjection()
    georef_raster = target_ds.GetGeoTransform()
    file_raster.SetProjection(proj_raster)
    file_raster.SetGeoTransform(georef_raster)
    target_ds = None
    file_raster = None
    print("Done")

######################################################################################

make_dir(r"processor")
sys.setrecursionlimit(9000000)
threading.stack_size(200000000)
thread = threading.Thread(target=rasterize_reclassify(pixel_size=50.5591322649074))
thread.start()


import shutil
shutil.rmtree(r"processor")




