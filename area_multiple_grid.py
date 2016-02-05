import arcpy
from arcpy.sa import *

import numpy
import glob
import os

arcpy.CheckOutExtension('Spatial')

# Setting up the processing environment
arcpy.env.workspace = 'e:/dev/antarctic-seaice-extent/antarctic_sea_ice.gdb'
arcpy.env.scratchWorkspace = 'e:/dev/antarctic-seaice-extent/antarctic_sea_ice_scratch.gdb'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('South Pole Lambert Azimuthal Equal Area')
arcpy.env.overwriteOutput = True

# Input sea ice data directory and creation of a list of files
data_dir = 'e:/dev/antarctic-seaice-extent/data_monthly/'
data_listing = glob.glob('{}nt_201401*.tif'.format(data_dir))

# Creating a table in the geodatabase to store results of the area calculation
if not arcpy.Exists('extent_results'):
    arcpy.CreateTable_management(arcpy.env.workspace, 'extent_results') 
    arcpy.AddField_management("extent_results", 'data_source', "TEXT")
    arcpy.AddField_management("extent_results", 'area', "DOUBLE")

# This line creates an object for inputing data into the results table
table_input = arcpy.da.InsertCursor('extent_results', ['data_source', 'area'])

# Here, we loop through the file listing and for each input raster, we do the following:
# - Create a Raster object
# - Query this raster object to extract a mask with only cells above 15
# - Save the mask to the geodatabase
# - Convert the mask to a polygon feature class and save it to the geodatabase
# - Total up the area of each polygon within the feature class
# - Add the total area to a new row in the results table

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

