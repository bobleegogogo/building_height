# Semi-supervised Learning from Street-View Image and OpenStreetMap for Automatic Building Height Estimation

### Introduction:

Accurate building height estimation is key to the automatic derivation of 3D city models from emerging big geospatial data, including Volunteered Geographical Information (VGI), where a low-cost and automatic solution for large-scale building height estimation is currently missing. More recently, the fast development of VGI data platforms, especially OpenStreetMap (OSM) and crowdsourced street-view image (SVI), offers a stimulating opportunity to fill this research gap. In this work, we propose a semi-supervised learning (SSL) method to automatically estimate building height from Mapillary SVI and OSM data, which is able to create low-cost and open-source 3D city models in LoD1. 

Specifically, the proposed method consists of three parts: first, we propose an SSL schema with the option of setting different ratio of "pseudo label" during the supervised regression; second, we extract multi-level morphometric features from OSM data (i.e., buildings and streets) for the purposed of inferring building height; last, we design a building floor estimation workflow with a pre-trained facade object detection network to generate "pseudo label" from SVI and assign it to the corresponding OSM building footprint.

### Complete feature list:

|***Abbr. name***|***Definition***|***Range/ Unit***|
| :- | :- | :- |
|**Building\***|
|area|Area of the building|meter|
|perimeter|Perimeter of the building|meter|
|circularcompactness|The ratio between the area of the building footprint and the area of the circumscribed circle.|[0, 1]|
|longestaxislength|Length of the longest axis of the building footprint. Axis is defined as a diameter of minimal circumscribed circle around the convex hull.|<p>meter</p><p></p>|
|elongation|Elongation of the minimum bounding box around the building footprint.|[0, 1]|
|<p>convexity</p><p></p>|Area of the footprint divided by the area of the convex hull around the footprint.|[0, 1]|
|orientation|Orientation of the longest axis of bounding rectangle in range 0 – 45. It captures the deviation of orientation from cardinal directions|degree|
|corners|Calculates number of corners of the building.|count|
|sharedwall|Length of wall shared with other buildings.|meters|
|**Block\***|
|*Features of buildings in blocks*|
|blockcount|Number of buildings in the block that the building is part of.|count|
|avBlockFootprintArea|Average footprint area of buildings in the block|squared meter|
|stdBlockFootprintArea|Standard deviation of footprint areas of buildings in the block.|squared meter|
|blockTotalFootprintArea|Total building footprint of the block. Unit: squared meters.|squared meter|
|*Features of block itself*|
|BlockPerimeter|Total perimeter of the block.|meter|
|BlockLongestAxisLength|Length of the longest axis of whole block footprint.|meter|
|BlockElongation|` `Elongation of the minimum bounding box around the whole block footprint.|[0, 1]|
|BlockConvexity|Convexity of the whole block footprint. |[0, 1]|
|BlockOrientation|Orientation of the whole block footprint.|degree|
|BlockCorners|Number of corners of the whole block footprint.|count|
|**Street & intersection\***|
|closeness500|Local closeness centrality for the closest street to the building.|[0, 1]|
|betweenness|Betweenness centrality of the closest street to the building.|[0, 1]|
|global\_closeness|Global closeness centrality of the closest street to the building.|[0, 1]|
|<p>openness</p><p></p>|Openness of the closest street to building. Proportion of the street where buildings are or not present on the sides of the street.|[0, 1]|
|width\_deviations|Standard deviation of the width of the closest street to the building. Width is defined here as the average distance between buildings on both sides of the street.|<p>meters</p><p></p>|
|widths\_street|Width of the closest street to the building. |meters|
|lengths\_street|Length of the closest street to the building.|meters|
|distance\_road|Distance between the building and the closest street.|meters|
|distance\_intersection|Distance between the building and the closest intersection. |meters|
|**Street-based block\***|
|<p>street\_based\_block\_phi</p><p></p>|Anisotropy index of the street-based block at the building location.|` `[0, 1]|
|street\_based\_block\_area|Area of the street-based block at the building location.|squared meter|
\* 50,200,500m buffers applied and the mean and std values were calculated.

## Contact

Dr. Hao Li \
Email: [hao_bgd.li@tum.de](mailto:hao_bgd.li@tum.de)\
Technische Universität München, Dartment Aerospace and Geodesy \
Professur für Big Geospatial Data Management \
Lise Meitner Str. 9, 85521 Ottobrunn
