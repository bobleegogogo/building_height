# import momepy
import random
import geopandas as gpd
from matplotlib import pyplot as plt

# some threshold and need man-made parameters
Num_pt_svimg_for_everybuilding = 2
Num_sampling = 2

# plot window
fig, ax = plt.subplots(figsize=(12, 12))


# load data
## footprints data
bldg = gpd.read_file(r'D:\Work\buildingheight\building_height_street_view\data\HD_sample_data\sample_1\1block.geojson').to_crs(epsg=3035)
print('bldg:******\n', bldg)
## gps poitns of stretview images
pt_svimg = gpd.read_file(r'D:\Work\buildingheight\building_height_street_view\data\HD_sample_data\sample_1\1street-3-points.geojson').to_crs(epsg=3035)
print('pt_svimg:******\n', pt_svimg)
pt_svimg['unique_idx'] = pt_svimg.index
# ax = pt_svimg.plot(ax=ax, color='black')

# calculate center of every building
bldg_center = gpd.GeoDataFrame(bldg, geometry=bldg.centroid)


'''Step 1: Find clean building polygons (footprints)'''
# 1.1 create every building's buffer (distance=0.2 or smaller)
bldg_buffer = bldg.buffer(distance=0.2)
bldg_buffer = gpd.GeoDataFrame(bldg, geometry=bldg_buffer)
# print(gdf_buffer)
# ax=gdf_buffer.plot(ax=ax, color='red')
# gdf_buffer.plot()

# 1.2 find overlayed building buffers, and then delete them
## 1.2.1 find
bldg_together = gpd.sjoin(bldg_buffer, bldg_buffer.set_index(bldg_buffer['@osmId']))
bldg_over = bldg_together.loc[bldg_together['@osmId_left'] != bldg_together.index_right]
# ax=bldg_over.plot(ax=ax, color='green')

## 1.2.2 drop
bldg_unique = bldg.drop(bldg_over.index)
print(bldg_unique)
# bldg_unique.plot()

# # union overlapped building buffers
# gdf_union_explode = gdf_buffer.dissolve().explode()
# gdf_union_explode['index'] = gdf_union_explode.index
# print(gdf_union_explode)
#
# # count





'''Step 2: find clean footprints with streetview images'''
# 2.1 decrease the number of gps points --> to avoid the calculation of many close or overlapped points
## 2.1.1 create points buffers
pt_svimg_buffer = pt_svimg.buffer(distance=3)
pt_svimg_buffer = gpd.GeoDataFrame(pt_svimg, geometry=pt_svimg_buffer)
# ax = pt_svimg_buffer.plot(ax=ax, color='green', alpha=0.2)

## 2.1.2 union overlapped points, and create new street view points
# pt_svimg_together = gpd.sjoin(pt_svimg_buffer, pt_svimg_buffer.set_index(pt_svimg_buffer['unique_idx']))
# pt_svimg_over = pt_svimg_together.loc[pt_svimg_together['unique_idx_left'] != pt_svimg_together.index_right]
pt_svimg_union_explode = pt_svimg_buffer.dissolve().explode()
# ax = pt_svimg_buffer.plot(ax=ax, color='brown', alpha=0.2)
pt_svimg_clean_center = pt_svimg_union_explode.centroid
pt_svimg_clean_center = gpd.GeoDataFrame(geometry=pt_svimg_clean_center)
print('new center points of street view images******\n', pt_svimg_clean_center)
# ax = pt_svimg_clean_center.plot(ax=ax, color='red')


# 2.2 create larger buffer for every clean footprint (distance=10, which can cover most roads' widths)
bldg_buffer_large = bldg_unique.buffer(distance=10)
bldg_buffer_large = gpd.GeoDataFrame(bldg_unique, geometry=bldg_buffer_large)
bldg_buffer_large['bldg_idx'] = bldg_buffer_large.index
print('bldg_buffer_large******\n', bldg_buffer_large)
# ax = bldg_buffer_large.plot(ax=ax, alpha=0.2)


# 2.3 count points in every polygon
# reference: https://blog.csdn.net/fengdu78/article/details/107054250/?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_baidulandingword-0&spm=1001.2101.3001.4242
### points: gps points of streetview images
### polygons: clean footprints
bldg_num_pt_svimg = gpd.sjoin(left_df=bldg_buffer_large, right_df=pt_svimg_clean_center, op='contains').groupby('bldg_idx').size()
# print(bldg_num_pt_svimg)
bldg_buffer_large['num_svimg'] = 0
bldg_buffer_large.loc[bldg_num_pt_svimg.index, 'num_svimg'] = bldg_num_pt_svimg
print('\nthe number of streetview images in every building large buffer:******\n', bldg_buffer_large)

# 2.4 find footprints with over than 2 streetview images
bldg_buffer_large_over_2 = bldg_buffer_large[bldg_buffer_large['num_svimg']>=Num_pt_svimg_for_everybuilding]
bldg_can_sampling = bldg.loc[bldg_buffer_large_over_2['bldg_idx'],:]
# ax = bldg_buffer_large_over_2.plot(ax=ax, alpha=0.2, color='purple')
# ax = bldg_can_sampling.plot(ax=ax, alpha=1, color='purple')




'''Step 3: sampling'''
# 3.1 judge whether 'num_sampling' is larger than the number of footprints can be used
if Num_sampling > len(bldg_can_sampling):
    print('the smapling number is too large! Please set it smaller than {}'.format(len(bldg_can_sampling)))
else:
    sample_idx = random.sample(range(len(bldg_can_sampling)),Num_sampling)
    bldg_sampling_res = bldg_can_sampling.iloc[sample_idx,:]
    print('sample successfully!******\nsample_idx: {}\nsampling result: {}\n'.format(sample_idx, bldg_sampling_res))

# plt.show()