import geopandas as gpd
import matplotlib.pyplot as plt

# 读取Shapefile
shp_file_path = 'wsg84/wsg84.shp'
gdf = gpd.read_file(shp_file_path)

# 绘制Shapefile
gdf.plot()

# 添加标题
plt.title('Shapefile Visualization')

# 显示图形
plt.show()
