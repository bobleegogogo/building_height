# features from 21-38

building_buffer50 = buildings.copy()
building_buffer50.geometry  = building_buffer50.geometry.buffer(50)
building_buffer50_joined = gpd.sjoin(building_buffer50, blocks.iloc[:,np.r_[0,1,3]],how="left",op="intersects")

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

buildings = buildings.merge(building_temp.iloc[:,np.r_[0,2:8]].copy(),how= "left",on="bID")
# save the feature to geojson
save_repo = 'HD_building_all_1-28.geojson'
buildings.to_file(save_repo, driver='GeoJSON')
print('successfully save to ' + save_repo)



# create buffer ->http://docs.momepy.org/en/stable/user_guide/weights/weights_nb.html?highlight=buffer
# http://docs.momepy.org/en/stable/generated/momepy.AverageCharacter.html
#b_dis_50 = libpysal.weights.DistanceBand.from_dataframe(buildings,
#                                                  threshold=50,
#                                                  silence_warnings=True,
#                                                  ids='uID')
# no std.... damn!
# features from 21-38
# features from 21-38
#21
buildings['std_block_orientation_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='BlockOrientation',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').std
#22
buildings['av_block_orientation_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='BlockOrientation',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').mean
#23
buildings['av_block_av_footprint_area_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='AvBlockFootprintArea',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').mean
#24
buildings['std_block_footprint_area_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='AvBlockFootprintArea',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').std
#25
buildings['av_block_footprint_area_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='BlockTotalFootprintArea',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').mean

#26
buildings['std_block_length_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='blockcount',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').std
#27
buildings['av_block_length_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='blockcount',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').mean
#28
buildings['blocks_within_buffer_50'] = momepy.AverageCharacter(buildings,
                                                    values='blockcount',
                                                    spatial_weights=b_dis_50,
                                                    unique_id='uID').count
