import geopandas as gpd
import pandas as pd
from pyproj import Transformer

# 读取Shapefile
shp_file_path = 'wsg84/wsg84.shp'
gdf_projected = gpd.read_file(shp_file_path)

# 检查当前的投影坐标系
print(f"Current CRS: {gdf_projected.crs}")

# 转换为适合面积和质心计算的投影坐标系（例如EPSG:3857）
gdf_projected = gdf_projected.to_crs(epsg=3857)

# 计算投影坐标系下的面积，并将其转换为平方公里
gdf_projected['area_km2'] = (gdf_projected.geometry.area * 0.000001).round(0)  # 转换为平方公里，并保留整数位

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
gdf_sorted = gdf_projected.sort_values(by='area_km2', ascending=False)

# 创建DataFrame，只保留感兴趣的列
df = pd.DataFrame({
    'Area (km²)': gdf_sorted['area_km2'].astype(int),  # 保留整数位
    'Centroid Latitude (WGS84)': gdf_sorted['centroid_lat'],
    'Centroid Longitude (WGS84)': gdf_sorted['centroid_lon'],
    'Vegetation_1': gdf_sorted['植被'],  # 调整为正确的列名
    'Vegetation_2': gdf_sorted['植被_2']  # 调整为正确的列名
})

# 将结果保存为CSV文件
output_csv_path = 'polygons.csv'
df.to_csv(output_csv_path, index=False)

# 将结果保存为JSON文件
output_json_path = 'polygons.json'
df.to_json(output_json_path, orient='records', force_ascii=False, indent=2)  # 使用'records'格式并保持格式化

print(f"polygons saved to {output_csv_path} and {output_json_path}")
import json

# 创建包含感兴趣数据的列表
data = []
for _, row in gdf_sorted.iterrows():
    data.append({
        'weight': int(row['area_km2']),  # 使用面积作为 weight，并确保为整数
        'lnglat': [str(row['centroid_lon']), str(row['centroid_lat'])],
        'name': row.get('Vegetation_2', '')  # 使用 'Vegetation_2' 列作为 name
    })
# 转换为 JavaScript 数组格式
points_js = 'var points = [\n' + ',\n'.join(
    f"    {{ weight: {item['weight']}, lnglat: [{item['lnglat'][0]}, {item['lnglat'][1]}], name: '{item['name']}' }}" 
    for item in data
) + '\n];'

# 保存为 JavaScript 文件
with open('points.js', 'w', encoding='utf-8') as f:
    f.write(points_js)

print("数据已保存为 points.js")