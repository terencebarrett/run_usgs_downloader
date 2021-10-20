# Modified from a script provided by Andrew Lister, based on an example script
#   in the USGSlidar repo

library(rgdal)
library(sf)
library(mapview)
library(RSQLite)
library(dplyr)
library(tidyverse)
library(lubridate)

library(USGSlidar)

# Input parameters
# TODO: Move all other hard-coded parameters in this script to this section
# TODO: Make these into CLI args
state <- "DE"
pipelines <- "pipelines"
clips <- "clips"
clipSize <- 1000 # A square, centered on the point
showMaps <- FALSE  # TODO: True is not currently producing plots

# TODO: Provide for the working folder to be outside the repo, and on a network drive

# TODO: Make sure all aspects of this script can run in parallel with another session of it running

# TODO: Save plots and clips as subdirs of a a time-stamped directory, so multiple
#  searches can be kept, and so the root of the working folder can keep general
#  reference data across runs

# TODO: Generalize all aspects of this script so works for any state, without tweaking

# TODO: Investigate why LiDAR tiles are smaller than expected

# Set working folder based on script location at runtime
initial.options <- commandArgs(trailingOnly = FALSE)
file.arg.name <- "--file="
script.name <- sub(file.arg.name, "", initial.options[grep(file.arg.name, initial.options)])
script.basename <- dirname(script.name)
workingFolder = normalizePath(file.path(script.basename, "working"))
cat("Working directory: ", workingFolder, "\n")
setwd(workingFolder)

# get FIADB for state
FIADBFile <- paste0("FIADB_", state, ".db")

# check to see if file exists
if (!file.exists(FIADBFile)) {
  fetchFile(paste0("https://apps.fs.usda.gov/fia/datamart/Databases/SQLite_FIADB_", state, ".zip"),
            paste0(state, ".zip"))

  # unzip the file
  unzip(zipfile = paste0(state, ".zip"), exdir = getwd())

  if (file.exists(FIADBFile)) {
    file.remove(paste0(state, ".zip"))
  } else {
    # report a problem unzipping the file
    cat("*****Could not unzip file: ", paste0(state, ".zip"), "\n")
  }
}

# connect to FIADB
con <- dbConnect(RSQLite::SQLite(), FIADBFile)

# read tables
PLOT <- dbReadTable(con, "PLOT")
totalPlots <- nrow(PLOT)

# disconnect from database
dbDisconnect(con)

# get plots measured in last ~10 years...could include multiple measurements for some plots
PLOT <- subset(PLOT, MEASYEAR >= 2010)
plotsSince2010 <- nrow(PLOT)

# FIADB locations are LON-LAT...this is OK but I prefer to work in web mercator (EPSG:3857)
# create sf object with locations
pts_sf <- st_as_sf(PLOT,
                   coords = c("LON", "LAT"),
                   remove = FALSE,
                   crs = 4269)

# reproject to web mercator
pts_sf <- st_transform(pts_sf, 3857)

if (showMaps) mapview(pts_sf)

# retrieve the entwine index with metadata
fetchUSGSProjectIndex(type = "entwineplus")

# query the index to get the lidar projects covering the points with 160m circle
# this call returns the project boundaries that contain plots
projects_sf <- queryUSGSProjectIndex(buffer = clipSize / 2, aoi = pts_sf)

# subset the results to drop the KY statewide aggregated point set
# there are a few lidar projects like this where data from several projects
# were aggregated. Unfortunately, the naming isn't consistent so you have to
# know something about the data.
projects_sf <- subset(projects_sf, name != "KY_FullState")

if (showMaps) mapview(projects_sf)

# query the index again to get the point data populated with lidar project information
# this call returns the sample locations (polygons) with lidar project attributes
real_polys_sf <- queryUSGSProjectIndex(buffer = clipSize / 2, aoi = pts_sf, return = "aoi", shape = "square")

# query the index again to get the point data populated with lidar project information
# this call returns the sample locations (points) with lidar project attributes
real_pts_sf <- queryUSGSProjectIndex(buffer = 0, aoi = pts_sf, return = "aoi")

