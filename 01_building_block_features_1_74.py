import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import libpysal
import osmnx as ox
import pandas as pd
import numpy as np
################ building feature engineering ###############  from 1 to 10
#buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)
#buildings['area'] = momepy.Area(buildings).series
#buildings['perimeter'] = momepy.Perimeter(buildings).series
#buildings['circularcompactness'] = momepy.CircularCompactness(buildings).series
#buildings['longestaxislength'] = momepy.LongestAxisLength(buildings).series
#buildings['elongation'] = momepy.Elongation(buildings).series
#buildings['convexity'] = momepy.Convexity(buildings).series
#buildings['orientation'] = momepy.Orientation(buildings).series
#buildings['corners'] = momepy.Corners(buildings).series
#buildings['sharedwall'] = momepy.SharedWalls(buildings).series
#buildings['uID'] = momepy.unique_id(buildings)
#save_repo = 'HD_building_all.geojson'
#buildings.to_file(save_repo, driver='GeoJSON')
#print('successfully save to ' + save_repo)


# from 11-74
buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)
print(buildings.columns)
################ block feature engineering ###############  @zhendong  from 11 to 74
# load blocks generated from 03_generating_blocks.py
blocks = gpd.read_file('blocks/HD_block.shp')
print(blocks.columns)
#blocks['bID_test'] = momepy.unique_id(blocks)
# features from no.11 to no.14
block_tempe = pd.DataFrame()
#11
buildings_count = buildings.groupby('bID')['uID'].count()
block_tempe = pd.DataFrame({'bID':buildings_count.index, 'blockcount':buildings_count.values})

#12
block_tempe['AvBlockFootprintArea'] = buildings.groupby('bID')['area'].mean()
block_tempe['StdBlockFootprintArea'] =buildings.groupby('bID')['area'].std()   # problem here, there are NAs in the dataframe.
block_tempe['BlockTotalFootprintArea']= buildings.groupby('bID')['area'].sum()
print(block_tempe.head())
# need to merge blocks to buildings.
buildings = buildings.merge(block_tempe,how= "left",on="bID")

# features from no.15 to no.20
# step1. features of blocks itself
blocks['BlockPerimeter'] = momepy.Perimeter(blocks).series
blocks['BlockLongestAxisLength'] = momepy.LongestAxisLength(blocks).series
blocks['BlockElongation'] = momepy.Elongation(blocks).series
blocks['BlockConvexity'] = momepy.Convexity(blocks).series
blocks['BlockOrientation'] = momepy.Orientation(blocks).series
blocks['BlockCorners'] = momepy.Corners(blocks).series
# step2. merge blocks to buildings.
buildings = buildings.merge(blocks.iloc[:,np.r_[0,2:8]].copy(),how= "left",on="bID")

blocks['AvBlockFootprintArea'] = block_tempe['AvBlockFootprintArea']
blocks['StdBlockFootprintArea'] =block_tempe['StdBlockFootprintArea']
blocks['BlockTotalFootprintArea']= block_tempe['BlockTotalFootprintArea']
blocks['blockcount']= block_tempe['blockcount']

# save the feature to geojson
save_repo = 'blocks_temp.geojson'
blocks.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)

################ Buildings & blocks within 50 m  ###############  from 21 to 38
building_buffer50 = buildings.copy()
building_buffer50.geometry  = building_buffer50.geometry.buffer(50)
building_buffer50_joined = gpd.sjoin(building_buffer50[['uID','geometry']], blocks,how="left",op="intersects")
building_temp = pd.DataFrame()
#21
BlockOrientation_test = building_buffer50_joined.groupby('uID')['BlockOrientation'].std()
building_temp = pd.DataFrame({'uID':BlockOrientation_test.index, 'std_block_orientation_within_buffer_50':BlockOrientation_test.values})
#22
building_temp['av_block_orientation_within_buffer_50'] = building_buffer50_joined.groupby('uID')['BlockOrientation'].mean()
#23
building_temp['av_block_av_footprint_area_within_buffer_50'] = building_buffer50_joined.groupby('uID')['AvBlockFootprintArea'].mean()
#24
building_temp['std_block_footprint_area_within_buffer_50'] = building_buffer50_joined.groupby('uID')['AvBlockFootprintArea'].std()
#25
building_temp['av_block_footprint_area_within_buffer_50'] = building_buffer50_joined.groupby('uID')['BlockTotalFootprintArea'].mean()
#26
building_temp['std_block_length_within_buffer_50'] = building_buffer50_joined.groupby('uID')['blockcount'].std()
#27
building_temp['av_block_length_within_buffer_50'] = building_buffer50_joined.groupby('uID')['blockcount'].mean()
#28
building_temp['blocks_within_buffer_50'] = building_buffer50_joined.groupby('uID')['bID'].count()

