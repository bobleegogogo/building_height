# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 06.05.2021
# -------------------------------

import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox


# load street and buildings
gdf_projected = gpd.read_file('HD_building.geojson').to_crs(epsg=3035)

# prepossessing the building footprints
buildings = momepy.preprocess(gdf_projected, size=30,
                              compactness=True, islands=True)

buildings['uID'] = momepy.unique_id(buildings)
limit = momepy.buffered_limit(buildings)

# generate morphological tessellation
tessellation = momepy.Tessellation(buildings, unique_id='uID', limit=limit)
tessellation_gdf = tessellation.tessellation


# visualize tessellation
f, ax = plt.subplots(figsize=(10, 10))
tessellation_gdf.plot(ax=ax)
buildings.plot(ax=ax, color='white', alpha=.5)
ax.set_axis_off()
plt.show()





