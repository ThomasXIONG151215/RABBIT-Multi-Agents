import pandas as pd 
import numpy as np

data = { 'Indoor Temperature (°C)': np.random.uniform(20, 30, size=30), 
        #'Outdoor Temperature (°C)': np.random.uniform(15, 25, size=30), 
        'Indoor Humidity (%)': np.random.uniform(40, 60, size=30), 
        #'Outdoor Humidity (%)': np.random.uniform(30, 50, size=30), 
        'CO2 (ppm)': np.random.uniform(300, 500, size=30), 
        'PM2.5 (µg/m³)': np.random.uniform(0, 50, size=30), 
        'VOC (ppm)': np.random.uniform(0, 1, size=30), 
        'LED PPFD (µmol/m²/s)': np.random.uniform(100, 400, size=30), 
        'Water pH': np.random.uniform(5.5, 6.5, size=30), 
        'EC (dS/m)': np.random.uniform(1.0, 2.5, size=30), 
        'LED Energy Consumption (kWh)': np.random.uniform(20, 100, size=30), 
        'AC Energy Consumption (kWh)': np.random.uniform(50, 200, size=30), 
        'Water Pump Energy Consumption (kWh)': np.random.uniform(10, 50, size=30), 
        'Outdoor Temperature (°C)': np.random.uniform(-70, 20, size=30),  # Mars temperature range
    'Atmospheric Pressure (hPa)': np.random.uniform(30, 100, size=30),  # Mars atmospheric pressure
    'Outdoor Humidity (%)': np.random.uniform(0, 10, size=30),       # Mars humidity is very low
    'Dust Concentration (µg/m³)': np.random.uniform(0, 1000, size=30), # Dust storms can be common
    'Solar Irradiance (W/m²)': np.random.uniform(150, 590, size=30),  # Solar irradiance on Mars
        }
n_observations = 30
# 生成生长速率数据，这里假设单位是毫米/天
growth_rate_mm_per_day = np.random.uniform(0.1, 5, size=n_observations)

# 生成收获指数数据，这里假设是比例
harvest_index = np.random.uniform(0.2, 0.8, size=n_observations)

# 这里我们假设 data 是已存在的字典或数据框，我们将把生成的数据加入其中
data['Growth Rate (mm/day)'] = growth_rate_mm_per_day
data['Harvest Index'] = harvest_index
df = pd.DataFrame(data)
