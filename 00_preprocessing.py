# -------------------------------
# author: Hao Li, hao.li@uni-heidelberg.de
# data: 26.04.2021
# -------------------------------


import momepy
import geopandas as gpd
import matplotlib.pyplot as plt
import libpysal
import osmnx as ox

# # download the data
# gdf = ox.geometries.geometries_from_place('Heidelberg, Germany', tags={'building': True})
# gdf_projected = ox.projection.project_gdf(gdf, to_crs='epsg:3035')
#

# read to geojson and project to EPSG3035
buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)


#
# # # save to geojson
# save_repo = 'HD_building_all.geojson'
# gdf_save = gdf_projected .applymap(lambda x: str(x) if isinstance(x, list) else x) #fiona datatype issue
# # gdf_save = gdf_save[gdf_save['element_type'] == 'way' or 'relation']
# # print(gdf_save.head())
# gdf_save = gdf_save[['@osmId', 'geometry']] #charmap issue
# gdf_save.to_file(save_repo, driver='GeoJSON') #first node issue
# # gdf_save.drop(labels="nodes", axis=1).to_file(save_repo, driver='GeoJSON') #first node issue
# print('successfully save to ' + save_repo)

# # read to geojson and project to EPSG3035
# buildings = gpd.read_file('HD_building_all.geojson').to_crs(epsg=3035)

# # visualize
# f, ax = plt.subplots(figsize=(10, 10))
# gdf_projected.plot(ax=ax)
# ax.set_axis_off()
# plt.show()

################ building feature engineering ###############
buildings['area'] = momepy.Area(buildings).series
buildings['perimeter'] = momepy.Perimeter(buildings).series
buildings['circularcompactness'] = momepy.CircularCompactness(buildings).series
buildings['longestaxislength'] = momepy.LongestAxisLength(buildings).series
buildings['elongation'] = momepy.Elongation(buildings).series
buildings['convexity'] = momepy.Convexity(buildings).series
buildings['orientation'] = momepy.Orientation(buildings).series
buildings['corners'] = momepy.Corners(buildings).series
buildings['sharedwall'] = momepy.SharedWalls(buildings).series
buildings['uID'] = momepy.unique_id(buildings)


################ street feature engineering ###############
# preprocessing
# load GeoPackage as node/edge GeoDataFrames indexed as described in OSMnx docs
gdf_nodes = gpd.read_file('HD_street.gpkg', layer='nodes').set_index('osmid')
gdf_edges = gpd.read_file('HD_street.gpkg', layer='edges').set_index(['u', 'v', 'key'])
# convert the node/edge GeoDataFrames to a MultiDiGraph
graph_attrs = {'crs': 'epsg:3035', 'simplified': True}
streets_df = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs)
# calculate streetfeatures
edges = ox.graph_to_gdfs(streets_df, nodes=False, edges=True,
                         node_geometry=False, fill_edge_geometry=True)
streets_graph = momepy.gdf_to_nx(edges)
# closeness centrality in 500 meters
streets_graph = momepy.closeness_centrality(streets_graph, radius=500, name='closeness500', distance='mm_len', weight='mm_len')
momepy.mean_nodes(streets_graph, 'closeness500')
# betweeennes centrality
streets_graph = momepy.betweenness_centrality(streets_graph, name='betweenness', mode='edges')
# global closeness centrality
streets_graph = momepy.closeness_centrality(streets_graph, name='global_closeness', distance='mm_len', weight='mm_len')
momepy.mean_nodes(streets_graph, 'global_closeness')


# convert to nodes and edges again and align with the nearest buildings
points, lines = momepy.nx_to_gdf(streets_graph)
lines['nID'] = momepy.unique_id(lines)
# buildings['nID'] = momepy.get_network_id(buildings, lines, 'nID')
buildings['nID'] = momepy.get_network_id(buildings, lines, 'nID', min_size=1000)

# openness of the closest street
profile = momepy.StreetProfile(lines, buildings)
lines['widths'] = profile.w
lines['width_deviations'] = profile.wd
lines['openness'] = profile.o

# match the attributes for each buildings based on the nearest rule
closeness500 = []
betweenness = []
global_closeness = []
openness = []
width_deviations = []
widths = []
length = []
for index, row in buildings.iterrows():
    n = row['nID']
    line = lines[lines['nID'] == n]
    betweenness.append(line['betweenness'])
    closeness500.append(line['closeness500'])
    global_closeness.append(line['global_closeness'])
    openness.append(line['openness'])
    width_deviations.append((line['width_deviations']))
    widths.append((line['widths']))
    length.append(line['length'])
buildings['closeness500'] = closeness500
buildings['betweenness'] = betweenness
buildings['global_closeness'] = global_closeness
buildings['openness'] = openness
buildings['width_deviations'] = width_deviations
buildings['widths_street'] = widths
buildings['lengths_street'] = length

# test the output
print(buildings)
assert 0

# save the feature to geojson
save_repo = 'HD_building_all.geojson'
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
