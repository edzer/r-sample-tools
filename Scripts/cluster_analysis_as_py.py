# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# cluster_analysis_as_py.py
# Created on: 2015-06-19 16:38:15.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: cluster_analysis_as_py <Input_Point_Features> <Clipping_Dataset> <Output_Uncertancy_Dataset> <Output_Classification_Dataset> <Output_Density_Raster> <Output_Superimposing_Ellipses_Dataset> 
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy

# Load required toolboxes
arcpy.ImportToolbox("Z:/projects/r/example-tools/r-sample-tools/RToolbox.tbx")

# Script arguments
Input_Point_Features = arcpy.GetParameterAsText(0)

Clipping_Dataset = arcpy.GetParameterAsText(1)

Output_Uncertancy_Dataset = arcpy.GetParameterAsText(2)

Output_Classification_Dataset = arcpy.GetParameterAsText(3)
if Output_Classification_Dataset == '#' or not Output_Classification_Dataset:
    Output_Classification_Dataset = "%scratchGDB%\\tmp2_Dissolve_Clip" # provide a default value if unspecified

Output_Density_Raster = arcpy.GetParameterAsText(4)
if Output_Density_Raster == '#' or not Output_Density_Raster:
    Output_Density_Raster = "%scratchGDB%\\dens_raster" # provide a default value if unspecified

Output_Superimposing_Ellipses_Dataset = arcpy.GetParameterAsText(5)

# Local variables:
tmp2 = "%scratchGDB%\\tmp2"
tmp_dis = "%scratchGDB%\\tmp2_Dissolve"
cn_density = "%scratchGDB%\\cn_density"
dens_clip = "%scratchGDB%\\dens_clip"
Output_geostatistical_layer = ""

# Set Geoprocessing environments
arcpy.env.extent = Clipping Dataset

# Process: Cluster Analysis
arcpy.gp.toolbox = "Z:/projects/r/example-tools/r-sample-tools/RToolbox.tbx";
# Warning: the toolbox Z:/projects/r/example-tools/r-sample-tools/RToolbox.tbx DOES NOT have an alias. 
# Please assign this toolbox an alias to avoid tool name collisions
# And replace arcpy.gp.clustering(...) with arcpy.clustering_ALIAS(...)
arcpy.gp.clustering(Input_Point_Features, "", Output_Uncertancy_Dataset, Output_Superimposing_Ellipses_Dataset, cn_density)

# Process: Create Thiessen Polygons
arcpy.CreateThiessenPolygons_analysis(Output_Uncertancy_Dataset, tmp2, "ALL")

# Process: Dissolve
arcpy.Dissolve_management(tmp2, tmp_dis, "cluster", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Clip
arcpy.Clip_analysis(tmp_dis, Clipping_Dataset, Output_Classification_Dataset, "")

# Process: Clip (2)
arcpy.Clip_analysis(cn_density, Clipping_Dataset, dens_clip, "")

# Process: Kernel Interpolation With Barriers
tempEnvironment0 = arcpy.env.extent
arcpy.env.extent = Clipping Dataset
arcpy.KernelInterpolationWithBarriers_ga(dens_clip, "density", Output_geostatistical_layer, Output_Density_Raster, "0.263200383398682", "", "POLYNOMIAL5", "", "1", "50", "PREDICTION")
arcpy.env.extent = tempEnvironment0
