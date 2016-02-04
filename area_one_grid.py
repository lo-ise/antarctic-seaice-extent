import numpy
import arcpy
from arcpy.sa import *

in_ras = 'nt_19810103_n07_v01_s.tif'
 
arcpy.env.workspace = 'e:/manch_app_exercise/antarctic_sea_ice.gdb'
arcpy.env.scratchWorkspace = 'e:/manch_app_exercise/antarctic_sea_ice_scratch.gdb'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(102020)

seaice_raster = Raster('nt_19810103_n07_v01_s.tif')
seaice_mask = Con(seaice_raster >= 15, 1)
seaice_mask.save('nt_19810103_n07_v01_s_mask')
arcpy.RasterToPolygon_conversion(seaice_mask, "nt_19810103_n07_v01_s_poly")
area_field = arcpy.da.TableToNumPyArray("nt_19810103_n07_v01_s_poly", "Shape_Area")
total_area = area_field["Shape_Area"].sum()

print total_area
