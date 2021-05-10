#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:49:11 2021

@author: maxwellkent
"""

#Grouping blocks(County shapefile and Fixed BB) with block groups (Census variables)
import geopandas
import pandas as pd

#Import from last script
fixedproviders= pd.read_csv("fixedroviders_block.csv", )

#Grouping data from fixed providers

#Slice off block 
fixedproviders["blockgroup"]= fixedproviders["blockcode"].astype(str).str[:12]


#Grouping data from fixed providers at the blockgroup level
fixedproviders_grouped= fixedproviders.groupby('blockgroup').agg(
    num_consumerproviders= pd.NamedAgg(column='consumer', aggfunc=sum), 
    mode_tech= pd.NamedAgg(column='techcode_char', aggfunc=lambda x: x.value_counts().index[0]),
    mean_max_down= pd.NamedAgg(column='maxaddown', aggfunc='mean'), 
    max_max_down= pd.NamedAgg(column='maxaddown', aggfunc='max'),
    min_max_down= pd.NamedAgg(column='maxaddown', aggfunc='min'), 
    range_max_down= pd.NamedAgg(column='maxaddown', aggfunc= lambda x: max(x)-min(x)), 
    mean_max_up= pd.NamedAgg(column='maxadup', aggfunc='mean'), 
    max_max_up= pd.NamedAgg(column='maxadup', aggfunc='max'),
    min_max_up= pd.NamedAgg(column='maxadup', aggfunc='min'), 
    range_max_up= pd.NamedAgg(column='maxadup', aggfunc= lambda x: max(x)-min(x))
    )


#Create state, county, tract, block group columns for fixed provider for join with census data and shapefile
fixedproviders_grouped.reset_index(inplace=True)
fixedproviders_grouped["state"]= fixedproviders_grouped['blockgroup'].str[0:2]
fixedproviders_grouped["county"]= fixedproviders_grouped["blockgroup"].str[2:5]
fixedproviders_grouped["tract"]= fixedproviders_grouped["blockgroup"].str[5:11]
fixedproviders_grouped["group"]= fixedproviders_grouped["blockgroup"].str[11:12]



#Reading in ACS Census variables
census_vars= pd.read_csv("censusvariables.csv", 
                         dtype={'state': str, 'county': str,'tract': str, 'block group': str })


#Reading in blockgroup shape file
census_blockgroups = geopandas.read_file("Mapping files/tl_2020_36_bg/tl_2020_36_bg.shp", 
                                         dtype= {'STATEFP': str, 'COUNTYFP': str, 'TRACTCE':str, 'BLKGRPCE': str})

census_blockgroups= census_blockgroups.query("STATEFP== '36' & COUNTYFP== '067'")
census_blockgroups= census_blockgroups.to_crs(epsg=4326)
#
#%%

#merge

merge_blockgroups = pd.merge(census_blockgroups, census_vars,  how='left', 
                             left_on=['STATEFP','COUNTYFP', 'TRACTCE', 'BLKGRPCE'], 
                             right_on = ['state','county', 'tract', 'block group'])


merge_blockgroups= pd.merge(merge_blockgroups, fixedproviders_grouped, how= 'left', 
                            left_on=['STATEFP','COUNTYFP', 'TRACTCE', 'BLKGRPCE'], 
                            right_on = ['state','county', 'tract', 'group'])




#%%

#Doing some grouping by race

merge_blockgroups["perc_black"]= merge_blockgroups['B02009_001E']/merge_blockgroups['B02001_001E']
merge_blockgroups["perc_white"]= merge_blockgroups['B02001_002E']/merge_blockgroups['B02001_001E']
merge_blockgroups["perc_native"]= merge_blockgroups['B02001_005E']/merge_blockgroups['B02001_001E']

#Percent mobile
merge_blockgroups["perc_mobile"]= merge_blockgroups['B19001_001E']/merge_blockgroups['B02001_001E']



#%%

#Send to geopackage
merge_blockgroups.set_index('GEOID', inplace=True)
merge_blockgroups.to_file("blockgroups.gpkg", layer= "merged", driver= "GPKG")


    
    