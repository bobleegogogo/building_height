import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import libpysal
import osmnx as ox
import pandas as pd
import numpy as np


################ street-based block, own block feature engineering ###############  @zhendong  from 117 to 136
# load blocks generated from 03_generating_blocks.py
blocks = gpd.read_file('blocks_temp.geojson').to_crs(epsg=3035)
print(blocks.columns)

#117
blocks['street_based_block_phi'] = momepy.CircularCompactness(blocks).series  # Anisotropy index ???
#118
blocks['street_based_block_area'] = momepy.Area(blocks).series

# read buildings.
buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)
################ Street-based blocks within 50 m ###############
building_buffer50 = buildings.copy()
building_buffer50.geometry  = building_buffer50.geometry.buffer(50)
building_buffer50_joined = gpd.sjoin(building_buffer50[['uID','geometry']], blocks,how="left",op="intersects")
building_temp = pd.DataFrame()
# 119
BlockOrientation_test = building_buffer50_joined.groupby('uID')['BlockOrientation'].std()
building_temp = pd.DataFrame({'uID':BlockOrientation_test.index, 'street_based_block_std_orientation_inter_buffer_50':BlockOrientation_test.values})
# 120
building_temp['street_based_block_std_phi_inter_buffer_50'] = building_buffer50_joined.groupby('uID')['street_based_block_phi'].std()
# 121
building_temp['street_based_block_av_phi_inter_buffer_50'] = building_buffer50_joined.groupby('uID')['street_based_block_phi'].mean()
# 122
building_temp['street_based_block_std_area_inter_buffer_50'] = building_buffer50_joined.groupby('uID')['street_based_block_area'].std()
# 123
building_temp['street_based_block_av_area_inter_buffer_50'] = building_buffer50_joined.groupby('uID')['street_based_block_area'].mean()
# 124
building_temp['street_based_block_number_inter_buffer_50'] = building_buffer50_joined.groupby('uID')['bID'].count()  ## which is the unique id for block?

################ Street-based blocks within 200 m ###############
building_buffer200 = buildings.copy()
building_buffer200.geometry  = building_buffer200.geometry.buffer(200)
building_buffer200_joined = gpd.sjoin(building_buffer200[['uID','geometry']], blocks,how="left",op="intersects")
# 125
building_temp['street_based_block_std_orientation_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['BlockOrientation'].std()
# 126
building_temp['street_based_block_std_phi_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['street_based_block_phi'].std()
# 127
building_temp['street_based_block_av_phi_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['street_based_block_phi'].mean()
# 128
building_temp['street_based_block_std_area_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['street_based_block_area'].std()
# 129
building_temp['street_based_block_av_area_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['street_based_block_area'].mean()
# 130
building_temp['street_based_block_number_inter_buffer_200'] = building_buffer200_joined.groupby('uID')['bID'].count()  ## which is the unique id for block?

################ Street-based blocks within 500 m ###############
building_buffer500 = buildings.copy()
building_buffer500.geometry  = building_buffer500.geometry.buffer(200)
building_buffer500_joined = gpd.sjoin(building_buffer500[['uID','geometry']], blocks,how="left",op="intersects")
# 131
building_temp['street_based_block_std_orientation_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['BlockOrientation'].std()
# 132
building_temp['street_based_block_std_phi_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['street_based_block_phi'].std()
# 133
building_temp['street_based_block_av_phi_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['street_based_block_phi'].mean()
# 134
building_temp['street_based_block_std_area_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['street_based_block_area'].std()
# 135
building_temp['street_based_block_av_area_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['street_based_block_area'].mean()
# 136
building_temp['street_based_block_number_inter_buffer_500'] = building_buffer500_joined.groupby('uID')['bID'].count()  ## which is the unique id for block?

# merge together
buildings = buildings.merge(building_temp,how= "left",on="uID")
print(buildings.columns)
# save the feature to geojson
save_repo = 'HD_building_117_136.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)