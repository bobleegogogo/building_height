# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 26.04.2021
# -------------------------------


import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

# download the data
gdf = ox.geometries.geometries_from_place('Heidelberg, Germany', tags={'building': True})
gdf_projected = ox.projection.project_gdf(gdf, to_crs='epsg:3035')

# save to geojson
save_repo = 'HD_building.geojson'
gdf_save = gdf_projected .applymap(lambda x: str(x) if isinstance(x, list) else x) #fiona datatype issue
gdf_save = gdf_save[gdf_save['element_type'] == 'way']
# print(gdf_save.head())
gdf_save = gdf_save[['unique_id', 'osmid', 'geometry', 'nodes']] #charmap issue
gdf_save.drop(labels="nodes", axis=1).to_file(save_repo, driver='GeoJSON') #first node issue
print('successfully save to' + save_repo)

# read to geojson and project to EPSG3035
buildings = gpd.read_file('HD_building.geojson').to_crs(epsg=3035)

# visualize
f, ax = plt.subplots(figsize=(10, 10))
gdf_projected.plot(ax=ax)
ax.set_axis_off()
plt.show()


# first test of momepy
blg_area = momepy.Area(buildings)
buildings['area'] = blg_area.series

f, ax = plt.subplots(figsize=(10, 10))
buildings.plot('area', ax=ax, legend=True, scheme='quantiles', cmap='Blues',
               legend_kwds={'loc': 'lower left'})
ax.set_axis_off()
plt.show()


