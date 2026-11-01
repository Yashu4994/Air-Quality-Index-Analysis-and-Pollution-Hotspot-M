"""
generate_dataset.py
Generates 5,000 rows of realistic CPCB-aligned Air Quality Index and Weather data
across 50 Indian cities over a 5-year span (2021-2025).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_aqi_dataset(seed=42, total_rows=5000):
    np.random.seed(seed)
    
    cities_meta = [
        # City, Region, Lat, Lon, Baseline PM2.5 multiplier
        ("Delhi", "North", 28.6139, 77.2090, 1.45),
        ("Ghaziabad", "North", 28.6692, 77.4538, 1.50),
        ("Noida", "North", 28.5355, 77.3910, 1.40),
        ("Gurugram", "North", 28.4595, 77.0266, 1.38),
        ("Faridabad", "North", 28.4089, 77.3178, 1.35),
        ("Lucknow", "North", 26.8467, 80.9462, 1.30),
        ("Kanpur", "North", 26.4499, 80.3319, 1.38),
        ("Varanasi", "North", 25.3176, 82.9739, 1.25),
        ("Agra", "North", 27.1767, 78.0081, 1.28),
        ("Meerut", "North", 28.9845, 77.7064, 1.32),
        ("Prayagraj", "North", 25.4358, 81.8463, 1.20),
        ("Bareilly", "North", 28.3670, 79.4304, 1.15),
        ("Gorakhpur", "North", 26.7606, 83.3732, 1.18),
        ("Chandigarh", "North", 30.7333, 76.7794, 0.95),
        ("Ludhiana", "North", 30.9010, 75.8573, 1.25),
        ("Amritsar", "North", 31.6340, 74.8723, 1.15),
        ("Jalandhar", "North", 31.3260, 75.5762, 1.12),
        ("Dehradun", "North", 30.3165, 78.0322, 0.85),
        ("Srinagar", "North", 34.0837, 74.7973, 0.75),
        ("Jammu", "North", 32.7266, 74.8570, 0.82),
        
        ("Kolkata", "East", 22.5726, 88.3639, 1.15),
        ("Patna", "East", 25.5941, 85.1376, 1.42),
        ("Ranchi", "East", 23.3441, 85.3096, 0.95),
        ("Bhubaneswar", "East", 20.2961, 85.8245, 0.85),
        ("Guwahati", "East", 26.1445, 91.7362, 0.90),
        
        ("Mumbai", "West", 19.0760, 72.8777, 1.05),
        ("Pune", "West", 18.5204, 73.8567, 0.92),
        ("Nagpur", "West", 21.1458, 79.0882, 0.98),
        ("Nashik", "West", 19.9975, 73.7898, 0.88),
        ("Ahmedabad", "West", 23.0225, 72.5714, 1.15),
        ("Surat", "West", 21.1702, 72.8311, 1.02),
        ("Vadodara", "West", 22.3072, 73.1812, 0.96),
        ("Rajkot", "West", 22.3039, 70.8022, 0.90),
        ("Jaipur", "West", 26.9124, 75.7873, 1.18),
        ("Jodhpur", "West", 26.2389, 73.0243, 1.10),
        ("Kota", "West", 25.2138, 75.8648, 1.08),
        
        ("Bhopal", "Central", 23.2599, 77.4126, 0.98),
        ("Indore", "Central", 22.7196, 75.8577, 0.94),
        ("Jabalpur", "Central", 23.1815, 79.9864, 0.95),
        ("Gwalior", "Central", 26.2183, 78.1828, 1.25),
        ("Raipur", "Central", 21.2514, 81.6296, 1.10),
        
        ("Bengaluru", "South", 12.9716, 77.5946, 0.65),
        ("Chennai", "South", 13.0827, 80.2707, 0.78),
        ("Hyderabad", "South", 17.3850, 78.4867, 0.88),
        ("Visakhapatnam", "South", 17.6868, 83.2185, 0.82),
        ("Coimbatore", "South", 11.0168, 76.9558, 0.60),
        ("Kochi", "South", 9.9312, 76.2673, 0.55),
        ("Thiruvananthapuram", "South", 8.5241, 76.9366, 0.52),
        ("Mysuru", "South", 12.2958, 76.6394, 0.58),
        ("Madurai", "South", 9.9252, 78.1198, 0.62)
    ]
    
    city_names = [c[0] for c in cities_meta]
    city_multipliers = {c[0]: c[4] for c in cities_meta}
    
    # 5 years: Jan 1, 2021 00:00:00 to Dec 31, 2025 23:00:00
    start_date = datetime(2021, 1, 1, 8, 0, 0)
    end_date = datetime(2025, 12, 31, 20, 0, 0)
    total_seconds = int((end_date - start_date).total_seconds())
    
    # Generate sequential sorted timestamps
    random_offsets = np.sort(np.random.randint(0, total_seconds, total_rows))
    timestamps = [start_date + timedelta(seconds=int(offset)) for offset in random_offsets]
    
    # Assign cities in a balanced yet natural distribution
    assigned_cities = np.random.choice(city_names, size=total_rows)
    
    records = []
    
    for i in range(total_rows):
        dt = timestamps[i]
        city = assigned_cities[i]
        c_mult = city_multipliers[city]
        
        month = dt.month
        day_of_year = dt.timetuple().tm_yday
        hour = dt.hour
        
        # Seasonal cycles in India:
        # Winter: Nov, Dec, Jan, Feb (high pollution, cold, inversion)
        # Summer: Mar, Apr, May, Jun (hot, high ozone, moderate-high dust)
        # Monsoon: Jul, Aug, Sep (rain washout, low particulate)
        # Post-monsoon / Crop burning: Oct, Nov (severe spikes in North)
        
        # Temperature modeling (°C)
        is_north = c_mult >= 1.15
        if month in [12, 1, 2]:
            base_temp = 13.0 if is_north else 23.0
            temp_var = np.random.normal(0, 3.5)
        elif month in [5, 6]:
            base_temp = 36.0 if is_north else 33.0
            temp_var = np.random.normal(0, 3.0)
        elif month in [7, 8, 9]:
            base_temp = 29.0
            temp_var = np.random.normal(0, 2.0)
        else:
            base_temp = 26.0
            temp_var = np.random.normal(0, 3.0)
        
        temp_C = round(float(np.clip(base_temp + temp_var + (hour - 14)*0.3, 4.0, 47.0)), 1)
        
        # Humidity modeling (%)
        if month in [7, 8, 9]:
            base_hum = 82.0
        elif month in [4, 5]:
            base_hum = 32.0
        elif month in [11, 12, 1]:
            base_hum = 68.0
        else:
            base_hum = 55.0
        humidity_pct = round(float(np.clip(base_hum + np.random.normal(0, 9.0), 15.0, 98.0)), 1)
        
        # Seasonal factor for particulate matter
        if month in [11, 12, 1]:
            season_mult = 2.15  # Winter inversion & crop residue
        elif month in [10, 2]:
            season_mult = 1.65
        elif month in [7, 8, 9]:
            season_mult = 0.52  # Monsoon washout
        elif month in [4, 5]:
            season_mult = 1.10  # Dust and dry heat
        else:
            season_mult = 1.00
            
        # Base PM2.5 calculation (ug/m3)
        base_pm25 = 48.0 * c_mult * season_mult
        pm25 = np.random.gamma(shape=5.0, scale=base_pm25/5.0)
        pm25 = round(float(np.clip(pm25, 8.0, 480.0)), 1)
        
        # PM10 is correlated with PM2.5 (ratio roughly 1.5 - 2.2 in India)
        ratio = np.random.uniform(1.55, 2.15)
        pm10 = round(float(np.clip(pm25 * ratio + np.random.normal(5, 10), 18.0, 650.0)), 1)
        
        # NO2 (ppb) - vehicular and industrial (peaks in winter and evening/morning rush hours)
        no2_base = 24.0 * (1.2 if is_north else 0.9) * (1.3 if month in [11, 12, 1] else 1.0)
        no2_ppb = round(float(np.clip(np.random.normal(no2_base, 7.5), 4.0, 115.0)), 1)
        
        # SO2 (ppb) - coal plants / industrial
        so2_base = 12.0 * (1.1 if is_north else 0.85)
        so2_ppb = round(float(np.clip(np.random.normal(so2_base, 4.0), 2.0, 58.0)), 1)
        
        # CO (ppm) - incomplete combustion (ranges 0.3 - 4.5)
        co_base = 1.1 * (1.3 if is_north else 0.9) * (1.4 if month in [11, 12, 1] else 1.0)
        co_ppm = round(float(np.clip(np.random.normal(co_base, 0.35), 0.2, 4.8)), 2)
        
        # O3 (ppb) - photochemically formed, peaks in summer and sunny afternoons
        o3_base = 32.0 * (1.35 if month in [3, 4, 5, 6] else 0.85)
        o3_ppb = round(float(np.clip(np.random.normal(o3_base, 9.0), 5.0, 95.0)), 1)
        
        # CPCB National Air Quality Index (NAQI) calculation
        # Primary driver is PM2.5 and PM10 sub-indices
        # PM2.5 breakpoints:
        # 0-30 -> 0-50
        # 31-60 -> 51-100
        # 61-90 -> 101-200
        # 91-120 -> 201-300
        # 121-250 -> 301-400
        # 250+ -> 401-500
        if pm25 <= 30:
            sub_pm25 = (50 / 30) * pm25
        elif pm25 <= 60:
            sub_pm25 = 50 + (50 / 30) * (pm25 - 30)
        elif pm25 <= 90:
            sub_pm25 = 100 + (100 / 30) * (pm25 - 60)
        elif pm25 <= 120:
            sub_pm25 = 200 + (100 / 30) * (pm25 - 90)
        elif pm25 <= 250:
            sub_pm25 = 300 + (100 / 130) * (pm25 - 120)
        else:
            sub_pm25 = 400 + (100 / 150) * min(pm25 - 250, 150)
            
        # PM10 sub-index
        if pm10 <= 50:
            sub_pm10 = pm10
        elif pm10 <= 100:
            sub_pm10 = 50 + (50 / 50) * (pm10 - 50)
        elif pm10 <= 250:
            sub_pm10 = 100 + (100 / 150) * (pm10 - 100)
        elif pm10 <= 350:
            sub_pm10 = 200 + (100 / 100) * (pm10 - 250)
        elif pm10 <= 430:
            sub_pm10 = 300 + (100 / 80) * (pm10 - 350)
        else:
            sub_pm10 = 400 + (100 / 170) * min(pm10 - 430, 170)
            
        aqi_val = int(round(max(sub_pm25, sub_pm10 * 0.95, no2_ppb * 1.5)))
        aqi = int(np.clip(aqi_val + np.random.randint(-5, 6), 18, 500))
        
        records.append({
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "pm25": pm25,
            "pm10": pm10,
            "no2_ppb": no2_ppb,
            "so2_ppb": so2_ppb,
            "co_ppm": co_ppm,
            "o3_ppb": o3_ppb,
            "aqi": aqi,
            "temp_C": temp_C,
            "humidity_pct": humidity_pct
        })
        
    df = pd.DataFrame(records)
    
    # Introduce ~3% realistic anomalies / sensor faults (as requested in prompt: 2-5%)
    n_anomalies = int(total_rows * 0.03)  # 150 rows
    anomaly_indices = np.random.choice(total_rows, size=n_anomalies, replace=False)
    
    for idx in anomaly_indices:
        anomaly_type = np.random.choice(["spike", "stuck_reading", "dust_surge"])
        if anomaly_type == "spike":
            # Sudden localized episodic industrial/fireworks spike
            df.at[idx, "pm25"] = round(float(np.clip(df.at[idx, "pm25"] * 2.2, 20.0, 520.0)), 1)
            df.at[idx, "pm10"] = round(float(np.clip(df.at[idx, "pm10"] * 2.1, 40.0, 720.0)), 1)
            df.at[idx, "aqi"] = int(np.clip(df.at[idx, "aqi"] + 110, 50, 500))
        elif anomaly_type == "stuck_reading":
            # Sensor calibration zero-offset drift or transient drop
            df.at[idx, "so2_ppb"] = 1.0
            df.at[idx, "no2_ppb"] = 3.0
        elif anomaly_type == "dust_surge":
            # Western storm event: huge PM10 disproportionate to PM2.5
            df.at[idx, "pm10"] = round(float(min(df.at[idx, "pm10"] * 2.8, 750.0)), 1)
            df.at[idx, "aqi"] = int(min(df.at[idx, "aqi"] + 85, 500))
            
    return df

def generate_data_dictionary():
    data = [
        {
            "column_name": "date",
            "data_type": "string (timestamp)",
            "sample_value_1": "2021-01-01 08:14:22",
            "sample_value_2": "2023-06-15 14:30:00",
            "sample_value_3": "2025-11-20 18:45:10",
            "nullable": "No",
            "description": "Timestamp of air quality observation formatted as YYYY-MM-DD HH:MM:SS. Sequential across 5 years (2021-2025)."
        },
        {
            "column_name": "city",
            "data_type": "string (categorical)",
            "sample_value_1": "Delhi",
            "sample_value_2": "Bengaluru",
            "sample_value_3": "Mumbai",
            "nullable": "No",
            "description": "Name of the Indian municipal city / monitoring zone (50 major cities across North, South, East, West, and Central India)."
        },
        {
            "column_name": "pm25",
            "data_type": "float (1 dp)",
            "sample_value_1": "112.4",
            "sample_value_2": "34.8",
            "sample_value_3": "245.1",
            "nullable": "No",
            "description": "Particulate Matter with aerodynamic diameter <= 2.5 micrometres, measured in ug/m3. Primary driver of National AQI."
        },
        {
            "column_name": "pm10",
            "data_type": "float (1 dp)",
            "sample_value_1": "218.6",
            "sample_value_2": "68.2",
            "sample_value_3": "430.5",
            "nullable": "No",
            "description": "Particulate Matter with aerodynamic diameter <= 10 micrometres, measured in ug/m3 (coarse inhalable dust and exhaust particles)."
        },
        {
            "column_name": "no2_ppb",
            "data_type": "float (1 dp)",
            "sample_value_1": "38.5",
            "sample_value_2": "18.2",
            "sample_value_3": "54.0",
            "nullable": "No",
            "description": "Nitrogen Dioxide concentration measured in parts per billion (ppb). Key indicator of vehicular traffic and diesel emissions."
        },
        {
            "column_name": "so2_ppb",
            "data_type": "float (1 dp)",
            "sample_value_1": "14.2",
            "sample_value_2": "8.5",
            "sample_value_3": "22.1",
            "nullable": "No",
            "description": "Sulphur Dioxide concentration measured in parts per billion (ppb). Primarily originates from thermal power generation and refining."
        },
        {
            "column_name": "co_ppm",
            "data_type": "float (2 dp)",
            "sample_value_1": "1.45",
            "sample_value_2": "0.65",
            "sample_value_3": "2.80",
            "nullable": "No",
            "description": "Carbon Monoxide concentration measured in parts per million (ppm). Emitted from incomplete combustion in engines and biomass."
        },
        {
            "column_name": "o3_ppb",
            "data_type": "float (1 dp)",
            "sample_value_1": "28.4",
            "sample_value_2": "45.1",
            "sample_value_3": "16.8",
            "nullable": "No",
            "description": "Ground-level Tropospheric Ozone concentration in parts per billion (ppb). Formed by photochemical reactions between NOx and VOCs."
        },
        {
            "column_name": "aqi",
            "data_type": "integer",
            "sample_value_1": "274",
            "sample_value_2": "68",
            "sample_value_3": "395",
            "nullable": "No",
            "description": "Central Pollution Control Board (CPCB) National Air Quality Index (0-500 scale): 0-50 Good, 51-100 Satisfactory, 101-200 Moderate, 201-300 Poor, 301-400 Very Poor, 401-500 Severe."
        },
        {
            "column_name": "temp_C",
            "data_type": "float (1 dp)",
            "sample_value_1": "14.2",
            "sample_value_2": "32.5",
            "sample_value_3": "26.8",
            "nullable": "No",
            "description": "Ambient surface air temperature measured in degrees Celsius (°C)."
        },
        {
            "column_name": "humidity_pct",
            "data_type": "float (1 dp)",
            "sample_value_1": "72.4",
            "sample_value_2": "41.0",
            "sample_value_3": "88.5",
            "nullable": "No",
            "description": "Relative atmospheric humidity expressed as a percentage (%)."
        }
    ]
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating dataset.csv (5,000 rows)...")
    df = generate_aqi_dataset(seed=42, total_rows=5000)
    df.to_csv("dataset.csv", index=False)
    print(f"Saved dataset.csv with shape: {df.shape}")
    
    print("Generating data_dictionary.csv...")
    dict_df = generate_data_dictionary()
    dict_df.to_csv("data_dictionary.csv", index=False)
    print(f"Saved data_dictionary.csv with shape: {dict_df.shape}")
