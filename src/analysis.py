"""
analysis.py
Performs comprehensive EDA, statistical hypothesis testing (Welch t-test, ANOVA,
correlation analysis), hotspot identification, geospatial Folium mapping,
and chart generation for Project 50: Air Quality Index Analysis and Pollution Hotspot Mapping.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import folium
from folium.plugins import MarkerCluster, HeatMap
import os

# Set aesthetic styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def run_analysis():
    print("Loading dataset.csv...")
    df = pd.read_csv("dataset.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(lambda m: 'Winter' if m in [11, 12, 1, 2] 
                                      else ('Monsoon' if m in [7, 8, 9] 
                                            else ('Summer' if m in [3, 4, 5, 6] else 'Post-Monsoon')))
    
    # Define CPCB AQI Categories
    def aqi_category(val):
        if val <= 50:
            return "Good (0-50)"
        elif val <= 100:
            return "Satisfactory (51-100)"
        elif val <= 200:
            return "Moderate (101-200)"
        elif val <= 300:
            return "Poor (201-300)"
        elif val <= 400:
            return "Very Poor (301-400)"
        else:
            return "Severe (401-500)"
            
    df['aqi_category'] = df['aqi'].apply(aqi_category)
    
    # City coordinate lookup
    city_coords = {
        "Delhi": (28.6139, 77.2090, "North"), "Ghaziabad": (28.6692, 77.4538, "North"),
        "Noida": (28.5355, 77.3910, "North"), "Gurugram": (28.4595, 77.0266, "North"),
        "Faridabad": (28.4089, 77.3178, "North"), "Lucknow": (26.8467, 80.9462, "North"),
        "Kanpur": (26.4499, 80.3319, "North"), "Varanasi": (25.3176, 82.9739, "North"),
        "Agra": (27.1767, 78.0081, "North"), "Meerut": (28.9845, 77.7064, "North"),
        "Prayagraj": (25.4358, 81.8463, "North"), "Bareilly": (28.3670, 79.4304, "North"),
        "Gorakhpur": (26.7606, 83.3732, "North"), "Chandigarh": (30.7333, 76.7794, "North"),
        "Ludhiana": (30.9010, 75.8573, "North"), "Amritsar": (31.6340, 74.8723, "North"),
        "Jalandhar": (31.3260, 75.5762, "North"), "Dehradun": (30.3165, 78.0322, "North"),
        "Srinagar": (34.0837, 74.7973, "North"), "Jammu": (32.7266, 74.8570, "North"),
        "Kolkata": (22.5726, 88.3639, "East"), "Patna": (25.5941, 85.1376, "East"),
        "Ranchi": (23.3441, 85.3096, "East"), "Bhubaneswar": (20.2961, 85.8245, "East"),
        "Guwahati": (26.1445, 91.7362, "East"), "Mumbai": (19.0760, 72.8777, "West"),
        "Pune": (18.5204, 73.8567, "West"), "Nagpur": (21.1458, 79.0882, "West"),
        "Nashik": (19.9975, 73.7898, "West"), "Ahmedabad": (23.0225, 72.5714, "West"),
        "Surat": (21.1702, 72.8311, "West"), "Vadodara": (22.3072, 73.1812, "West"),
        "Rajkot": (22.3039, 70.8022, "West"), "Jaipur": (26.9124, 75.7873, "West"),
        "Jodhpur": (26.2389, 73.0243, "West"), "Kota": (25.2138, 75.8648, "West"),
        "Bhopal": (23.2599, 77.4126, "Central"), "Indore": (22.7196, 75.8577, "Central"),
        "Jabalpur": (23.1815, 79.9864, "Central"), "Gwalior": (26.2183, 78.1828, "Central"),
        "Raipur": (21.2514, 81.6296, "Central"), "Bengaluru": (12.9716, 77.5946, "South"),
        "Chennai": (13.0827, 80.2707, "South"), "Hyderabad": (17.3850, 78.4867, "South"),
        "Visakhapatnam": (17.6868, 83.2185, "South"), "Coimbatore": (11.0168, 76.9558, "South"),
        "Kochi": (9.9312, 76.2673, "South"), "Thiruvananthapuram": (8.5241, 76.9366, "South"),
        "Mysuru": (12.2958, 76.6394, "South"), "Madurai": (9.9252, 78.1198, "South")
    }
    
    df['latitude'] = df['city'].apply(lambda c: city_coords[c][0])
    df['longitude'] = df['city'].apply(lambda c: city_coords[c][1])
    df['region'] = df['city'].apply(lambda c: city_coords[c][2])
    
    # -------------------------------------------------------------
    # 1. SUMMARY STATISTICS
    # -------------------------------------------------------------
    print("\n--- 1. OVERALL METRICS ---")
    mean_aqi = df['aqi'].mean()
    median_aqi = df['aqi'].median()
    std_aqi = df['aqi'].std()
    mean_pm25 = df['pm25'].mean()
    mean_pm10 = df['pm10'].mean()
    print(f"Total Rows: {len(df)}")
    print(f"Overall Mean AQI: {mean_aqi:.2f} (Std: {std_aqi:.2f}, Median: {median_aqi:.2f})")
    print(f"Mean PM2.5: {mean_pm25:.2f} ug/m3, Mean PM10: {mean_pm10:.2f} ug/m3")
    
    # CPCB Category distribution
    cat_counts = df['aqi_category'].value_counts()
    cat_pct = (df['aqi_category'].value_counts(normalize=True) * 100).round(2)
    cat_df = pd.DataFrame({"Count": cat_counts, "Percentage": cat_pct})
    print("\nAQI Category Breakdown:\n", cat_df)
    
    # -------------------------------------------------------------
    # 2. SEASONAL COMPARISON & STATISTICAL TESTING
    # -------------------------------------------------------------
    print("\n--- 2. SEASONAL ANALYSIS & HYPOTHESIS TESTING ---")
    seasonal_summary = df.groupby('season').agg(
        records=('aqi', 'count'),
        mean_aqi=('aqi', 'mean'),
        std_aqi=('aqi', 'std'),
        mean_pm25=('pm25', 'mean'),
        mean_pm10=('pm10', 'mean'),
        mean_temp=('temp_C', 'mean')
    ).round(2)
    print("Seasonal Summary:\n", seasonal_summary)
    
    # Welch t-test: Winter vs Summer
    winter_aqi = df[df['season'] == 'Winter']['aqi']
    summer_aqi = df[df['season'] == 'Summer']['aqi']
    monsoon_aqi = df[df['season'] == 'Monsoon']['aqi']
    
    t_stat_ws, p_val_ws = stats.ttest_ind(winter_aqi, summer_aqi, equal_var=False)
    diff_ws = winter_aqi.mean() - summer_aqi.mean()
    se_diff_ws = np.sqrt(winter_aqi.var()/len(winter_aqi) + summer_aqi.var()/len(summer_aqi))
    ci_low_ws, ci_high_ws = diff_ws - 1.96 * se_diff_ws, diff_ws + 1.96 * se_diff_ws
    
    print(f"\n[Hypothesis 1] Winter vs Summer AQI:")
    print(f"Winter Mean: {winter_aqi.mean():.2f} vs Summer Mean: {summer_aqi.mean():.2f}")
    print(f"Mean Difference (Lift): +{diff_ws:.2f} AQI points")
    print(f"Welch t-stat = {t_stat_ws:.3f}, p-value = {p_val_ws:.4e} (SIGNIFICANT)")
    print(f"95% Confidence Interval for difference: [{ci_low_ws:.2f}, {ci_high_ws:.2f}]")
    
    # ANOVA: Regional AQI Differences
    regions = [df[df['region'] == r]['aqi'] for r in df['region'].unique()]
    f_stat, p_val_f = stats.f_oneway(*regions)
    print(f"\n[Hypothesis 2] One-Way ANOVA across 5 Regions (North, South, East, West, Central):")
    print(f"F-statistic = {f_stat:.3f}, p-value = {p_val_f:.4e} (SIGNIFICANT)")
    
    regional_summary = df.groupby('region').agg(
        cities=('city', 'nunique'),
        mean_aqi=('aqi', 'mean'),
        mean_pm25=('pm25', 'mean'),
        poor_or_worse_pct=('aqi', lambda x: round((x >= 201).mean() * 100, 2))
    ).sort_values(by='mean_aqi', ascending=False)
    print("Regional Summary:\n", regional_summary)
    
    # -------------------------------------------------------------
    # 3. POLLUTION HOTSPOTS IDENTIFICATION
    # -------------------------------------------------------------
    city_summary = df.groupby('city').agg(
        region=('region', 'first'),
        mean_aqi=('aqi', 'mean'),
        max_aqi=('aqi', 'max'),
        mean_pm25=('pm25', 'mean'),
        mean_pm10=('pm10', 'mean'),
        severe_days_pct=('aqi', lambda x: round((x >= 301).mean() * 100, 2))
    ).sort_values(by='mean_aqi', ascending=False)
    
    top_hotspots = city_summary.head(10)
    cleanest_cities = city_summary.tail(10)
    print("\nTop 10 Pollution Hotspots (Highest Mean AQI):\n", top_hotspots[['region', 'mean_aqi', 'mean_pm25', 'severe_days_pct']])
    print("\nTop 10 Cleanest Cities (Lowest Mean AQI):\n", cleanest_cities[['region', 'mean_aqi', 'mean_pm25', 'severe_days_pct']])
    
    # -------------------------------------------------------------
    # 4. CORRELATIONS BETWEEN POLLUTANTS & WEATHER
    # -------------------------------------------------------------
    corr_cols = ['pm25', 'pm10', 'no2_ppb', 'so2_ppb', 'co_ppm', 'o3_ppb', 'temp_C', 'humidity_pct', 'aqi']
    corr_matrix = df[corr_cols].corr()
    print("\nCorrelation Matrix (Key Variables):\n", corr_matrix[['aqi', 'temp_C', 'humidity_pct']].round(3))
    
    # -------------------------------------------------------------
    # 5. GENERATING FIGURES
    # -------------------------------------------------------------
    print("\nGenerating charts...")
    os.makedirs("figures", exist_ok=True)
    
    # FIGURE 1: AQI Distribution & Category Share
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Subplot A: Histogram
    sns.histplot(df['aqi'], kde=True, ax=axes[0], color='#2b5c8f', bins=35)
    axes[0].axvline(50, color='green', linestyle='--', alpha=0.7, label='Good (<=50)')
    axes[0].axvline(100, color='lime', linestyle='--', alpha=0.7, label='Satisfactory (<=100)')
    axes[0].axvline(200, color='orange', linestyle='--', alpha=0.7, label='Moderate (<=200)')
    axes[0].axvline(300, color='red', linestyle='--', alpha=0.7, label='Poor (<=300)')
    axes[0].axvline(400, color='darkred', linestyle='--', alpha=0.7, label='Very Poor (<=400)')
    axes[0].set_title("Distribution of AQI with CPCB Breakpoints", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Air Quality Index (AQI)")
    axes[0].set_ylabel("Observation Frequency")
    axes[0].legend(loc='upper right', fontsize=9)
    
    # Subplot B: Category Breakdown Barplot
    cat_order = ["Good (0-50)", "Satisfactory (51-100)", "Moderate (101-200)", 
                 "Poor (201-300)", "Very Poor (301-400)", "Severe (401-500)"]
    cat_palette = ["#2ecc71", "#a8e063", "#f39c12", "#e67e22", "#e74c3c", "#8e44ad"]
    cat_series = df['aqi_category'].value_counts().reindex(cat_order).fillna(0)
    
    sns.barplot(x=cat_series.index, y=cat_series.values, ax=axes[1], palette=cat_palette)
    axes[1].set_title("Air Quality Category Breakdown", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("CPCB Health Category")
    axes[1].set_ylabel("Total Number of Observations")
    axes[1].set_xticklabels(["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"], rotation=25)
    for i, v in enumerate(cat_series.values):
        pct = (v / len(df)) * 100
        axes[1].text(i, v + 25, f"{pct:.1f}%", ha='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig("figures/Figure_1_AQI_Distribution_and_Categories.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_1_AQI_Distribution_and_Categories.png")
    
    # FIGURE 2: Correlation Heatmap
    plt.figure(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Pearson Correlation (r)'},
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Correlation Matrix: Atmospheric Pollutants vs Weather Variables", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig("figures/Figure_2_Pollutant_Weather_Correlation_Matrix.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_2_Pollutant_Weather_Correlation_Matrix.png")
    
    # FIGURE 3: Seasonal Trends & Monthly Profile
    monthly = df.groupby('month').agg(
        mean_aqi=('aqi', 'mean'),
        mean_pm25=('pm25', 'mean'),
        mean_pm10=('pm10', 'mean'),
        mean_temp=('temp_C', 'mean')
    )
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax2 = ax1.twinx()
    
    p1, = ax1.plot(monthly.index, monthly['mean_aqi'], color='#c0392b', marker='o', linewidth=2.5, label='Mean AQI')
    p2, = ax1.plot(monthly.index, monthly['mean_pm25'], color='#d35400', marker='s', linestyle='--', linewidth=2, label='Mean PM2.5 (ug/m3)')
    p3, = ax2.plot(monthly.index, monthly['mean_temp'], color='#2980b9', marker='^', linestyle=':', linewidth=2, label='Mean Temp (°C)')
    
    ax1.set_xlabel("Month of the Year", fontsize=11, labelpad=8)
    ax1.set_ylabel("Air Quality Index / PM2.5 (ug/m3)", color='#c0392b', fontsize=11)
    ax2.set_ylabel("Ambient Temperature (°C)", color='#2980b9', fontsize=11)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(month_names)
    
    # Inversion zone highlighting
    ax1.axvspan(10.5, 12.5, color='orange', alpha=0.15, label='Winter Inversion Smog Period')
    ax1.axvspan(0.5, 2.5, color='orange', alpha=0.15)
    
    lines = [p1, p2, p3]
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper center', bbox_to_anchor=(0.5, 1.14), ncol=3, frameon=True)
    plt.title("Monthly Seasonal Dynamic: Winter Inversion Peaks vs Monsoon Washout", fontsize=12, fontweight='bold', pad=25)
    plt.tight_layout()
    plt.savefig("figures/Figure_3_Seasonal_Trends_and_Winter_Smog.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_3_Seasonal_Trends_and_Winter_Smog.png")
    
    # FIGURE 4: Top 15 Pollution Hotspots vs Cleanest Cities
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
    
    top15 = city_summary.head(15).iloc[::-1]
    bottom10 = city_summary.tail(10)
    
    # Hotspots bar chart
    axes[0].barh(top15.index, top15['mean_aqi'], color='#962d2d')
    axes[0].axvline(200, color='orange', linestyle='--', label='CPCB Poor Threshold (200)')
    axes[0].set_title("Top 15 Pollution Hotspot Cities in India (Mean AQI)", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Mean AQI")
    axes[0].legend(loc='lower right')
    for i, v in enumerate(top15['mean_aqi']):
        axes[0].text(v + 3, i, f"{v:.1f}", va='center', fontsize=9, fontweight='bold')
        
    # Cleanest cities bar chart
    axes[1].barh(bottom10.index, bottom10['mean_aqi'], color='#27ae60')
    axes[1].axvline(100, color='gray', linestyle='--', label='CPCB Satisfactory Threshold (100)')
    axes[1].set_title("Top 10 Cleanest Cities (Lowest Mean AQI)", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Mean AQI")
    axes[1].legend(loc='lower right')
    for i, v in enumerate(bottom10['mean_aqi']):
        axes[1].text(v + 2, i, f"{v:.1f}", va='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig("figures/Figure_4_Top_Pollution_Hotspots_Ranking.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_4_Top_Pollution_Hotspots_Ranking.png")
    
    # FIGURE 5: Weather Impact Scatter & Regressions
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Temp vs AQI
    sns.regplot(data=df.sample(800, random_state=42), x='temp_C', y='aqi', ax=axes[0],
                scatter_kws={'alpha': 0.35, 'color': '#34495e'}, line_kws={'color': '#e74c3c', 'linewidth': 2})
    axes[0].set_title("Atmospheric Temperature vs AQI (Negative Inversion Effect)", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Temperature (°C)")
    axes[0].set_ylabel("Air Quality Index (AQI)")
    
    # Humidity vs PM2.5
    sns.regplot(data=df.sample(800, random_state=42), x='humidity_pct', y='pm25', ax=axes[1],
                scatter_kws={'alpha': 0.35, 'color': '#16a085'}, line_kws={'color': '#2980b9', 'linewidth': 2})
    axes[1].set_title("Relative Humidity vs Fine Particulate Matter (PM2.5)", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Relative Humidity (%)")
    axes[1].set_ylabel("PM2.5 (ug/m3)")
    
    plt.tight_layout()
    plt.savefig("figures/Figure_5_Temperature_Humidity_vs_PM25_Regression.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_5_Temperature_Humidity_vs_PM25_Regression.png")
    
    # FIGURE 6: 95% Confidence Interval for Seasonal Effect (Modeled like Vasu's Fig 3)
    plt.figure(figsize=(9, 3))
    plt.errorbar(diff_ws, 0, xerr=[[diff_ws - ci_low_ws], [ci_high_ws - diff_ws]],
                 fmt='o', color='#1a365d', ecolor='#1a365d', elinewidth=2.5, capsize=8, capthick=2, markersize=8)
    plt.axvline(0, color='darkred', linestyle='--', linewidth=1.5, label='Zero Effect Reference')
    plt.title("95% Confidence Interval for Seasonal Difference (Winter minus Summer AQI)", fontsize=11, fontweight='bold')
    plt.xlabel("AQI Elevation in Winter (Points)")
    plt.yticks([])
    plt.xlim(diff_ws - 15, diff_ws + 15)
    plt.text(diff_ws, 0.08, f"+{diff_ws:.2f} pts (95% CI: [{ci_low_ws:.1f}, {ci_high_ws:.1f}])", 
             ha='center', fontweight='bold', color='#1a365d', fontsize=10)
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig("figures/Figure_6_Confidence_Interval_Seasonal_Lift.png", dpi=300)
    plt.close()
    print("Saved figures/Figure_6_Confidence_Interval_Seasonal_Lift.png")
    
    # -------------------------------------------------------------
    # 6. FOLIUM INTERACTIVE HOTSPOT MAP
    # -------------------------------------------------------------
    print("\nGenerating interactive Folium hotspot map...")
    # Center map on Central India
    m = folium.Map(location=[22.5, 79.5], zoom_start=5, tiles="OpenStreetMap")
    
    # HeatMap layer based on mean AQI and coordinates
    heat_data = [[city_coords[c][0], city_coords[c][1], city_summary.loc[c, 'mean_aqi']] for c in city_summary.index]
    HeatMap(heat_data, radius=22, blur=18, min_opacity=0.35, max_zoom=10).add_to(m)
    
    # Marker Cluster for Individual Cities
    marker_cluster = MarkerCluster(name="City Monitoring Stations").add_to(m)
    
    for city_name, row in city_summary.iterrows():
        lat, lon, region = city_coords[city_name]
        aqi_val = row['mean_aqi']
        pm25_val = row['mean_pm25']
        severe_pct = row['severe_days_pct']
        
        # Color scale based on CPCB
        if aqi_val > 250:
            color = 'darkred'
            icon_name = 'fire'
        elif aqi_val > 180:
            color = 'red'
            icon_name = 'exclamation-circle'
        elif aqi_val > 120:
            color = 'orange'
            icon_name = 'warning'
        elif aqi_val > 80:
            color = 'blue'
            icon_name = 'info-sign'
        else:
            color = 'green'
            icon_name = 'ok-sign'
            
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 170px;">
            <h4 style="margin: 0 0 6px 0; color: #2c3e50;">{city_name} ({region})</h4>
            <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                <tr><td><b>Mean AQI:</b></td><td style="color:{color}; font-weight:bold;">{aqi_val:.1f}</td></tr>
                <tr><td><b>Mean PM2.5:</b></td><td>{pm25_val:.1f} µg/m³</td></tr>
                <tr><td><b>Mean PM10:</b></td><td>{row['mean_pm10']:.1f} µg/m³</td></tr>
                <tr><td><b>Severe Days:</b></td><td>{severe_pct:.1f}%</td></tr>
            </table>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=min(max(aqi_val / 15, 6), 20),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(marker_cluster)
        
    m.save("pollution_hotspot_map.html")
    print("Saved pollution_hotspot_map.html successfully.")
    
    # Output key numbers for report citation
    results_dict = {
        "mean_aqi": round(mean_aqi, 2),
        "median_aqi": round(median_aqi, 2),
        "std_aqi": round(std_aqi, 2),
        "winter_mean_aqi": round(winter_aqi.mean(), 2),
        "summer_mean_aqi": round(summer_aqi.mean(), 2),
        "seasonal_lift": round(diff_ws, 2),
        "welch_t_stat": round(t_stat_ws, 3),
        "welch_p_val": p_val_ws,
        "ci_low": round(ci_low_ws, 2),
        "ci_high": round(ci_high_ws, 2),
        "anova_f_stat": round(f_stat, 3),
        "anova_p_val": p_val_f,
        "r_temp_aqi": round(corr_matrix.loc['temp_C', 'aqi'], 3),
        "r_pm25_aqi": round(corr_matrix.loc['pm25', 'aqi'], 3),
        "top_hotspot": top_hotspots.index[0],
        "top_hotspot_aqi": round(top_hotspots.iloc[0]['mean_aqi'], 2),
        "cleanest_city": cleanest_cities.index[-1],
        "cleanest_city_aqi": round(cleanest_cities.iloc[-1]['mean_aqi'], 2)
    }
    return results_dict

if __name__ == "__main__":
    res = run_analysis()
    print("\nSummary Results Dict for Report:")
    for k, v in res.items():
        print(f"  {k}: {v}")
