import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import Transformer

# 读取Shapefile
shp_file_path = 'wsg84/wsg84.shp'
gdf_projected = gpd.read_file(shp_file_path)

# 检查当前的投影坐标系
print(f"Current CRS: {gdf_projected.crs}")

# 计算投影坐标系下的面积
gdf_projected['area'] = gdf_projected.geometry.area

# 计算投影坐标系下的质心
gdf_projected['centroid'] = gdf_projected.geometry.centroid

# 定义从 EPSG:3857 到 WGS84 (EPSG:4326) 的转换器
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")

# 创建新列以存储转换后的经纬度
gdf_projected['centroid_wgs84'] = gdf_projected['centroid'].apply(lambda point: transformer.transform(point.x, point.y))

# 分离出经纬度
gdf_projected['centroid_lat'] = gdf_projected['centroid_wgs84'].apply(lambda coord: coord[0])
gdf_projected['centroid_lon'] = gdf_projected['centroid_wgs84'].apply(lambda coord: coord[1])

# 按面积从大到小排序
gdf_sorted = gdf_projected.sort_values(by='area', ascending=False)

# 选择前5个多边形
top_5_gdf = gdf_sorted.head(2000)

# 输出前5个多边形的面积和质心经纬度
for index, row in top_5_gdf.iterrows():
    print(f"Polygon {index}:")
    print(f"  Area: {row['area']}")
    print(f"  Centroid Longitude (WGS84): {row['centroid_lon']}")
    print(f"  Centroid Latitude (WGS84): {row['centroid_lat']}")
    print()

# 绘制前5个多边形
fig, ax = plt.subplots(figsize=(10, 10))
top_5_gdf.plot(ax=ax, edgecolor='black', facecolor='skyblue', alpha=0.7)

# 设置图表标题和标签
plt.title('Top 5 Largest Polygons')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 展示图表
plt.show()
