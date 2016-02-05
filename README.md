# antarctic-seaice-extent
A tutorial to calculate Antarctic Sea Ice extent from a timeseries of Sea Ice concentration data

## Introduction

This exercise presents a way you might want to calculate sea ice extent from sea ice concentration data, using ArcGIS.

The exercise will begin by showing a flow of commands to go from reading in the sea ice concentration data, to ending up with a calculation of the area. It will demonstrate this on one single band raster dataset. 

The exercise will show how to do this by typing commands into the Python prompt in ArcGIS Desktop. 

It will go on to show how to perform the same commands on any number of datasets. Why? Because the dataset we are using for this is actually 33 years long. 33 years times 365 days (give or take a few leap years and data gaps), is 12045 single band rasters. 

## Learning outcomes

GIS based functions
* Raster conditional statements
* Awareness of choosing correct projections
* Area calculations
* Raster to vector conversions

Datasets
* Working with high temporal resolution datasets

Coding / Scripting
* An introduction to scripting in ArcGIS using ArcPy (Python library). 

## Tools required

ESRI ArcGIS 10, 10.1, 10.2 or ArcGIS Pro with Spatial Analyst extension

## The data source



## Project setup

1. Create a working directory

2. Unzip the `data` directory into here

3. Open ArcMap

4. Using ArcCatalog, create two file geodatabases in the working directory called `antarctic-sea-ice.gdb` and `antarctic-sea-ice-scratch.gdb`

5. Open up the Python prompt and type the following:
```python
arcpy.env.workspace = 'path-to-working-directory/antarctic-sea-ice.gdb'
arcpy.env.scratchWorkspace = 'path-to-working-directory/antarctic-sea-ice-scratch.gdb'
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(102020)
arcpy.env.overwriteOutput = True

```
Note that `path-to-working-directory` should be replaced with the actual path you the working directory that was created in step number 1, ie. `c:/working-dir/` or something similar. 

The above commands are simply setting the processing environment for the operations that will be conducted. 

`arcpy.env.workspace` is the default workspace that all outputs will be saved to. The `arcpy.env.scratchWorkspace` is for all the temporary files that ArcGIS might create during the processing. 

`arcpy.env.outputCoordinateSystem` simply ensures that all outputs will be converted to an equal area projection. In this case EPSG 102020, which is South Polar Lambert Azimuthal Equal Area. We will be calucating areas, so it is important to ensure we calculate on an equal area projection. 

Finally, `arcpy.env.overwriteOutput = True` prevents the annoyance of having to delete outputs from the database before repeats of the same process are completed.  


## Extracting area of sea ice extent from one piece of data

In order to extract the sea ice extent from the dataset of sea ice concetration, we need to chain together a series of functions. To do this we will use ArcPy commands.

Before that though, choose a raster from the `data` directory and add it to ArcMap. For this example we will use `nt_19810103_n07_v01_s.tif`

The workflow will be:

1. Load in the raster data into an ArcPy object.
2. Use raster conditional statement within the ArcGIS Spatial Analyst extension, to extract all cells that are 15% or above, indicating the extent of sea ice, and output a raster mask with all sea ice cells with the value of 1.
3. Convert the raster to a polygon feature class. Note, there might be more than one polygon geometry. 
4. Total up the areas of the polygons within the feature class. 

Type the following into the Python prompt:

```python
import numpy
from arcpy.sa import *

```
Here we are simply importing some extra python functionality which allows us to easily total up the polygon areas at the end.. we will come to this...

And we are importing all the ArcPy Spatial Analyst functions as well. Make sure you have this extension enabled. 

```python
seaice_raster = Raster('nt_19810103_n07_v01_s.tif')
seaice_mask = Con(seaice_raster >= 15, 1)
seaice_mask.save('nt_19810103_n07_v01_s_mask')
```
In this three lines we are creating a Raster object, pulling out all the cells whose values are 15 or above to a mask object, and finally saving the mask object to the geodatabase. 

```python
arcpy.RasterToPolygon_conversion(seaice_mask, "nt_19810103_n07_v01_s_poly")
```

This line converts the raster mask to a polygon feature class and saves it to the geodatabase.

```python
area_field = arcpy.da.TableToNumPyArray("nt_19810103_n07_v01_s_poly", "Shape_Area")
total_area = area_field["Shape_Area"].sum()
print total_area

```

These final few lines extract all the records in the `Shape_Area` field of the attribute table, which is already calculated in the previous step by default. It them sums these values which give is `total_area`. 

## Extracting sea ice extent from multiple grids

As mentioned above, daily sea ice concentration data from this dataset goes back to 1978. However, for this exercise, we are just going to see how the sea ice extent changes over one year. We could take 365 data grids, but instead we are only going to take 24, from the 1st and 15th of every month. 

In the `data` directory, 

### We need to write a script

### We need somewhere to store the data

## Extracting sea ice extent from any number of days of data

## Final thoughts...

If this is the first time you have tried scripting, don't worry. Try things, make mistakes, break things and work out why they aren't running. Play around with different ArcPy functions and enjoy. You can't break anything!

Finally, watch out for typos!


## What can you do from here?

Here are some ideas for ways to extend this porject, now that you have a script for extracting sea ice extent. 

* Download [all the monthly data from NSIDC](https://nsidc.org/data/nsidc-0051), and run this script over the whole time series. 

* Download all the daily data from the timeseries and run this script over all available days, one day for each year, one month, or whatever you choose. To do this, just select the day/month/year of rasters you want by ammending this line in `area_multiple_grid.py`:

```python
# ie. 1st September for every year
data_listing = glob.glob('{}nt_????0901*.tif'.format(data_dir))

# ie. all rasters available for the year 1984
data_listing = glob.glob('{}nt_1984*.tif'.format(data_dir))

```

* Graph out the results

* Create a time attribute on the polygon features and run animations. 

* Calculate the extent of ice that is classified as over 50% concentration. 

## Reference

Cavalieri, D. J., C. L. Parkinson, P. Gloersen, and H. J. Zwally. 1996, updated yearly. Sea Ice Concentrations from Nimbus-7 SMMR and DMSP SSM/I-SSMIS Passive Microwave Data, Version 1. [indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. http://dx.doi.org/10.5067/8GQ8LZQVL0VL. [Date Accessed].
