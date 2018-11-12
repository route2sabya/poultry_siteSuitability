import csv
from osgeo import gdal
def tocsv():
    with open(r'D:\cag_poultry\test\data\result\test_review6.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        fn = gdal.Open(r'D:\cag_poultry\test\data\result\test_review6.tif')
        #rat = fn.GetRasterBand(1)
        #rat = rat.ReadAsArray()

        #Write out column headers
        icolcount=fn.GetColumnCount()
        cols=[]

        for icol in range(icolcount):
            cols.append(rat.GetNameOfCol(icol))
        csvwriter.writerow(cols)

        #Write out each row.
        irowcount = rat.GetColumnCount()
        for irow in range(irowcount):
            cols=[]
            for icol in range(icolcount):
                itype=rat.GetTypeOfCol(icol)
                if itype==gdal.GFT_Integer:
                    value='%s'%rat.GetValueAsInt(irow,icol)
                elif itype==gdal.GFT_Real:
                    value='%.16g'%rat.GetValueAsDouble(irow,icol)
                else:
                    value='%s'%rat.GetValueAsString(irow,icol)
                cols.append(value)
            csvwriter.writerow(cols)


