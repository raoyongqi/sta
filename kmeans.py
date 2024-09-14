import geopandas as gpd
from sklearn.cluster import KMeans
import os
from pyproj import Transformer
# 读取Shapefile
shp_file_path = 'wsg84/wsg84.shp'
gdf = gpd.read_file(shp_file_path)

# 计算质心
gdf['centroid'] = gdf.geometry.centroid
gdf['centroid_lon'] = gdf['centroid'].x
gdf['centroid_lat'] = gdf['centroid'].y
gdf['area'] = gdf.geometry.area

# 准备质心位置的数据
centroids = gdf[['centroid_lon', 'centroid_lat']].values

# 应用 K-means 聚类
n_clusters = 5  # 你可以根据需要调整聚类的数量
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(centroids)
gdf['cluster'] = kmeans.labels_


# 创建一个空的 GeoDataFrame
empty_gdf = gpd.GeoDataFrame(columns=gdf.columns, crs=gdf.crs)


# 创建保存文件夹（如果不存在）
if not os.path.exists('cluster'):
    os.makedirs('cluster')

# 将每个聚类结果保存到不同的 GeoJSON 文件中
for cluster in range(n_clusters):
    cluster_gdf = gdf[gdf['cluster'] == cluster].copy()
    top_two_polygons = cluster_gdf.nlargest(5, 'area')
    # 计算面积（平方公里）
    top_two_polygons['area_km2'] = top_two_polygons['area'] / 1_000_000

    
    # 筛选面积大于 10,000 平方公里的多边形
    top_two_polygons = top_two_polygons[top_two_polygons['area_km2'] > 5_000]

    # 选择前两个最大的多边形
    # 输出结果
    print(f"Cluster {cluster}:")
    for index, row in top_two_polygons.iterrows():
        area_sq_km = row['area_km2']
        print(f"  Polygon Index: {index}")
        print(f"  Area: {area_sq_km:.2f} square kilometers")
        print(f"  Vegetation: {row['植被']}")  # Adjust column name as needed
        print(f"  Vegetation: {row['植被_2']}")  # Adjust column name as needed
        print(f"  Centroid Longitude (WGS84): {row['centroid_lon']}")
        print(f"  Centroid Latitude (WGS84): {row['centroid_lat']}")
        print()
    
    # 转换为 WKT 格式
    cluster_gdf['geometry_wkt'] = cluster_gdf.geometry.to_wkt()
    
    # 删除原始 geometry 列
    cluster_gdf = cluster_gdf.drop(columns='geometry')
    
    # Save the GeoDataFrame with WKT to a GeoJSON file
    cluster_gdf.to_file(f'cluster/cluster_{cluster}.geojson', driver='GeoJSON')
