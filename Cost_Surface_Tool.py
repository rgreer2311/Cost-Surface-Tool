import arcpy
from arcpy import env
from arcpy.sa import *

# Set workspace environment
env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

# Declare Variables
Roads = arcpy.GetParameterAsText(1)
MaskIn = arcpy.GetParameterAsText(2)
Elevation = arcpy.GetParameterAsText(3)
ccSpd = arcpy.GetParameterAsText(4)
spdTime = arcpy.GetParameterAsText(5)


  
try:
    # Convert vector road file to raster
    arcpy.FeatureToRaster_conversion("Roads", "Speed.Speed", "RasRoad", 30)
    arcpy.AddMessage("Rasterized road file created.")

    # Terrain mask input feature
    Mask = SetNull(MaskIn, 1, "Value > 0")

    # Create temporary mask feature
    arcpy.MakeRasterLayer_management(Mask, "MaskFeature")

    # Set environmental variable mask to input feature
    arcpy.env.mask = "MaskFeature"

    # Set off road values to a mph default
    OffRoad = Con(IsNull("RasRoad"), float(ccSpd), "RasRoad")
    arcpy.AddMessage("Off road speed set to " + str(ccSpd) + " mph.")

    # Calculate Slope
    ElevSlope = Slope(Elevation, "DEGREE", 1)
    arcpy.AddMessage("Slope created from elevation.")

    # Adjust off road speed by slope
    ModOffRoad = Con(OffRoad == float(ccSpd), (float(ccSpd) / ElevSlope), OffRoad)
    arcpy.AddMessage("Off road speed adjusted for slope.")

    # Create final cost surface. Convert speed to time
    TravelCost = (1.0 / (ModOffRoad * float(spdTime)))
    TravelCost.save("TravelCost")

    arcpy.AddMessage("Cost surface created successfully!")

except:
    #Report Error Message
    print "There was an error creating the cost surface."
    arcpy.AddMessage(arcpy.GetMessage(2))


Tags
