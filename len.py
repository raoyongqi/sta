import geopandas as gpd
from pyproj import Transformer
import matplotlib.pyplot as plt

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


print(len(gdf_sorted))
