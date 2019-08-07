# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:04:38 2019

@author: wike4167
"""

from math import *
import arcpy,os

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


#Making a function for circularity ratio
def Circle(Areas, Perimeters):   
    Circles = []
    for j in range(len(Areas)):
    
        M = (4*(pi)*Areas[j])/(Perimeters[j]**2)
        Circles.append(M)
    return(Circles)

#making a function for what I just did
def area3d(slope, shapefile, zonefield):
    slopey = Raster(slope)
    Araster = slopey * (pi/180)
    area3draster = (Araster.meanCellWidth*(Araster.meanCellWidth/Cos(Araster)))
    area3draster.save('area3draster')
    ZonalStatisticsAsTable(shapefile,zonefield, 'area3draster','AreaTable.dbf', "NODATA", "SUM")
    Cursorobject = [i for i in arcpy.da.SearchCursor('AreaTable.dbf', 'SUM')]
    print 'This tool returns the areas of each polygon in the shapefile'
    yeet = []
    for i in range(len(Cursorobject)):
        yeet.append(Cursorobject[i][0])
    del Cursorobject
    return(yeet)

def Perimeter3d(Pgons):
    P = 0
    Ps = []
    for j in range(len(Pgons)):    
        for i in range(len(Pgons[j][0][0])-1):
            sidelength = sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2 + (Pgons[j][0][0][i].Z-Pgons[j][0][0][i+1].Z)**2)
            P = P + sidelength
        Ps.append(P)
        P = 0
    return(Ps)

def LCAfunction(Pgons, Areas):
#Find the X coords of the centroids
    XLCAss = []
    XLCAs = 0
    for j in range(len(Pgons)):   
        for i in range(len(Pgons[j][0][0])-1):
            part = ((-1/(6*Areas[j])))*(Pgons[j][0][0][i].X + Pgons[j][0][0][i+1].X)*(Pgons[j][0][0][i].X*Pgons[j][0][0][i+1].Y - Pgons[j][0][0][i+1].X*Pgons[j][0][0][i].Y)
            XLCAs = XLCAs + part   
        XLCAss.append(XLCAs)
        XLCAs = 0
        
#Find the Y coords of the centroids
    YLCAss = []
    YLCAs = 0
    for j in range(len(Pgons)):   
        for i in range(len(Pgons[j][0][0])-1):
            part = ((-1/(6*Areas[j])))*(Pgons[j][0][0][i].Y + Pgons[j][0][0][i+1].Y)*(Pgons[j][0][0][i].X*Pgons[j][0][0][i+1].Y - Pgons[j][0][0][i+1].X*Pgons[j][0][0][i].Y)
            YLCAs = YLCAs + part   
        YLCAss.append(YLCAs)
        YLCAs = 0

#find all the z values
    zcoords = [[],[],[],[]]
    for j in range(len(Pgons)):   
        for i in range(len(Pgons[j][0][0])-1):
            zcoords[j].append(Pgons[j][0][0][i].Z)
            

#Find the minimum z values
    MinZvalues = []
    for i in range(len(Pgons)):
        MinZvalues.append(min(zcoords[i]))

#Find the X and Ys at the Minimum Z point.
    MinCoordsx = []
    MinCoordsy = []
    for j in range(len(Pgons)):   
        for i in range(len(Pgons[j][0][0])-1):
            if Pgons[j][0][0][i].Z == MinZvalues[j]:
                MinCoordsx.append((Pgons[j][0][0][i].X))
                MinCoordsy.append((Pgons[j][0][0][i].Y))
    LCAs = []
    for i in range(len(XLCAss)):
        LCAs.append(sqrt((MinCoordsx[i]-XLCAss[i])**2 + (MinCoordsy[i]-YLCAss[i])**2))
    return(LCAs)
    
    
def ReliefR(Pgons):
    zcoords = [[],[],[],[]]
    for j in range(len(Pgons)):   
        for i in range(len(Pgons[j][0][0])-1):
            zcoords[j].append(Pgons[j][0][0][i].Z)
    MinZvalues = []
    for i in range(len(Pgons)):
        MinZvalues.append(min(zcoords[i]))
    maxzcoords = []
    Numerators = []
    for i in range(len(Pgons)):
        maxzcoords.append(max(zcoords[i]))
        Numerators.append((maxzcoords[i]-MinZvalues[i]))
    
    #Calculating the denominator
    dists = [[],[],[],[]]
    for j in range(len(Pgons)):    
        for i in range(len(Pgons[j][0][0])-1):
            dists[j].append(sqrt((Pgons[j][0][0][i].X-Pgons[j][0][0][i+1].X)**2 + (Pgons[j][0][0][i].Y-Pgons[j][0][0][i+1].Y)**2 + (Pgons[j][0][0][i].Z-Pgons[j][0][0][i+1].Z)**2))

    maxdists = []
    for j in range(len(Pgons)):
        maxdists.append(max(dists[j]))
    
    #Calculate relief ratios
    Rratios = []
    for j in range(len(Pgons)):
        Rratios.append((Numerators[j]/maxdists[j]))
    return(Rratios)