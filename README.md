# Mapping-Access-to-Broadband-Prototype-

### Summary and motivating question

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

There will be three deliverables in the form of python scripts: 

1. A script which COLLECTS the following data: 
    a.County/Block Group shp: Downloads county and block group shape files, filtering on Onondaga County and the block groups within it's border.
    b.Mobile Broadband data: Downloads spatial data from the FCC providing download and upload speeds for mobile broadband providers(in this prototype I only use Sprint and Verizon as examples because the size of the files exceeds my storage capabilities).
    c.Fixed Broadband data: Uses an API from the Federal Communication Commission to extract Census-block level data about fixed broadband speed from every available broadband provider. Because of the amount of broadband providers that supply a diversity of consumer types, this only includes observations where the maximum download speed was between 10 mbps and 25 mbps, which represents a typical range for household broadband access. 
    d.Demographic data: Downloads county-level demographic data such as health, education, age, unemployment, and geography from the 2018 American Community Survey five-year API. 
    
2. A script which MANAGES the following data wrangling: 
    - Groups the fixed broadband data into data associated with each county:
        - Download speed: Average, maximum, minimum, and range of download speeds for each block group.
        - Upload speed:Average, maximum, minimum, and range of upload speeds for each block group.
        - Internet providers Number of providers per census block group.
    - Merges the dataframes from 1a, 1c, and 1d of the first deliverable on the county blockgroup.
    - Groups demographic and socio-economic variables together at the county-level.
        - Calculates the percentage of the population that is White, Black, and Native American.
        - Calculates the percentage of the population that makes an income.
        - Calculates the percentage of the income-generating population that makes less than $10,000 per year. Although this was chosen originally as a proxy for low-income, it may have been better to have increased this to $20,000 per year (which would be closer to the federal poverty line for a family of three).

3. A script which ANALYZES by doing the following:
    - Calculates the total area of each census block group in Onondaga County. Although it is capable of determining the area, it is not that understandable as the area used is calculated by GIS and I cannot determine the metric by which area is being displayed.
    - Overlays the mobile broadband shapefile on the County/block group shapefile to determine how much area of each block is covered by that broadband provider. Again, similar to the previous step, it is capable of determining the area, but it is not that understandable as the area used is calculated by GIS and I cannot determine the metric by which area is being displayed. However, it does provide an idea about which block groups have the most coverage.
    - Plots the relationship between demographic statistics of the census block group and the number of fixed broadband providers in the block group.
    - Provides condensed dataframes with the top and bottom five census blocks in terms of number of providers
    - Provides a condensed dataframe with the top and bottom five census blocks in terms of average upload and download speeds.

4. A GIS pacakage which displays: 
    - The relationships between fixed broadband access and mobile broadband access
    - Demographic factors and the relationships those have with broadband access.
    - These maps are then converted into .png images for analyses.
    - I have included six different versions of images that display the various demographic and digital characteristics of Onondaga County.
    
5. Four scatter plots that show the relationship between fixed broadband opportunities and racial/income makeup of the block group.
    
### Instructions

Create a script for collecting (Collect.py)

