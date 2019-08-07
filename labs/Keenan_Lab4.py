'''
author: William Keenan
date: 3/14/2019
purpose: Lab4
'''

#import modules
import arcpy,os
from arcpy import env
arcpy.CheckOutExtension("SPATIAL")
from arcpy.sa import * 


import lab4moduleKeenan

#set env properties
env.workspace = r"D://lab4/data"
env.overwriteOutput = 1

#Defining Stuff
Wsheds = 'watersheds_3d.shp'
Curse = arcpy.da.SearchCursor(Wsheds, 'SHAPE@')
#Making list of polygons
Pgons = []
for i in range(1,5):
    Points = Curse.next()
    Pgons.append(Points)
    
from math import *

##Making a function for 2D perimeter
#def Perimeter(Pgons):
#    Perimeter = 0
#    Perimeters = []
#    for j in range(len(Pgons)):
#    
#        for i in range(len(Pgons[j][0][0])-1):
#        #    xcoords.append(Pgons[0][0][0][i].X)
#        #    ycoords.append(Pgons[0][0][0][i].Y)
#            sidelength = sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2)
#            Perimeter = Perimeter + sidelength
#        Perimeters.append(Perimeter)
#        Perimeter = 0
#    return(Perimeters)
#    
Perimeters = Perimeter(Pgons)

#Making a function for 2D Area
#def Area(Pgons):
#    TotalArea = 0
#    Areas = []
#    for j in range(len(Pgons)):
#    
#        for i in range(len(Pgons[j][0][0])-1):
#            Area = (0.5*(Pgons[j][0][0][i+1].X - Pgons[j][0][0][i].X)*(Pgons[j][0][0][i].Y + Pgons[j][0][0][i+1].Y))
#            TotalArea = TotalArea + Area
#        Areas.append(TotalArea)
#        TotalArea = 0
#    return(Areas)
    
Areas = Area(Pgons)


#Making a function for circularity ratio
#def Circle(Areas, Perimeters):   
#    Circles = []
#    for j in range(len(Areas)):
#    
#        M = (4*(pi)*Areas[j])/(Perimeters[j]**2)
#        Circles.append(M)
#    return(Circles)

Circularities = Circle(Areas, Perimeters)

#Making 3D Area


#Making a slope grid
#slope = arcpy.sa.Slope('demlab4', 'DEGREE')
#slope.save("slopegrid")
#
##convert to radians
#slopeboi = Raster('slopegrid')
#degrees = slopeboi * (pi/180)
#degrees.meanCellWidth
#
##do the math, make 3Darea raster
#area3D = (degrees.meanCellWidth*(degrees.meanCellWidth/Cos(degrees)))
#area3D.save("area3d")
#AreaTable = ZonalStatisticsAsTable('watersheds_3D.shp','Id', 'area3d','AreaTable.dbf', "NODATA", "SUM")

#making a function for what I just did
#def area3d(DEMraster, shapefile, zonefield):
#    slope = arcpy.sa.Slope(DEMraster)
#    radians = slope * (pi/180)
#    area3draster = (radians.meanCellWidth*(degrees.meanCellWidth/Cos(degrees)))
#    area3draster.save('area3draster')
#    ZonalStatisticsAsTable(shapefile,zonefield, 'area3draster','AreaTable.dbf', "NODATA", "SUM")
#    Cursorobject = [i for i in arcpy.da.SearchCursor('AreaTable.dbf', 'SUM')]
#    print 'This tool returns the areas of each polygon in the shapefile'
#    yeet = []
#    for i in range(len(Cursorobject)):
#        yeet.append(Cursorobject[i][0])
#    del Cursorobject
#    return(yeet)
    
#Testing the function
Areas3d = area3d('slopegrid', Wsheds, 'Id')

##3d Perimeter
#
#def Perimeter3d(Pgons):
#    P = 0
#    Ps = []
#    for j in range(len(Pgons)):    
#        for i in range(len(Pgons[j][0][0])-1):
#            sidelength = sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2 + (Pgons[j][0][0][i].Z-Pgons[j][0][0][i+1].Z)**2)
#            P = P + sidelength
#        Ps.append(P)
#        P = 0
#    return(Ps)
#Testing the function
Perimeters3D = Perimeter3d(Pgons)
Circularity3d = Circle(Areas3d, Perimeters3D)



#Part II

