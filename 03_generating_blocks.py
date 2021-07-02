# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 06.05.2021
# -------------------------------

import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

# load building street and tessilation
buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)
streets = gpd.read_file('HD_street.gpkg', layer='edges').to_crs(epsg=3035)

# preprocess the buildings
buildings = momepy.preprocess(buildings, size=30,
                              compactness=True, islands=True)

# add uID for buildings
# buildings['uID'] = momepy.unique_id(buildings)
limit = momepy.buffered_limit(buildings)

# generate morphological tessellation
tessellation = momepy.Tessellation(buildings, unique_id='uID', limit=limit)
tessellation_gdf = tessellation.tessellation

# # visualize the streets, buildings and tessellation all together
# f, ax = plt.subplots(figsize=(10, 10))
# tessellation.plot(ax=ax, edgecolor='white', linewidth=0.2)
# buildings.plot(ax=ax, color='white', alpha=.5)
# streets.plot(ax=ax, color='black')
# ax.set_axis_off()
# plt.show()


# calculate the blocks
blocks = momepy.Blocks(
    tessellation_gdf, streets, buildings, id_name='bID', unique_id='uID')


# block ID for buildings and tessellation
blocks_gdf = blocks.blocks
buildings['bID'] = blocks.buildings_id
tessellation_gdf['bID'] = blocks.tessellation_id

# save the feature to geojson
save_repo = 'HD_building_all.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)

# save block to geojson
save_repo = 'HD_block.gpkg'
blocks_gdf.to_file(save_repo)

# save tessellation to geojson
save_repo = 'HD_tessellation.gpkg'
tessellation_gdf.to_file(save_repo)


# visualize the block
f, ax = plt.subplots(figsize=(10, 10))
blocks_gdf.plot(ax=ax, edgecolor='white', linewidth=0.5)
buildings.plot(ax=ax, color='white', alpha=.5)
ax.set_axis_off()
plt.show()