Downloading necessary files (Shapefiles for geography and mobile providers): 
    -Two of the data sources for repository will need to be downloaded to the local directory. These shapefiles are associated with the data for deliverable 1a and 1b.
    1. Download county/blockgroup shapefiles (Deliverables 1a): 
        - Download the county and block group shapefiles from the Census TIGER/Line web interface: https://www.census.gov/cgi-bin/geo/shapefiles/index.php
        - Filter the shapefiles for STATEFP== 36 and COUNTYFP=='067' into pandas dataframes called on_county and census_blockgroups. This will filter the shapefile to only include Onondaga County and the block groups within it.
    2. Download the shapefiles for mobile broadband (Deliverables 2a):
        - Navigate to the FCC website for downloading the shapefiles for each broadband provider (https://broadbandmap.fcc.gov/#/data-download)
        - The shapefiles are organized in hierarchical order by provider and the type of broadband service provided(4G, LTE, and 5G).
        - My analysis only converts the shapefiles from two of the largest mobile broadband providers, Verizon and Sprint, and only the LTE broadband service provided by these two companies into GeoDataFrames. 
        - Create a bounding box using the .envelope method on the on_county dataframe. From this boundig box series create a geopandas dataframe df. 
        - Now use this bounding box df to filter the mobile broadband geodataframes using the .overlay() method and including the how='intersection' argument. This will filter these national shapefiles to only include the parts of the shapefile that lie within the box surrounding Onondaga County.

API Call (for fixed providers and ACS variables):
    1. Query for fixed broadband providers: 
        - This dataset is organized with every observation representing characteristics for each fixed broadband provider in each census block. Therefore, this is an extremely large dataset.
        - Using the opendata.fcc.gov API, query the observations where blockcode is like '36067' and the maximum download speed is greater then 10 mbps and less than 26 mbps. Again, we do this to limit the broadband strength to include the range at which most individual households consume purchase. 
        - Make this list a pandas dataframe.
       
        Script: 
        client = Socrata("opendata.fcc.gov", "HXxZ7n7Y449hg6DQagESA4Xz7")
        client.timeout = 200
        results = client.get("4kuc-phrr", where= "blockcode like '36067%' AND maxaddown>10 AND maxaddown<26", limit= 100000) 
        
        
    2. Query American Community Survey data for each block group: 
        - Create a csv file with the census variables that you want to observe. This prototype only queries variables associated with basic race and socio-economic indicators. 
        - Query the ACS 5 year survey using the https://api.census.gov/data/2018/acs/acs5 website to get the list of variables in your csv for all block groups in Onondaga county.
        - Once you have a succesful connection and a list of queried variables, create a dataframe with the block group name as the index.

        var_info= pd.read_csv('census_variables.csv')
        var_name= var_info['CensusName'].to_list()
        var_list= ['NAME']+var_name
        var_string= ','.join(var_list)

        #https://api.census.gov/data/2017/acs/acs5/variables.html

        api= 'https://api.census.gov/data/2018/acs/acs5'

        for_clause= 'block group:*' #(block group)
        in_clause= 'state:36 & county:067'
        key_value= "c36a1b25c82686e09f753f4a28732a0a28f95511"

        payload= {'get':var_string, 'for': for_clause, 'in':in_clause, 'key':key_value}
        response= requests.get(api, payload)


Create a script for managing these scripts (manage.py): This script will manipulate and merge together the pandas dataframes we created from the collect.py script.

Manipulation: 
    - Using the fixed providers data set, create summary statistics for each of the variables chosen at the block group level. For my analysis, I look for the total number of broadband providers in each block group. I also analyzed the average, maximum, minimum, and range of upload and download speeds in each block group. 
    - Create a state, county, tract, and group variables in the the fixed providers dataframe by truncating the respective aspects of the 'blockgroup' variable (which is the ACS name for the GEOID)
    - Using the ACS 5 year data set, create summary statistics for the percentage of the population that is in each of the selected racial group and income group. 

Merging datasets: 
    - Merge the three data sets together by left-joining on the county/blockgroup geographic dataframe using the state, county, tract, and blockgroup variables.

Wrangling with the mobile broadband dataset: 
    - This section is for the purpose of attaining the percentage of census block group areas that are covered by the mobile broadband provider shapefiles. 
    - Use the pandas geopandas.overlay() method to create a data frame with the area of the mobile broadband shapefile in each block group. 
    - This should allow you to create two new variables that have the areas associated with Verizon and Sprint in each block group and make new variables in the merged dataframe that was just made in the previous step.
    - After you add these area variables, you can calculate the percentage of the block group area that has LTE mobile broadband access from these two providers.
    

Create a script for analyzing these scripts (analyze.py)
This script will do a couple different things to understand what the data is telling us:

1. Plot the relationship between the number of consumers(y axis) and the various demographic indicators (x-axis) including: 
    - % white
    - % black
    - % native american
    - % pop. with income less than 10k
    
2. Create dataframes that show the names and characteristics for the top and bottom 10 block groups for: 
    - Number of providers that are available in that blockgroup.
    - The mean upload and download speeds for fixed broadband services.
    - The percentage of area covered by mobile broadband providers (Sprint & Verizon).


### Tips









