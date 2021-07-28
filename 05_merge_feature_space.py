import geopandas as gpd
import numpy as np

feature_1 = gpd.read_file('HD_building_all_1-74.geojson').to_crs(epsg=3035)
feature_2 = gpd.read_file('HD_building_75_116.geojson').to_crs(epsg=3035)
feature_3 = gpd.read_file('HD_building_117_136.geojson').to_crs(epsg=3035)

# merge together
buildings = feature_1.merge(feature_2.iloc[:,np.r_[10,12:53]],how= "left",on="uID")
buildings = buildings.merge(feature_3.iloc[:,np.r_[10,12:30]],how= "left",on="uID")


print(buildings.columns.to_list())
print(buildings.shape)
save_repo = 'HD_building_features_1_136.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)