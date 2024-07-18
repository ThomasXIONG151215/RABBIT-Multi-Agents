import numpy as np
import pandas as pd

#np.random.seed(0)  # 为了可重复性设置随机种子

n_observations = 30
data = {
    'Indoor Temperature (°C)': np.random.normal(loc=25, scale=2, size=n_observations),
    'Indoor Humidity (%)': np.random.normal(loc=50, scale=5, size=n_observations),
    'CO2 (ppm)': np.random.normal(loc=400, scale=50, size=n_observations),
    'PM2.5 (µg/m³)': np.random.normal(loc=25, scale=10, size=n_observations),
    'VOC (ppm)': np.random.normal(loc=0.5, scale=0.1, size=n_observations),
    'LED PPFD (µmol/m²/s)': np.random.normal(loc=250, scale=50, size=n_observations),
    'Water pH': np.random.normal(loc=6, scale=0.2, size=n_observations),
    'EC (dS/m)': np.random.normal(loc=1.5, scale=0.25, size=n_observations),
    'LED Energy Consumption (kWh)': np.random.normal(loc=60, scale=10, size=n_observations),
    'AC Energy Consumption (kWh)': np.random.normal(loc=125, scale=25, size=n_observations),
    'Water Pump Energy Consumption (kWh)': np.random.normal(loc=30, scale=5, size=n_observations),
    'Outdoor Temperature (°C)': np.random.normal(loc=-20, scale=25, size=n_observations),
    'Atmospheric Pressure (hPa)': np.random.normal(loc=65, scale=10, size=n_observations),
    'Outdoor Humidity (%)': np.random.normal(loc=5, scale=2, size=n_observations),
    'Dust Concentration (µg/m³)': np.random.normal(loc=500, scale=250, size=n_observations),
    'Solar Irradiance (W/m²)': np.random.normal(loc=370, scale=50, size=n_observations),
}

# 生成增长速率数据，使用布朗运动模型
growth_rate_mm_per_day = np.cumsum(np.random.normal(loc=0.5, scale=0.3, size=n_observations))
growth_rate_mm_per_day2 = np.cumsum(np.random.normal(loc=0.5, scale=0.3, size=n_observations))

# 生成收获指数数据，保证它是累积且在合理范围内
harvest_index = np.minimum(np.cumsum(np.random.uniform(0, 0.1, size=n_observations)) + 0.2, 0.8)
harvest_index2 = np.minimum(np.cumsum(np.random.uniform(0, 0.1, size=n_observations)) + 0.2, 0.8)

# 将生成的数据加入到data字典中
data['Growth Rate (mm/day)'] = growth_rate_mm_per_day
data['Harvest Index'] = harvest_index
data['Growth Rate2 (mm/day)'] = growth_rate_mm_per_day2
data['Harvest Index2'] = harvest_index2

df = pd.DataFrame(data)