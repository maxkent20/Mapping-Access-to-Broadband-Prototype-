#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 12:02:58 2021

@author: maxwellkent
"""

import geopandas 
import pandas as pd
from shapely.geometry import LineString
import matplotlib.pyplot as mtplt


Merged= geopandas.read_file("Merged.gpkg", layer= "merged")
merged_df= pd.DataFrame(Merged)

#plotting percentage of population (white) against the number of fixed providers in the block group

mtplt.figure()
ax= merged_df.plot.scatter("perc_white", "num_consumerproviders")
ax.set_title("Consumer Providers and White Pop. in Block Group Population")
ax.figure.savefig("providers_white.png", dpi= 300)

#plotting percentage of population (bloack) against the number of fixed providers in the block group

mtplt.figure()
ax= merged_df.plot.scatter("perc_black", "num_consumerproviders")
ax.set_title("Consumer Providers and Black Pop. in Block Group Population")
ax.figure.savefig("providers_black.png", dpi= 300)

#plotting percentage of population (native american) against the number of fixed providers in the block group

mtplt.figure()
ax= merged_df.plot.scatter("perc_native", "num_consumerproviders")
ax.set_title("Consumer Providers and Native American Pop. in Block Group")
ax.figure.savefig("providers_native.png", dpi= 300)

#plotting percentage of population that earns below 10k against the number of fixed providers in the block group

mtplt.figure()
ax= merged_df.plot.scatter("perc_below10", "num_consumerproviders")
ax.set_title("Percentage of population under 10k in block group")
ax.figure.savefig("providers_10below.png", dpi= 300)


#%%
#Listing the top five communities with providers and their demographics
print(merged_df.columns.values)

merged_cut= merged_df[['NAME', 'perc_black','perc_white', 'perc_native', 
                       'perc_income', 'perc_mobile', 'perc_below10', 'num_consumerproviders',
                       'mode_tech', 'mean_max_down', 'mean_max_up', 'perc_sprint', 'perc_verizon']]

#create a dataframe with the top and bottom five block groups based on number of providers
providers_top= pd.DataFrame(merged_cut.nlargest(10,['num_consumerproviders']))
providers_last= pd.DataFrame(merged_cut.nsmallest(10,['num_consumerproviders']))

#create a dataframe with the top and bottom five block groups based on the mean maximum upload and download speed 
meanupdown_last= pd.DataFrame(merged_cut.nsmallest(10,['mean_max_down', 'mean_max_up']))
mean_up_down_top= pd.DataFrame(merged_cut.nlargest(10,['mean_max_down', 'mean_max_up']))

#create a dataframe with the communities with the best and worst mobile broadband access
mobile_top= pd.DataFrame(merged_cut.nlargest(10,['perc_sprint', 'perc_verizon']))
mobile_bottom= pd.DataFrame(merged_cut.nsmallest(10,['perc_sprint', 'perc_verizon']))


