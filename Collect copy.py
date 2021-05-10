#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:12:50 2021

@author: maxwellkent
"""

#This file is for reading in and finding data sources

#Importing the Shapefile for Onondaga County for making a bounding box

import geopandas 

county = geopandas.read_file("Mapping files/cb_2018_us_county_20m/cb_2018_us_county_20m.shp")

#Filter the county to Onondaga county

on_county= county.query("STATEFP== '36' & COUNTYFP== '067'")

on_border= on_county["geometry"]

#Importing the census tracts

#census_blockgroups = geopandas.read_file("Mapping files/tl_2020_36_bg/tl_2020_36_bg.shp", dtype= {'TRACTCE':str})

#Filtering only to tracts in Onondaga County

#census_blockgroups= census_blockgroups.query("STATEFP== '36' & COUNTYFP== '067'")

#Filtering only to 
pro_county= on_county.to_crs(epsg=4326)
#pro_blockgroups= census_blockgroups.to_crs(epsg=4326)

pro_county.to_file("onondaga.gpkg", layer= "county", driver= "GPKG")

#census_blockgroups.to_csv("blockgroups.csv")
#pro_blockgroups.to_file("onondaga.gpkg", layer= "blockgroups", driver= "GPKG")


#%%
#Importing Mobile Broadband access

#Building a bounding box using GeoPandas Envelope method

bounding_box = on_county.envelope
df = geopandas.GeoDataFrame(geopandas.GeoSeries(bounding_box), columns=['geometry'])
df= df.to_crs(epsg=4326)

#Importing for Verizon, Sprint, T-Mobile, ATT, and U.S. Cellular


#Use this geographic parameter to limit how much of these files we are uploading. This saves time for importing large shapefiles and converting them to dataframes. 
print(on_border.total_bounds)
bbox=(-76.491941,  42.771257, -75.896079,  43.268473)


#Verizon
Verizon_LTE= geopandas.GeoDataFrame.from_file("Zipped Mobile Provider Data/F477_2019_12_Broadband_VerizonWireless/F477_2019_12_Broadband_VerizonWireless_83_267195/VZW_LTE_AWS1.shp", bbox= bbox)
Verizon_LTE= Verizon_LTE.to_crs(epsg=4326)
Verizon_LTE = geopandas.overlay(df, Verizon_LTE, how='intersection')
Verizon_LTE.to_file("Verizon.gpkg", layer= "Verizon_LTE", driver= "GPKG")

#Sprint
Sprint_LTE= geopandas.read_file("Zipped Mobile Provider Data/F477_2019_12_Broadband_Sprint/F477_2019_12_Broadband_Sprint_83_268336/Sprint_LTE.SHP", bbox= bbox)
Sprint_LTE= Sprint_LTE.to_crs(epsg=4326)
Sprint_LTE = geopandas.overlay(df, Sprint_LTE, how='intersection')
Sprint_LTE.to_file("Sprint.gpkg", layer= "Sprint_LTE", driver= "GPKG")





#%%

#Importing fixed Broadband providers by blockcode through API 

import pandas as pd
from sodapy import Socrata

client = Socrata("opendata.fcc.gov", "HXxZ7n7Y449hg6DQagESA4Xz7")

client.timeout = 200
# First 2000 results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
#filtering results on those blocks in Onondaga County and where download speed is greater than 10Mbps
 

results = client.get("4kuc-phrr", where= "blockcode like '36067%' AND maxaddown>10 AND maxaddown<26", limit= 100000) 

# Convert to pandas DataFrame
fixedproviders_df = pd.DataFrame.from_records(results)
fixedproviders_df.to_csv("fixedroviders_block.csv")


#%%


# Importing Census information through Census information

import requests
import pandas as pd
   
#Import CSV with list of variables
var_info= pd.read_csv('census_variables.csv')
var_name= var_info['Name'].to_list()
var_list= ['NAME']+var_name
var_string= ','.join(var_list)

#https://api.census.gov/data/2017/acs/acs5/variables.html

api= 'https://api.census.gov/data/2018/acs/acs5'

for_clause= 'block group:*' #(block group)
in_clause= 'state:36 & county:067'
key_value= "c36a1b25c82686e09f753f4a28732a0a28f95511"

payload= {'get':var_string, 'for': for_clause, 'in':in_clause, 'key':key_value}
response= requests.get(api, payload)


if response.status_code== 200:
    print("Success!")
else:
    print(response.status_code)
    print(response.text)
    assert False

row_list= response.json()
print(row_list)

colnames= row_list[0]
datarows= row_list[1:]

census_df= pd.DataFrame(columns=colnames, data=datarows)
census_df=census_df.set_index("NAME")
census_df.to_csv("censusvariables.csv")