#29 from building to buildings
building_buffer50_joined_buildings = gpd.sjoin(building_buffer50[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer50_joined_buildings.columns)

building_temp['std_orientation_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['orientation'].std()

#30
building_temp['av_orientation_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['orientation'].mean()
#31
building_temp['std_convexity_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['convexity'].std()
#32
building_temp['av_convexity_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['convexity'].mean()
#33
building_temp['std_elongation_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['elongation'].std()
#34
building_temp['av_elongation_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['elongation'].mean()
#35
building_temp['std_footprint_area_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['area'].std()
#36
building_temp['av_footprint_area_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['area'].mean()
#37
building_temp['total_ft_area_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['area'].sum()
#38
building_temp['buildings_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['uID_right'].count()

################ Buildings & blocks within 200 m  ###############  from 39 to 56
building_buffer200 = buildings.copy()
building_buffer200.geometry  = building_buffer200.geometry.buffer(200)
building_buffer200_joined = gpd.sjoin(building_buffer200[['uID','geometry']], blocks,how="left",op="intersects")
#39
building_temp['std_block_orientation_within_buffer_200'] = building_buffer200_joined.groupby('uID')['BlockOrientation'].std()
#40
building_temp['av_block_orientation_within_buffer_200'] = building_buffer200_joined.groupby('uID')['BlockOrientation'].mean()
#41
building_temp['av_block_av_footprint_area_within_buffer_200'] = building_buffer200_joined.groupby('uID')['AvBlockFootprintArea'].mean()
#42
building_temp['std_block_footprint_area_within_buffer_200'] = building_buffer200_joined.groupby('uID')['AvBlockFootprintArea'].std()
#43
building_temp['av_block_footprint_area_within_buffer_200'] = building_buffer200_joined.groupby('uID')['BlockTotalFootprintArea'].mean()
#44
building_temp['std_block_length_within_buffer_200'] = building_buffer200_joined.groupby('uID')['blockcount'].std()
#45
building_temp['av_block_length_within_buffer_200'] = building_buffer200_joined.groupby('uID')['blockcount'].mean()
#46
building_temp['blocks_within_buffer_200'] = building_buffer200_joined.groupby('uID')['bID'].count()


#47 from building to buildings
building_buffer200_joined_buildings = gpd.sjoin(building_buffer200[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer200_joined_buildings.columns)
building_temp['std_orientation_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['orientation'].std()
#48
building_temp['av_orientation_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['orientation'].mean()
#49
building_temp['std_convexity_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['convexity'].std()
#50
building_temp['av_convexity_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['convexity'].mean()
#51
building_temp['std_elongation_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['elongation'].std()
#52
building_temp['av_elongation_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['elongation'].mean()
#53
building_temp['std_footprint_area_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['area'].std()
#54
building_temp['av_footprint_area_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['area'].mean()
#55
building_temp['total_ft_area_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['area'].sum()
#56
building_temp['buildings_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['uID_right'].count()


################ Buildings & blocks within 500 m  ###############  from 57 to 74
building_buffer500 = buildings.copy()
building_buffer500.geometry  = building_buffer500.geometry.buffer(500)
building_buffer500_joined = gpd.sjoin(building_buffer500[['uID','geometry']], blocks,how="left",op="intersects")
#57
building_temp['std_block_orientation_within_buffer_500'] = building_buffer500_joined.groupby('uID')['BlockOrientation'].std()
#58
building_temp['av_block_orientation_within_buffer_500'] = building_buffer500_joined.groupby('uID')['BlockOrientation'].mean()
#59
building_temp['av_block_av_footprint_area_within_buffer_500'] = building_buffer500_joined.groupby('uID')['AvBlockFootprintArea'].mean()
#60
building_temp['std_block_footprint_area_within_buffer_500'] = building_buffer500_joined.groupby('uID')['AvBlockFootprintArea'].std()
#61
building_temp['av_block_footprint_area_within_buffer_500'] = building_buffer500_joined.groupby('uID')['BlockTotalFootprintArea'].mean()
#62
building_temp['std_block_length_within_buffer_500'] = building_buffer500_joined.groupby('uID')['blockcount'].std()
#63
building_temp['av_block_length_within_buffer_500'] = building_buffer500_joined.groupby('uID')['blockcount'].mean()
#64
building_temp['blocks_within_buffer_500'] = building_buffer500_joined.groupby('uID')['bID'].count()


#65 from building to buildings
building_buffer500_joined_buildings = gpd.sjoin(building_buffer500[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer500_joined_buildings.columns)
building_temp['std_orientation_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['orientation'].std()
#66
building_temp['av_orientation_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['orientation'].mean()
#67
building_temp['std_convexity_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['convexity'].std()
#68
building_temp['av_convexity_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['convexity'].mean()
#69
building_temp['std_elongation_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['elongation'].std()
#70
building_temp['av_elongation_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['elongation'].mean()
#71
building_temp['std_footprint_area_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['area'].std()
#72
building_temp['av_footprint_area_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['area'].mean()
#73
building_temp['total_ft_area_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['area'].sum()
#74
building_temp['buildings_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['uID_right'].count()


# merge together
buildings = buildings.merge(building_temp,how= "left",on="uID")

# save the feature to geojson
save_repo = 'HD_building_all_1-74.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)