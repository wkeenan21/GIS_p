# -*- coding: utf-8 -*-

#William Keenan
#Lab 3

#Doin the regular stuff at the beggining'
import arcpy
from arcpy import env
env.workspace = r"D://Keenan_Lab3/data"
env.overwriteOutput= 1
theme = 'interestAreas.shp'


#Step 1. Make a list of the Polygons
Polygons=[]
P1cursor = arcpy.da.SearchCursor(theme,["SHAPE@",'FID'])
for i in P1cursor:
    Polygons.append(i[0])
#Create my shp
arcpy.CreateFeatureclass_management(env.workspace, 'P1.shp', 'POINT')

#Define my function for Part II
meshsizes = [2000, 3500, 4500]
def BoxOfPointsMaker(YourBoxOfPoints, XRange, YRange, meshsize=2000):
    '''This function makes a box of points given a shapefile, an xrange, a yrange
    and a meshsize. Default mesh size is 2000. When you run the function,
    your shapefile will be filled with a bunch of points shaped like a square defined
    by your x and y ranges. It is the most useful 
    function of all time.'''
    cursorPnt = arcpy.da.InsertCursor(YourBoxOfPoints, ['SHAPE@'])
    xCoords = []
    for j in range(int(xrange/meshsizes[i])):
        xCoords.append(Xmin + meshsizes[i]*j)
    ycoords = []
    for j in range(int(yrange/meshsizes[i])):
        ycoords.append(Ymin + meshsizes[i]*j)
    point = arcpy.CreateObject('point')
    for g in range(len(xCoords)):
        point.X = xCoords[g]
        for g in range(len(ycoords)):
            point.Y = ycoords[g]          
            cursorPnt.insertRow([point])
    del cursorPnt
    
#Step 2: Use the function to make boxes of points!!
for i in range(len(Polygons)):
    #Making Extents
    Xmax = Polygons[i].extent.XMax
    Ymin = Polygons[i].extent.YMin
    Ymax = Polygons[i].extent.YMax
    Xmin = Polygons[i].extent.XMin
    #Making Ranges
    xrange = Xmax - Xmin
    yrange = Ymax - Ymin  
    #Making Boxes
    BoxOfPointsMaker('P1.shp', xrange, yrange, meshsizes[i])

 
#This makes the buffer and the clip for the
arcpy.Buffer_analysis('P1.shp', 'P1Buffer.shp', 500)
arcpy.Clip_analysis('interestAreas.shp', 'P1Buffer.shp', 'P1Clip.shp')

#Making Square Buffers
arcpy.CreateFeatureclass_management(env.workspace, 'P2.shp', 'POLYGON')

MyArray = arcpy.CreateObject('Array')
Point = arcpy.CreateObject("point")
InsertBoi = arcpy.da.InsertCursor('P2.shp', ['SHAPE@'])
SearchBoi =  arcpy.da.SearchCursor('P1.shp',["SHAPE@"])
for i in SearchBoi:
    MyArray = arcpy.CreateObject('Array')
    Point.X = SearchBoi[0][0].X + 500
    Point.Y = SearchBoi[0][0].Y + 500
    MyArray.add(Point)
    
    Point.X = SearchBoi[0][0].X - 500
    Point.Y = SearchBoi[0][0].Y + 500
    MyArray.add(Point)
    
    Point.X = SearchBoi[0][0].X - 500
    Point.Y = SearchBoi[0][0].Y - 500
    MyArray.add(Point)
    
    Point.X = SearchBoi[0][0].X + 500
    Point.Y = SearchBoi[0][0].Y - 500
    MyArray.add(Point)
    
    NewPoly = arcpy.Polygon(MyArray)    
    InsertBoi.insertRow([NewPoly])
del InsertBoi

#This makes the zonal statistics. If you wanted to find the statistics of the square buffers,
#change the input file to "P2.shp"
arcpy.CheckOutExtension("SPATIAL")
ZonalStats = arcpy.sa.ZonalStatisticsAsTable("P1Clip.shp", "ID", "agr1992", "1992.dbf", "DATA", "MEAN")
ZonalStats = arcpy.sa.ZonalStatisticsAsTable("P1Clip.shp", "ID", "agr2001", "2001.dbf", "DATA", "MEAN")

# Step 6 Printing the Means
Mean = [i for i in arcpy.da.SearchCursor('1992.dbf', 'MEAN')]
Mean2 = [i for i in arcpy.da.SearchCursor('2001.dbf', 'MEAN')]
print 'Agricultural intensity means in 1992 are:'
print 'Polygon 1 mean is', Mean[0][0]
print 'Polygon 2 mean is', Mean[1][0]
print 'Polygon 3 mean is', Mean[2][0]

print 'Agricultural intensity means in 2001 are:'
print 'Polygon 1 mean is', Mean2[0][0]
print 'Polygon 2 mean is', Mean2[1][0]
print 'Polygon 3 mean is', Mean2[2][0]




##this big loop makes the dots. It is the code I used to make the BoxOfPointsMaker. I want
    # to save it so I'm leaving it here.
#for i in range(len(Polygons)):
#    #Making Extents
#    Xmax = Polygons[i].extent.XMax
#    Ymin = Polygons[i].extent.YMin
#    Ymax = Polygons[i].extent.YMax
#    Xmin = Polygons[i].extent.XMin
#    #Making Ranges
#    xrange = Xmax - Xmin
#    yrange = Ymax - Ymin
#    #Creating Cursors
#    cursorPnt = arcpy.da.InsertCursor('P1.shp', ['SHAPE@'], )
#   # xCoords = []
#    for j in range(int(xrange/meshsizes[i])):
#        xCoords.append(Xmin + meshsizes[i]*j)
#
#    #ycoords = []
#    for j in range(int(yrange/meshsizes[i])):
#        ycoords.append(Ymin + meshsizes[i]*j)
#    point = arcpy.CreateObject('point')
#    for g in range(len(xCoords)):
#        point.X = xCoords[g]
#        for g in range(len(ycoords)):
#            point.Y = ycoords[g]          
#            #cursorPnt.insertRow([point])
#
#del cursorPnt
    
    
