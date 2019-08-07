# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:29:03 2019

@author: wike4167
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:51:58 2019
GIS3 Group Project script
@author: wike4167
This is the version which creates the WCM raster
"""
# Set environment settings
import arcpy
from arcpy import env
from arcpy.sa import *
import arcpy.sa as sa
import numpy as np
arcpy.CheckOutExtension("Spatial")
env.workspace = "D:/finalData"
env.overwriteOutput = 1


#Defining variables
NationalForestMask = 'vector_data.mdb/National_Forest'
themeFile = 'inputs/dem_mask'
theme = sa.Raster(themeFile)


#Lines 28-39 are necessary so that at the end of the analysis, you can convert from Numpy Array back to a raster with the 
#correct spatial reference and size.

#Find the number of rows and columns
theme.height #number of rows - Y axis
theme.width #number of columns - X axis
#get cell size; 
cellSize = theme.meanCellHeight
#get lower left point of extent to write output after analysis
llpnt = theme.extent.lowerLeft
#get spatial reference object from the raster object
spref = theme.spatialReference
#check datatype of original raster grid
theme.pixelType

"""
Elevation Reclass

Elevation raster was downloaded from the colorado data atlas on the Z drive in Kesda

"""

#convert raster objects to numpy arrays
themeNp = arcpy.RasterToNumPyArray(theme)

#Here, wecreate class breaks for the layer we are analysing

maxValue=4405
minValue=1594
numberofclasses=10

interval = (maxValue-minValue)/numberofclasses

#this code creates a list of equidistant classes
classbreaks = [minValue]
for i in range(0,numberofclasses):
    classbreaks.append(classbreaks[i]+interval)
    

#This np.where statement reclassifies the raster into the assigned classes.
elevReclass= np.where(themeNp > classbreaks[9], 10, np.where(themeNp > classbreaks[8], 9,np.where(themeNp > classbreaks[7], 8, 
                    np.where(themeNp > classbreaks[6], 7, np.where(themeNp > classbreaks[5], 6, 
                    np.where(themeNp > classbreaks[4], 5, np.where(themeNp > classbreaks[3], 4, 
                    np.where(themeNp > classbreaks[2], 3, np.where(themeNp > classbreaks[1], 2, 
                    np.where(themeNp > classbreaks[0], 1, 0))))))))))


"""
Access analysis

The themeFile "access_pop" was created using the cost distance tool. The cost raster was the RCL file and the source data
was the top 20 most populous cities in CO.

