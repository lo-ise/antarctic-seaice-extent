# antarctic-seaice-extent
A tutorial to calculate Antarctic Sea Ice extent from a timeseries of Sea Ice concentration data

## Introduction

This exercise presents a way you might want to calculate sea ice extent from sea ice concentration data, using ArcGIS.

The exercise will begin by showing a flow of commands to go from reading in the sea ice concentration data, to ending up with a calculation of the area. It will demonstrate this with one days worth of data, a single band raster dataset. 

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
