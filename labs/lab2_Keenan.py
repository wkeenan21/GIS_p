'''*********************************************
Author: William Keenan
Date: today
Purpose: Student prototype for lab 2
*********************************************'''

print "Importing variables"
# import necessary modules for the analysis
import arcpy
from arcpy import env

env.workspace = r"D://KeenanLab2/data"
env.overwriteOutput= 1


arcpy.CheckOutExtension("3D") #Check out the extention 3D
print "Declaring variables."
#Declare variables, i.e. existing and new ones you will need
CoordString= ''
CoordString2= []
coords = []
print "*******Part I*********"
print "Reading the textfile."
#Read in the text file information line by line

text = open(r"D:\KeenanLab2\data\route_coords.txt")
for i in range(1,50):
    CoordString2.append(text.readline().strip())
    

print "Creating the lists of x-y coordinate pairs."

for i in range(len(CoordString2)):
    coords.append(CoordString2[i].split(','))
coords.pop(48)

print "Creating a polyline feature class."
#The feature class will be 'empty' at this point
arcpy.CreateFeatureclass_management(env.workspace,'line2.shp','POLYLINE')
arcpy.AddField_management('line2.shp','numPnts','FLOAT')

print "Creating a point object and an array object."     
#The point object will be used to create each of the vertices of the array 
arcpy.CreateFeatureclass_management(env.workspace,'points.shp','POINT')
point = arcpy.CreateObject('point')
array = arcpy.CreateObject('array')
Cursor = arcpy.da.InsertCursor('line2.shp',['SHAPE@'])
for i in range(len(coords)):
    point.X = coords[i][0]
    point.Y = coords[i][1]
    array.add(point)
    
NumberofPoints = len(coords)
arcpy.CalculateField_management('line2.shp', 'numPnts', str(NumberofPoints)) 
Polyline = arcpy.Polyline(array)
Cursor.insertRow([Polyline])
del Cursor


print "*******Part II********"
print "Conducting 3D analysis"
#Extensions, such as 3D analyst and Spatial Analyst must be "Checked Out" to use
arcpy.CheckOutExtension("3D")


print "Creating 3D shape"
#use 2D polyline and DEM to create 3D polyline. Hint: use InterpolateShape_3d function
arcpy.InterpolateShape_3d('dem_lab2', 'line2.shp','3DLine.shp')
print "Adding fields."
#Add fields (numPnts, 2Dlength and 3Dlength) to 3D feature class
arcpy.AddField_management('3dLine.shp', 'length2d','FLOAT')
arcpy.AddField_management('3dLine.shp', 'length3d', 'FLOAT')

print "updating fields"
#use cursor to populate numPnts, 2D and 3D length fieldss
length2D = arcpy.da.SearchCursor('3dLine.shp', 'SHAPE@LENGTH').next()
length2Dbutnotatuple = length2D[0]
arcpy.CalculateField_management('3dLine.shp', 'length2d', length2Dbutnotatuple)

cursor2 = arcpy.da.SearchCursor('3dLine.shp', 'SHAPE@').next()
for geom in cursor2:
    length3D = geom.length3D

zvalues= []
xvalues= []
yvalues= []
for i in range(len(cursor2[0][0])):
    zvalues.append(cursor2[0][0][i].Z)
for i in range(len(cursor2[0][0])):
    yvalues.append(cursor2[0][0][i].Y)
for i in range(len(cursor2[0][0])):
    xvalues.append(cursor2[0][0][i].X)
    
Minz= min(zvalues)
MinIndex=zvalues.index(Minz)

MaxZ=max(zvalues)
MaxIndex=zvalues.index(MaxZ)
print "The 2D length is:", length2D

print "The 3D length is:", length3D

print "The difference is:", length3D - length2Dbutnotatuple

print "The minimum z value is:", Minz, ". Its X,Y coordinates are", xvalues[MinIndex],',',yvalues[MinIndex]
print "The maximum z value is:", MaxZ, ". Its X,Y coordinates are", xvalues[MaxIndex],',',yvalues[MaxIndex]
#print out planar and surface lengths and the difference