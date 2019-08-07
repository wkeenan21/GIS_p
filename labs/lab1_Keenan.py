# GIS 3
# Lab 1 student prototype

#import the modules needed
import arcpy
from arcpy import env
#set workspace

env.workspace = r'D:\Ex1keenan\lab1\data'
env.overwriteOutput = 1
#create your list of year values
year=range(1972, 1979,1)
Soil_sample = 'soil_sample.shp'
print 'Creating iterable of years'

#buffer soil sample feature class
#fty=arcpy.da.SearchCursor('clipforestArea_1972.shp', "SHAPE@AREA").next()

arcpy.Buffer_analysis('soil_sample.shp', 'sample_buffer.shp', 500)
print 'Buffering soil layer'

#create search cursor for soil_sample.shp
cursor = arcpy.da.SearchCursor('soil_sample.shp', "SHAPE@AREA")
print 'Opening search cursor on soil layer'
forests= arcpy.ListFiles('*forest'+'*.shp')


#loop through each year of analysis
#fill in the blank:
for i in range(len(year)):
    #dynamically declare variables that you will need
    print "Declaring variables needed for year",year

    #add a field "data_year" to the forest table
    print "Adding year field to"
   
    #arcpy.AddField_management(forests[i],'data_year', 'SHORT')
    #calculate the field "data_year"
    print "Calculating year field of"
    arcpy.CalculateField_management(forests[i],'data_year', str(year[i]))
    #clip the forest polygon to the buffered soil sample point
    print "Clipping: forests to buffered point"
    arcpy.Clip_analysis(forests[i],'sample_buffer.shp', 'clip'+forests[i])
    forestclips= arcpy.ListFiles('*clipforest'+'*.shp')
    #add needed fields to the result of the clip operation
    print "Adding fields to forest clips"
    arcpy.AddField_management(forestclips[i], 'for_area', 'FLOAT')
    
    #get area from the clipped forest polygon theme
    print "Getting the forest area for the year"
    
    cursorboi=arcpy.da.SearchCursor(forestclips[i], "SHAPE@AREA").next()
    area=cursorboi[0]
    #populate the for_area field with the area retrieved
    print "Calculating the for_area field"
    arcpy.CalculateField_management(forestclips[i], 'for_area', area)
    
    #get the soil result for the corresponding year
    print "Getting soil result from"
    arcpy.AddField_management(forestclips[i], 'soil_smp', 'FLOAT')
    #populate the "soil_smp" field in the clipped theme
    print "Calculating 'soil_smp' field of"
    soilcursor=arcpy.da.SearchCursor('soil_sample.shp', 'year'+str(year[i])).next()
    soilstat=soilcursor[0]
    arcpy.CalculateField_management(forestclips[i], 'soil_smp', soilstat)
    #print values of forest area and soil sample
    print "The forest area in",year[i],"was",cursorboi,"and the soil \
    measurement was",soilstat
    #this prototype provides you with intuitive names for all of these variables
    #if you use different variable names, you will need to change the print
    #statements.