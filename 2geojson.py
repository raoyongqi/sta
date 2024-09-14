import geopandas as gpd

# 读取Shapefile
shp_file_path =  'wsg84/wsg84.shp'
gdf = gpd.read_file(shp_file_path)

# 将数据保存为GeoJSON格式
geojson_file_path = 'grass.geojson'
gdf.to_file(geojson_file_path, driver='GeoJSON')

print(f"Shapefile已成功转换为GeoJSON格式，并保存在{geojson_file_path}")
