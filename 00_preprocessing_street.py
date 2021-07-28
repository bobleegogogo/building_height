# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 05.05.2021
# -------------------------------


import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

# download the data
gdf = ox.graph_from_place('Heidelberg, Germany', network_type='drive')
gdf_projected = ox.project_graph(gdf, to_crs='epsg:3035')
# show the street network with nodes and edges
ox.plot_graph(gdf_projected)

# save to geopackage
save_repo = 'HD_street.gpkg'
ox.save_graph_geopackage(gdf_projected, filepath=save_repo)
print('successfully save to' + save_repo)
#
# read to geopackage and project to EPSG3035
gdf_projected = gpd.read_file('HD_street.gpkg').to_crs(epsg=3035)
# ox.plot_graph(gdf_projected)

# first test of momepy
edges = ox.graph_to_gdfs(gdf_projected, nodes=False, edges=True,
                         node_geometry=False, fill_edge_geometry=True)

# # plot the edges
# f, ax = plt.subplots(figsize=(10, 10))
# edges.plot(ax=ax, color='pink')
# ax.set_axis_off()
# plt.show()

################ feature engineering ###############
# add street features
edg_lin = momepy.Linearity(edges)
edges['linearity'] = edg_lin.series

# show the results
f, ax = plt.subplots(figsize=(10, 10))
edges.plot(ax=ax, column='linearity', legend=True, cmap='coolwarm_r', scheme='quantiles', k=4)
ax.set_axis_off()
plt.show()