"""
themeFile = 'inputs/access_mask'
theme = sa.Raster(themeFile)
themeNp = arcpy.RasterToNumPyArray(theme)

maxValue= 610
minValue= 0
numberofclasses=10

interval = (maxValue-minValue)/numberofclasses

#edit this code to create a list of equidistant classes
classbreaks = [minValue]
for i in range(0,numberofclasses):
    classbreaks.append(classbreaks[i]+interval)

accessReclass= np.where(themeNp > classbreaks[9], 1, np.where(themeNp > classbreaks[8], 2,np.where(themeNp > classbreaks[7], 3, 
                    np.where(themeNp > classbreaks[6], 4, np.where(themeNp > classbreaks[5], 5, 
                    np.where(themeNp > classbreaks[4], 6, np.where(themeNp > classbreaks[3], 7, 
                    np.where(themeNp > classbreaks[2], 8, np.where(themeNp > classbreaks[1], 9, 
                    np.where(themeNp > classbreaks[0], 10, 0))))))))))

"""
Substations Portion
The "plinesed" layer was created using the Euclidean Distance tool with the powerlines feature data.
"""

themeFile = 'inputs/subs_mask'
theme = sa.Raster(themeFile)

themeNp = arcpy.RasterToNumPyArray(theme)

maxValue=50000
minValue=0
numberofclasses=10

interval = (maxValue-minValue)/numberofclasses

classbreaks = [minValue]
for i in range(0,numberofclasses):
    classbreaks.append(classbreaks[i]+interval)

stationsReclass= np.where(themeNp > classbreaks[9], 1, np.where(themeNp > classbreaks[8], 2,np.where(themeNp > classbreaks[7], 3, 
                    np.where(themeNp > classbreaks[6], 4, np.where(themeNp > classbreaks[5], 5, 
                    np.where(themeNp > classbreaks[4], 6, np.where(themeNp > classbreaks[3], 7, 
                    np.where(themeNp > classbreaks[2], 8, np.where(themeNp > classbreaks[1], 9, 
                    np.where(themeNp > classbreaks[0], 10, 0))))))))))

"""
precip Portion
The co_precipr layer was downloaded and pre-masked to the national forest layer to save RAM.
"""

themeFile = '/inputs/snow_mask'
theme = sa.Raster(themeFile)

themeNp = arcpy.RasterToNumPyArray(theme)

maxValue=1414.02
minValue=54.71
numberofclasses=10

interval = (maxValue-minValue)/numberofclasses

classbreaks = [minValue]
for i in range(0,numberofclasses):
    classbreaks.append(classbreaks[i]+interval)

precipReclass= np.where(themeNp > classbreaks[9], 10, np.where(themeNp > classbreaks[8], 9,np.where(themeNp > classbreaks[7], 8, 
                    np.where(themeNp > classbreaks[6], 7, np.where(themeNp > classbreaks[5], 6, 
                    np.where(themeNp > classbreaks[4], 5, np.where(themeNp > classbreaks[3], 4, 
                    np.where(themeNp > classbreaks[2], 3, np.where(themeNp > classbreaks[1], 2, 
                    np.where(themeNp > classbreaks[0], 1, 0))))))))))

"""
Aspect Portion
The aspect layer was created using the aspect tool and has been pre-masked to save RAM.
"""

themeFile = 'inputs/aspect_mask'
theme = sa.Raster(themeFile)

themeNp = arcpy.RasterToNumPyArray(theme)

aspectReclass= np.where(themeNp > 316, 10, np.where(themeNp > 225, 5,np.where(themeNp > 135, 0, 
                    np.where(themeNp > 45, 5, np.where(themeNp > 0, 10, 0)))))

"""
All of the code above has created five numpy layers which represent the best aspect, elevation, snowfall,
distance to substations, and accessability to the populations of Colorado.
This section converts them to rasters, multiplies each layer by a weight (weights should add up to 1), and then
adds the weighted rasters together. This sum of the weighted rasters is the weighted criteria model.
"""



elevRast = arcpy.NumPyArrayToRaster(elevReclass,llpnt,cellSize,cellSize)
accessRast = arcpy.NumPyArrayToRaster(accessReclass,llpnt,cellSize,cellSize)
aspectRast = arcpy.NumPyArrayToRaster(aspectReclass,llpnt,cellSize,cellSize)
stationsRast = arcpy.NumPyArrayToRaster(stationsReclass,llpnt,cellSize,cellSize)
precipRast = arcpy.NumPyArrayToRaster(precipReclass,llpnt,cellSize,cellSize)

arcpy.DefineProjection_management(elevRast,spref)
arcpy.DefineProjection_management(accessRast,spref)
arcpy.DefineProjection_management(aspectRast,spref)
arcpy.DefineProjection_management(stationsRast,spref)
arcpy.DefineProjection_management(precipRast,spref)


final = (elevRast * 0.2) + (accessRast * 0.2) + (aspectRast * 0.2) + (stationsRast * 0.2) + (precipRast * 0.2)

arcpy.DefineProjection_management(final,spref)
final.save("D:/finalData/post_inputs/equal_WCM")

#import IPython
#app = IPython.Application.instance()
#app.kernel.do_shutdown(True)  

"""
Post Processing
"""

import arcpy
from arcpy import env
from arcpy.sa import *
import arcpy.sa as sa
import numpy as np
from math import *


arcpy.CheckOutExtension("Spatial")
# Set environment settings
env.workspace = "D:/FinalData/post_inputs"
env.overwriteOutput = 1

#Defining variables
equalWCM = 'equal_WCM'
arcpy.env.extent = arcpy.Extent(139000.845106, 4093663.696099, 763840.845106, 4547023.696099)

#This erases the already existing ski areas from the result. Ski areas DEM is a masked DEM of the existing ski areas.
arcpy.gp.RasterCalculator_sa("SetNull( ~IsNull(\"skiareas_dem\"),\"equal_wcm\")", "D:/finalData/post_inputs/minusVail")

#Define input
minusVail = "D:/FinalData/post_inputs/minusVail"
#Reclassify the WCM so that it can be run through region group
arcpy.gp.Reclassify_sa(minusVail, "VALUE", "0 1 1;1 2 2;2 3 3;3 4 4;4 5.000000 5;5.000000 6 6;6 7.000000 7;7.000000 9 9", "D:/finalData/post_inputs/reclassWCM", "DATA")

#Define input and run region group
reclass = "D:/finalData/post_inputs/reclassWCM"
arcpy.gp.RegionGroup_sa(reclass, "D:/finalData/post_inputs/rgGroup", "FOUR", "WITHIN", "ADD_LINK", "")

#run raster calculator to get only groups with Link = 9
arcpy.gp.RasterCalculator_sa("Con(Lookup(\"rgGroup\",\"LINK\") == 9, \"rgGroup\", 0)", "D:/finalData/post_inputs/Link9")

#run raster calc to get only groups with count less than 2000. Each pixel is 0.0144 Km^2. (Vail is 21.40 km^2)
arcpy.gp.RasterCalculator_sa("Con(Lookup(\"Link9\",\"COUNT\")  < 2000, \"Link9\", 0)", "D:/finalData/post_inputs/less2000")

#run raster calc to get only groups with count greater than 416
arcpy.gp.RasterCalculator_sa("Con(Lookup(\"less2000\",\"COUNT\")  > 416, \"less2000\", 0)", "D:/finalData/post_inputs/great416")

#Making the zeros null
arcpy.gp.RasterCalculator_sa("SetNull(\"great416\"==0,\'great416\')", "D:/finalData/post_inputs/lastpart")

#Converting to vector and running the minimum bounding geometry tool
lastpart = "D:/finalData/post_inputs/lastpart"
arcpy.RasterToPolygon_conversion("D:/finalData/post_inputs/lastpart","D:/finalData/vector_data.gdb/unsimp_pgons")

arcpy.MinimumBoundingGeometry_management("D:/finalData/vector_data.gdb/unsimp_pgons", "D:/finalData/vector_data.gdb/potential_areas", "CONVEX_HULL")


import csv
import sys
import pandas as pd


#slope analysis
pot_areas = "D:/finalData/vector_data.gdb/potential_areas"
slope_CO = "D:/finalData/post_inputs/co_slope"
arcpy.sa.ZonalStatisticsAsTable(pot_areas, "Id", slope_CO, "D:/finalData/results/slopestats.dbf")
arcpy.TableToExcel_conversion("D:/finalData/results/slopestats.dbf", "D:/finalData/results/slopestats.xls")

sitesdata = pd.read_excel("D:/finalData/results/slopestats.xls")

#Conducting circularity analysis
Curse = arcpy.da.SearchCursor("D:/finalData/vector_data.gdb/potential_areas", 'SHAPE@')

#Making list of polygons
Pgons = []
for i in range(1,63):
    Points = Curse.next()
    Pgons.append(Points)
    
    
def Perimeter(Pgons):
    Perimeter = 0
    Perimeters = []
    for j in range(len(Pgons)):
    
        for i in range(len(Pgons[j][0][0])-1):
        #    xcoords.append(Pgons[0][0][0][i].X)
        #    ycoords.append(Pgons[0][0][0][i].Y)
            sidelength = sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2)
            Perimeter = Perimeter + sidelength
        Perimeters.append(Perimeter)
        Perimeter = 0
    return(Perimeters)
    
Pot_pers = Perimeter(Pgons)
    
def Area(Pgons):
    TotalArea = 0
    Areas = []
    for j in range(len(Pgons)):
    
        for i in range(len(Pgons[j][0][0])-1):
            Area = (0.5*(Pgons[j][0][0][i+1].X - Pgons[j][0][0][i].X)*(Pgons[j][0][0][i].Y + Pgons[j][0][0][i+1].Y))
            TotalArea = TotalArea + Area
        Areas.append(TotalArea)
        TotalArea = 0
    return(Areas)

Areas = Area(Pgons)

#Making a function for circularity ratio
def Circle(Areas, Perimeters):   
    Circles = []
    for j in range(len(Areas)):
    
        M = (4*(pi)*Areas[j])/(Perimeters[j]**2)
        Circles.append(M)
    return(Circles)

circles = Circle(Areas, Pot_pers)

#Adding the circularity data to the sites data
sitesdata.insert(10, "circles", circles)

sitelist = []
for i in range(len(sitesdata)):
    if sitesdata['RANGE'][i] > 40 and sitesdata['MEAN'][i] > 15 and sitesdata['STD'][i] > 9:
        sitelist.append(sitesdata['Id'][i])
        
#From these final 12 sites, we examined their circularites and chose our final 3 sites!


#import IPython
#app = IPython.Application.instance()
#app.kernel.do_shutdown(True) 