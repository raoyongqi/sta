import geopandas as gpd

# 读取Shapefile
shp_file_path = 'wsg84/wsg84.shp'
gdf_projected = gpd.read_file(shp_file_path)

# 检查当前的投影坐标系
print(f"Current CRS: {gdf_projected.crs}")

# 转换为适合面积和质心计算的投影坐标系（例如EPSG:3857）
gdf_projected = gdf_projected.to_crs(epsg=3857)

# 计算投影坐标系下的面积
gdf_projected['area'] = gdf_projected.geometry.area

# 计算所有面积的和（平方米）
total_area_sqm = gdf_projected['area'].sum()

# 将面积转换为万平方公里（1平方米 = 0.000001平方公里）
total_area_km2 = total_area_sqm * 0.000001  # 转换为平方公里
total_area_10k_km2 = total_area_km2 / 10000  # 转换为万平方公里

# 中国国土面积约为 9,600,000 平方公里，转换为平方米
china_area_sqm = 9_600_000 * 1_000_000  # 平方公里转平方米

# 计算面积占比（百分比）
area_percentage = (total_area_sqm / china_area_sqm) * 100

# 计算最大的2000个polygon的面积
gdf_projected_sorted = gdf_projected.sort_values(by='area', ascending=False)
largest_2000_polygons = gdf_projected_sorted.head(2000)

# 计算2000个polygon的面积和
largest_2000_area_sqm = largest_2000_polygons['area'].sum()

# 将面积转换为万平方公里
largest_2000_area_10k_km2 = largest_2000_area_sqm * 0.000001 / 10000  # 转换为万平方公里

# 计算2000个polygon占总面积的百分比
largest_2000_area_percentage = (largest_2000_area_sqm / total_area_sqm) * 100

# 打印结果，保留两位小数
print(f"Total area: {total_area_10k_km2:.2f} 万平方公里")
print(f"Percentage of China's land area: {area_percentage:.2f}%")
print(f"Top 2000 polygons area: {largest_2000_area_10k_km2:.2f} 万平方公里")
print(f"Top 2000 polygons percentage of total area: {largest_2000_area_percentage:.2f}%")