##Find the X coords of the centroids
#XLCAss = []
#XLCAs = 0
#for j in range(len(Pgons)):   
#        for i in range(len(Pgons[j][0][0])-1):
#            part = ((-1/(6*Areas[j])))*(Pgons[j][0][0][i].X + Pgons[j][0][0][i+1].X)*(Pgons[j][0][0][i].X*Pgons[j][0][0][i+1].Y - Pgons[j][0][0][i+1].X*Pgons[j][0][0][i].Y)
#            XLCAs = XLCAs + part   
#        XLCAss.append(XLCAs)
#        XLCAs = 0
#        
##Find the Y coords of the centroids
#YLCAss = []
#YLCAs = 0
#for j in range(len(Pgons)):   
#        for i in range(len(Pgons[j][0][0])-1):
#            part = ((-1/(6*Areas[j])))*(Pgons[j][0][0][i].Y + Pgons[j][0][0][i+1].Y)*(Pgons[j][0][0][i].X*Pgons[j][0][0][i+1].Y - Pgons[j][0][0][i+1].X*Pgons[j][0][0][i].Y)
#            YLCAs = YLCAs + part   
#        YLCAss.append(YLCAs)
#        YLCAs = 0
#
##find all the z values
#zcoords = [[],[],[],[]]
#for j in range(len(Pgons)):   
#        for i in range(len(Pgons[j][0][0])-1):
#            zcoords[j].append(Pgons[j][0][0][i].Z)
#            
#
##Find the minimum z values
#MinZvalues = []
#for i in range(len(Pgons)):
#    MinZvalues.append(min(zcoords[i]))
#
##Find the X and Ys at the Minimum Z point.
#MinCoordsx = []
#MinCoordsy = []
#for j in range(len(Pgons)):   
#        for i in range(len(Pgons[j][0][0])-1):
#            if Pgons[j][0][0][i].Z == MinZvalues[j]:
#                MinCoordsx.append((Pgons[j][0][0][i].X))
#                MinCoordsy.append((Pgons[j][0][0][i].Y))
#LCAs = []
#for i in range(len(XLCAss)):
#    LCAs.append(sqrt((MinCoordsx[i]-XLCAss[i])**2 + (MinCoordsy[i]-YLCAss[i])**2))

LCAs = LCAfunction(Pgons, Areas)

##Finding the relief ratio
##Calculating the numerator
#maxzcoords = []
#Numerators = []
#for i in range(len(Pgons)):
#    maxzcoords.append(max(zcoords[i]))
#    Numerators.append((maxzcoords[i]-MinZvalues[i]))
#    
##Calculating the denominator
#dists = [[],[],[],[]]
#for j in range(len(Pgons)):    
#    for i in range(len(Pgons[j][0][0])-1):
#        dists[j].append(sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2 + (Pgons[j][0][0][i].Z-Pgons[j][0][0][i+1].Z)**2))
#
#maxdists = []
#for j in range(len(Pgons)):
#    maxdists.append(max(dists[j]))
#    
##Calculate relief ratios
#Rratios = []
#for j in range(len(Pgons)):
#    Rratios.append((Numerators[j]/maxdists[j]))
    
Rratios = ReliefR(Pgons)
    
#Calculate the fields??? Why is this the hardest part???
arcpy.AddField_management('watersheds_3D.shp', 'Circul2D', 'FLOAT')
arcpy.AddField_management('watersheds_3D.shp', 'Circul3D', 'FLOAT')
arcpy.AddField_management('watersheds_3D.shp', 'Rratios', 'FLOAT')
arcpy.AddField_management('watersheds_3D.shp', 'LCAs', 'FLOAT')

cursor = arcpy.da.UpdateCursor('watersheds_3D.shp', ['Circul2D','Circul3d', 'Rratios', 'LCAs' ])

i = 0
for row in cursor:
    row[0] = Circularities[i]
    row[1] = Circularity3d[i]
    row[2] = Rratios[i]
    row[3] = LCAs[i]
    i += 1
    cursor.updateRow(row)

del row
del cursor

print 'The 2D Circularities:'  , Circularities
print 'The 3D Circularites:' , Circularity3d
print 'The 3D circularities are all slightly higher than the 2D ones.'
print 'LCAs:' , LCAs
print 'Area and 3D area:', Areas , Areas3d
print 'Perimeter and 3D perimeter', Perimeters, Perimeters3D
print 'Relief Ratios:' , Rratios
