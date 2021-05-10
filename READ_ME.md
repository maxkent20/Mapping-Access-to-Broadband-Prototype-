#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:53:34 2021

@author: maxwellkent
"""

### Summary

During the 2020 Presidential campaign, the Biden Aministration stressed the 
importance of increasing the availability and accesibility of reliable broadband
service to communities across the country. This all came to fruision when President
Biden announced his Build Back Better agenda, which includes substantial policy 
targeting the Covid-19 pandemic, the economy, and American households. 

The American Job Plan, which is currently undergoing substantial debate in both 
chambers of Congress, targets labor and capitol aspects of the economy such as 
jobs and infrastructure. One major component of the plan is the attempt to "bring affordable, reliable, 
high-speed broadband to every American,including the more than 35 percent of rural 
Americans who lack access to broadband at minimally acceptable speeds." Financially, 
this includes a $100 billion investment in to ensure every American has access 
to broadband access in the next eight years.

The Biden Administration has illuded to the prioritization of 
the plans funding to be allocated towards broadband in rural and low-income areas.
However, this still creates major policy challenges in deciding which communities 
are most in need of fast, reliable, and affordable broadband access. 

This analysis will attempt to provide a better understanding around which American communities
face the least amount of fixed broadband options, as well as the geographic, socio-economic, and 
technological factors that may be driving a greater divide between those with and without
access to broadband.

Sources: https://www.whitehouse.gov/american-jobs-plan/

### Delivarables

There will be a few deliverables: 

-A script which collects the following data: 
    -Uses an API from the Federal Communication Commission to extract Census-block level 
    data about fixed broadband speed from every Broadband provider.
    -Downloads spatial data from the FCC providing download and upload speeds for mobile 
    broadband providers. I am only including the major providers because these are often 
    the most capable of mass-production and have the greatest amount of access to reliable 
    broadband. 
    -Downloads county-level data about broadband access as well as socio-economic indicators 
    such as health, education, age, unemployment, and geography
    
-A script which performs the following data wrangling: 
    -Groups the fixed broadband data into data associated with each county:
        -Broadband accesibility: Percentage of population with fixed access to the Internet at speeds of 25 megabits per second (mbps) download and 3 mbps upload or higher
        -Rural Access: Percentage of rural population in a county with fixed access to the Internet at speeds of 25 megabits per second (mbps) download and 3 mbps upload or higher
        -Internet Adoption:	The number of residential fixed connections to the Internet over 200 kilobits per second (kbps) per 1000 households (as a percentage)
        -Download speed: Average, maximum, minimum download speeds for each county
        -Upload speed:Average, maximum, minimum upload speeds for each county
        -Internet providers Number of providers per county and state
    -Measure mobile broadband use in each county. 
        -Use QGIS to report how many of the major companies provide mobile services in that county
        high speed upload or download services 
        -Examine the range of upload speeds per county
        -Examine the range of download speeds for each county
    -Groups demographic and socio-economic variables together at the county-level.
        -Health, Race, Income, Employment, geography

-A script which analyses.
  -Disparities between fixed and mobile broadband 
  -Trends between fixed broadband and the demographic areas. 
  -
        
        
    
### Instructions

### Tips



 