# Manipulate acquisition date information. Ideally, this functionality would be
# part of the USGSlidar package but there is no consistent format (column names)
# for the date information
projects_sf <- subset(projects_sf, !is.na(collect_start) & !is.na(collect_end))
real_polys_sf <- subset(real_polys_sf, !is.na(collect_start) & !is.na(collect_end))
real_pts_sf <- subset(real_pts_sf, !is.na(collect_start) & !is.na(collect_end))

# do the date math to allow filtering of the sample POLYGONS
# this code is specific to the Entwine database structure populated using the PopulateEntwineDB.R code
# column names will be different for other index types.
# build a datetime value for start and end of collection using lubridate functions
real_polys_sf$startdate <- ymd(real_polys_sf$collect_start)
real_polys_sf$enddate <- ymd(real_polys_sf$collect_end)
real_polys_sf$avedate <- real_polys_sf$startdate + ((real_polys_sf$enddate - real_polys_sf$startdate) / 2)
real_polys_sf$measdate <- make_date(real_polys_sf$MEASYEAR, real_polys_sf$MEASMON, real_polys_sf$MEASDAY)

# repeat the date math to allow filtering of the sample POINTS
# build a datetime value for start and end of collection using lubridate functions
real_pts_sf$startdate <- ymd(real_pts_sf$collect_start)
real_pts_sf$enddate <- ymd(real_pts_sf$collect_end)
real_pts_sf$avedate <- real_pts_sf$startdate + ((real_pts_sf$enddate - real_pts_sf$startdate) / 2)
real_pts_sf$measdate <- make_date(real_pts_sf$MEASYEAR, real_pts_sf$MEASMON, real_pts_sf$MEASDAY)

# we only want plots measured within +- some time interval
dateHalfRange <- years(1) + months(6)

# do the date filtering on the POLYGONS
target_polys_sf <- subset(real_polys_sf, (measdate - avedate) >= -dateHalfRange & (measdate - avedate) <= dateHalfRange)

# do the date filtering on the POINTS
target_pts_sf <- subset(real_pts_sf, (measdate - avedate) >= -dateHalfRange & (measdate - avedate) <= dateHalfRange)

if (showMaps) mapview(target_pts_sf)

cat("Total number of plots in FIADB for ", state, ": ", totalPlots, "\r\n",
  "Plots with measurements since 01/01/2010: ", plotsSince2010, "\r\n",
  "   Of these, ", nrow(pts_sf), " have lidar coverage", "\r\n",
  "   Of these, ", nrow(target_pts_sf), " have lidar coverage within 18 months of field measurements", "\r\n"
)

# if we need a list of the lidar projects that cover the final target plot POLYGONS, we need to check to see if
# projects were dropped (because plots did not meet the measurement date requirements)
#
# We can simply subset the original set of projects based on some field from the set of plots that match the
# date criteria.
#
# NOTE: I am not using the project list for anything in this example
target_projects_sf <- subset(projects_sf, name %in% unique(target_polys_sf$name))

# build PDAL pipelines...use template included with library...basic clip with no additional processing
# To output LAS instead of LAZ: compress = FALSE
buildPDALPipelineENTWINE(target_polys_sf,
                         IDColumnLabel = "CN",
                         URLColumnLabel = "url",
                         pipelineOutputFolder = file.path(state, pipelines),
                         pipelineOutputFileBaseName = "Plot",
                         pipelineTemplateFile = "",
                         clipOutputFolder = file.path(state, clips),
                         verbose = 500
)

# build the output file name for clips and add a column to the data before writing to a file
# this is the logic used in buildPDALPipelineENTWINE() to build the output name using the
# values for URLColumnLabel and IDColumnLabel
lasFile <- paste0(basename(dirname(target_polys_sf$url)),
                  "_",
                  target_polys_sf$CN,
                  ".laz"
)

# add the clip file name to data
target_polys_sf$ClipFile <- lasFile

# write off data after dropping geometry
# NOTE: Excel doesn't really like some of the values in the file (CN & dates) so you are better off reading the
# data in R but you need to use the following options for read.csv:
#   stringsAsFactors = FALSE,
#   colClasses = c("CN"="character", "SRV_CN"="character", "CTY_CN"="character", "PREV_PLT_CN"="character")
write.csv(st_drop_geometry(target_polys_sf), paste0(state, "Plots.csv"))


