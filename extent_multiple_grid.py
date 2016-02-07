import arcpy
from arcpy.sa import *

import numpy
import glob
import os

arcpy.CheckOutExtension('Spatial')

arcpy.env.workspace = 'e:/dev/antarctic-seaice-extent/antarctic_sea_ice.gdb'
arcpy.env.scratchWorkspace = 'e:/dev/antarctic-seaice-extent/antarctic_sea_ice_scratch.gdb'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('South Pole Lambert Azimuthal Equal Area')
arcpy.env.overwriteOutput = True

data_dir = 'e:/dev/antarctic-seaice-extent/data_monthly/'
data_listing = glob.glob('{}nt_2014*.tif'.format(data_dir))

if not arcpy.Exists('extent_results'):
    arcpy.CreateTable_management(arcpy.env.workspace, 'extent_results') 
    arcpy.AddField_management("extent_results", 'data_source', "TEXT")
    arcpy.AddField_management("extent_results", 'area', "DOUBLE")

table_input = arcpy.da.InsertCursor('extent_results', ['data_source', 'area'])

for data in data_listing:
    raster_name = os.path.basename(data)
    raster_name = raster_name.replace('.tif', '')
    seaice_raster = Raster(data)
    seaice_mask = Con(seaice_raster >= 15, 1)
    seaice_mask.save("{}_mask".format(raster_name))
    arcpy.RasterToPolygon_conversion(seaice_mask, "{}_mask_poly".format(raster_name))
    area_field = arcpy.da.TableToNumPyArray("{}_mask_poly".format(raster_name), "Shape_Area")
    total_area = area_field["Shape_Area"].sum()
    table_input.insertRow([raster_name, total_area])

del table_input
