# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 26.04.2021
# -------------------------------


import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import libpysal
import osmnx as ox
import math
import numpy as np
import pandas as pd

############################  Streets & intersections within 50 m  ############################ from 84-95

buildings = gpd.read_file('HD_building_all_75_83.geojson').to_crs(epsg=3035)
points = gpd.read_file('points_temp.geojson').to_crs(epsg=3035)
building_buffer50 = buildings.copy()
building_buffer50.geometry = building_buffer50.geometry.buffer(50)
building_buffer50_joined_buildings = gpd.sjoin(building_buffer50[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer50_joined_buildings.columns)
building_temp = pd.DataFrame()
#84
building_clossness500_test = building_buffer50_joined_buildings.groupby('uID_left')['closeness500'].mean()
building_temp = pd.DataFrame({'uID':building_clossness500_test.index, 'street_closeness_500_av_inter_buffer_50':building_clossness500_test.values})
#85
building_temp['street_closeness_500_max_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['closeness500'].max()
#86
building_temp['street_betweeness_global_av_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['betweenness'].mean()
#87
building_temp['street_betweeness_global_max_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['betweenness'].max()
#88
building_temp['street_width_std_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['widths_street'].std()
#89
building_temp['street_width_av_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['widths_street'].mean()
#90
building_temp['street_length_total_inter_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#91
building_temp['street_length_std_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['lengths_street'].std()
#92
building_temp['street_length_av_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['lengths_street'].mean()
#93
building_temp['street_length_total_within_buffer_50'] = building_buffer50_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#94  number of intersection
building_buffer50_joined_intersections = gpd.sjoin(building_buffer50[['uID','geometry']], points,how="left",op="intersects")
print(building_buffer50_joined_intersections.columns)
#building_buffer50_joined_intersections_test = building_buffer50_joined_intersections.groupby('uID')['pID'].count()
building_temp['street_length_total_within_buffer_50'] =  building_buffer50_joined_intersections.groupby('uID')['pID'].count()



############################  Streets & intersections within 200 m  ############################ from 96-105
building_buffer200 = buildings.copy()
building_buffer200.geometry = building_buffer200.geometry.buffer(200)
building_buffer200_joined_buildings = gpd.sjoin(building_buffer200[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer200_joined_buildings.columns)
#95
building_temp['street_closeness_500_av_inter_buffer_200']  = building_buffer200_joined_buildings.groupby('uID_left')['closeness500'].mean()
#96
building_temp['street_closeness_500_max_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['closeness500'].max()
#97
building_temp['street_betweeness_global_av_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['betweenness'].mean()
#98
building_temp['street_betweeness_global_max_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['betweenness'].max()
#99
building_temp['street_width_std_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['widths_street'].std()
#100
building_temp['street_width_av_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['widths_street'].mean()
#101
building_temp['street_length_total_inter_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#102
building_temp['street_length_std_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['lengths_street'].std()
#103
building_temp['street_length_av_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['lengths_street'].mean()
#104
building_temp['street_length_total_within_buffer_200'] = building_buffer200_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#105  number of intersection
building_buffer200_joined_intersections = gpd.sjoin(building_buffer200[['uID','geometry']], points,how="left",op="intersects")
print(building_buffer200_joined_intersections.columns)
#building_buffer50_joined_intersections_test = building_buffer50_joined_intersections.groupby('uID')['pID'].count()
building_temp['street_length_total_within_buffer_200'] =  building_buffer200_joined_intersections.groupby('uID')['pID'].count()


############################  Streets & intersections within 500 m  ############################ from 106-
building_buffer500 = buildings.copy()
building_buffer500.geometry = building_buffer500.geometry.buffer(500)
building_buffer500_joined_buildings = gpd.sjoin(building_buffer500[['uID','geometry']], buildings,how="left",op="intersects")
print(building_buffer500_joined_buildings.columns)
#106
building_temp['street_closeness_500_av_inter_buffer_500']  = building_buffer500_joined_buildings.groupby('uID_left')['closeness500'].mean()
#107
building_temp['street_closeness_500_max_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['closeness500'].max()
#108
building_temp['street_betweeness_global_av_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['betweenness'].mean()
#109
building_temp['street_betweeness_global_max_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['betweenness'].max()
#110
building_temp['street_width_std_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['widths_street'].std()
#111
building_temp['street_width_av_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['widths_street'].mean()
#112
building_temp['street_length_total_inter_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#113
building_temp['street_length_std_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['lengths_street'].std()
#114
building_temp['street_length_av_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['lengths_street'].mean()
#115
building_temp['street_length_total_within_buffer_500'] = building_buffer500_joined_buildings.groupby('uID_left')['lengths_street'].sum()
#116  number of intersection
building_buffer500_joined_intersections = gpd.sjoin(building_buffer500[['uID','geometry']], points,how="left",op="intersects")
print(building_buffer500_joined_intersections.columns)
#building_buffer50_joined_intersections_test = building_buffer50_joined_intersections.groupby('uID')['pID'].count()
building_temp['street_length_total_within_buffer_500'] =  building_buffer500_joined_intersections.groupby('uID')['pID'].count()

# merge together
buildings = buildings.merge(building_temp,how= "left",on="uID")

# save the feature to geojson
save_repo = 'HD_building_75_116.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)

# # # query the first object from the Geopandas dataframe
# # print(buildings.loc[1, :])
# # assert 0
#
#
# # visualization
# f, ax = plt.subplots(figsize=(10, 10))
# buildings.plot('area', ax=ax, legend=True, scheme='quantiles', cmap='Blues',
#                legend_kwds={'loc': 'lower left'})
# ax.set_axis_off()
# plt.show()
