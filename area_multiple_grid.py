import numpy
import arcpy
from arcpy.sa import *
import glob
import os

arcpy.CheckOutExtension('Spatial')

# Setting up the processing environment
arcpy.env.workspace = 'e:/manch_app_exercise/antarctic_sea_ice.gdb'
arcpy.env.scratchWorkspace = 'e:/manch_app_exercise/antarctic_sea_ice_scratch.gdb'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(102020)
arcpy.env.overwriteOutput = True

# Input sea ice data directory and creation of a list of files
data_dir = 'E:/manch_app_exercise/all/'
data_listing = glob.glob('{}nt_????0901*.tif'.format(data_dir))

# Creating a table in the geodatabse to store results of the area calculation
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
    seaice_raster = Raster(data)
    seaice_mask = Con(seaice_raster >= 15, 1)
    seaice_mask.save('nt_19840902_n07_s_mask')
    arcpy.RasterToPolygon_conversion(seaice_mask, "nt_19840902_n07_v01_s_poly")
    area_field = arcpy.da.TableToNumPyArray("nt_19840902_n07_v01_s_poly", "Shape_Area")
    total_area = area_field["Shape_Area"].sum()
    table_input.insertRow([raster_name, total_area])

del table_input

