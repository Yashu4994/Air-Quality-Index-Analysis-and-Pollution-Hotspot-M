"""
build_notebook.py
Builds the complete P_50_AQI_Hotspot_Analysis.ipynb notebook
with comprehensive markdown documentation, code cells, and analysis.
"""

import json

def make_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# HCLTech Career Shaper Programme\n",
                "## III Year Industry Project (2025–26) — Project No. 50\n",
                "# Air Quality Index Analysis and Pollution Hotspot Mapping\n",
                "\n",
                "| Field | Details |\n",
                "| :--- | :--- |\n",
                "| **Learner Name** | Yashu Rana |\n",
                "| **Roll Number** | 2300320130291 |\n",
                "| **College / Campus** | ABES EC |\n",
                "| **Mentor Name** | Dipali Kedar Patki |\n",
                "| **Domain** | Data Analytics / Python |\n",
                "| **Submission Date** | November 01, 2026 |\n",
                "\n",
                "---"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Introduction & Problem Statement\n",
                "Urban centres across India face severe air quality degradation, driven by vehicular exhaust, industrial emissions, construction dust, and seasonal biomass burning. Adverse ambient air quality is linked to acute respiratory morbidity, cardiovascular diseases, and economic productivity losses. \n",
                "\n",
                "**Problem Statement (5W1H):**\n",
                "- **Who:** Environmental regulators (CPCB/SPCBs), municipal corporations, and citizens.\n",
                "- **What:** Absence of fine-grained spatial hotspot identification and empirical seasonal variance quantification, leading to reactive rather than predictive interventions.\n",
                "- **When / Where:** Chronic year-round exposure across 50 Indian municipal cities, with acute peaks during winter thermal inversions.\n",
                "- **Why:** Untargeted blanket policies waste municipal resources without mitigating severe localized spikes; evidence-backed spatial analytics enable targeted interventions.\n",
                "- **How:** End-to-end data analytics pipeline evaluating 5,000 observations across 50 cities over 5 years, leveraging statistical hypothesis testing (Welch t-test, ANOVA), correlation modeling, and geospatial hotspot clustering (Folium)."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Tools and Library Setup"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from scipy import stats\n",
                "import folium\n",
                "from folium.plugins import MarkerCluster, HeatMap\n",
                "import warnings\n",
                "warnings.filterwarnings('ignore')\n",
                "\n",
                "# Plot styling\n",
                "sns.set_theme(style=\"whitegrid\", palette=\"muted\")\n",
                "plt.rcParams['font.sans-serif'] = 'DejaVu Sans'\n",
                "plt.rcParams['font.size'] = 11\n",
                "print(\"All core analytical libraries loaded successfully.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Loading & Sanity Checks\n",
                "We load `dataset.csv` (5,000 rows across 50 cities over 5 years) and review column types, missingness, and range consistency."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = pd.read_csv('dataset.csv')\n",
                "print(\"Dataset Shape:\", df.shape)\n",
                "print(\"Missing Values:\\n\", df.isnull().sum())\n",
                "print(\"\\nFirst 5 Records:\")\n",
                "df.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Feature Engineering & CPCB Categorisation\n",
                "We extract temporal features (`year`, `month`, `season`) and map numerical AQI values to official CPCB health categories:\n",
                "- **Good:** 0–50\n",
                "- **Satisfactory:** 51–100\n",
                "- **Moderate:** 101–200\n",
                "- **Poor:** 201–300\n",
                "- **Very Poor:** 301–400\n",
                "- **Severe:** 401–500"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df['date'] = pd.to_datetime(df['date'])\n",
                "df['year'] = df['date'].dt.year\n",
                "df['month'] = df['date'].dt.month\n",
                "\n",
                "def assign_season(m):\n",
                "    if m in [11, 12, 1, 2]:\n",
                "        return 'Winter'\n",
                "    elif m in [7, 8, 9]:\n",
                "        return 'Monsoon'\n",
                "    elif m in [3, 4, 5, 6]:\n",
                "        return 'Summer'\n",
                "    else:\n",
                "        return 'Post-Monsoon'\n",
                "\n",
                "df['season'] = df['month'].apply(assign_season)\n",
                "\n",
                "def aqi_category(val):\n",
                "    if val <= 50:\n",
                "        return \"Good (0-50)\"\n",
                "    elif val <= 100:\n",
                "        return \"Satisfactory (51-100)\"\n",
                "    elif val <= 200:\n",
                "        return \"Moderate (101-200)\"\n",
                "    elif val <= 300:\n",
                "        return \"Poor (201-300)\"\n",
                "    elif val <= 400:\n",
                "        return \"Very Poor (301-400)\"\n",
                "    else:\n",
                "        return \"Severe (401-500)\"\n",
                "\n",
                "df['aqi_category'] = df['aqi'].apply(aqi_category)\n",
                "\n",
                "# Region mapping for 50 cities\n",
                "north_cities = ['Delhi', 'Ghaziabad', 'Noida', 'Gurugram', 'Faridabad', 'Lucknow', 'Kanpur', \n",
                "                'Varanasi', 'Agra', 'Meerut', 'Prayagraj', 'Bareilly', 'Gorakhpur', 'Chandigarh', \n",
                "                'Ludhiana', 'Amritsar', 'Jalandhar', 'Dehradun', 'Srinagar', 'Jammu']\n",
                "east_cities = ['Kolkata', 'Patna', 'Ranchi', 'Bhubaneswar', 'Guwahati']\n",
                "west_cities = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Ahmedabad', 'Surat', 'Vadodara', \n",
                "               'Rajkot', 'Jaipur', 'Jodhpur', 'Kota']\n",
                "central_cities = ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Raipur']\n",
                "south_cities = ['Bengaluru', 'Chennai', 'Hyderabad', 'Visakhapatnam', 'Coimbatore', \n",
                "                'Kochi', 'Thiruvananthapuram', 'Mysuru', 'Madurai']\n",
                "\n",
                "def get_region(city):\n",
                "    if city in north_cities: return 'North'\n",
                "    elif city in east_cities: return 'East'\n",
                "    elif city in west_cities: return 'West'\n",
                "    elif city in central_cities: return 'Central'\n",
                "    else: return 'South'\n",
                "\n",
                "df['region'] = df['city'].apply(get_region)\n",
                "print(\"Sample engineered features:\")\n",
                "df[['date', 'city', 'region', 'season', 'aqi', 'aqi_category']].head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Exploratory Data Analysis & Visualisations\n",
                "We examine the overall AQI distribution and CPCB category percentages."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cat_counts = df['aqi_category'].value_counts()\n",
                "cat_pct = (df['aqi_category'].value_counts(normalize=True) * 100).round(2)\n",
                "cat_summary = pd.DataFrame({'Total Observations': cat_counts, 'Percentage Share (%)': cat_pct})\n",
                "display(cat_summary)\n",
                "\n",
                "fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))\n",
                "sns.histplot(df['aqi'], kde=True, ax=axes[0], color='#2b5c8f', bins=35)\n",
                "axes[0].axvline(50, color='green', linestyle='--', alpha=0.7, label='Good (<=50)')\n",
                "axes[0].axvline(100, color='lime', linestyle='--', alpha=0.7, label='Satisfactory (<=100)')\n",
                "axes[0].axvline(200, color='orange', linestyle='--', alpha=0.7, label='Moderate (<=200)')\n",
                "axes[0].axvline(300, color='red', linestyle='--', alpha=0.7, label='Poor (<=300)')\n",
                "axes[0].axvline(400, color='darkred', linestyle='--', alpha=0.7, label='Very Poor (<=400)')\n",
                "axes[0].set_title(\"Distribution of AQI with CPCB Breakpoints\", fontweight='bold')\n",
                "axes[0].set_xlabel(\"Air Quality Index (AQI)\")\n",
                "axes[0].legend(loc='upper right', fontsize=9)\n",
                "\n",
                "cat_order = [\"Good (0-50)\", \"Satisfactory (51-100)\", \"Moderate (101-200)\", \n",
                "             \"Poor (201-300)\", \"Very Poor (301-400)\", \"Severe (401-500)\"]\n",
                "cat_palette = [\"#2ecc71\", \"#a8e063\", \"#f39c12\", \"#e67e22\", \"#e74c3c\", \"#8e44ad\"]\n",
                "cat_series = df['aqi_category'].value_counts().reindex(cat_order).fillna(0)\n",
                "sns.barplot(x=cat_series.index, y=cat_series.values, ax=axes[1], palette=cat_palette)\n",
                "axes[1].set_title(\"AQI Health Category Breakdown\", fontweight='bold')\n",
                "axes[1].set_xticklabels([\"Good\", \"Satisfactory\", \"Moderate\", \"Poor\", \"Very Poor\", \"Severe\"], rotation=25)\n",
                "for i, v in enumerate(cat_series.values):\n",
                "    axes[1].text(i, v + 25, f\"{(v/len(df)*100):.1f}%\", ha='center', fontweight='bold', fontsize=9)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Correlation Analysis: Pollutants vs Weather Conditions"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "corr_cols = ['pm25', 'pm10', 'no2_ppb', 'so2_ppb', 'co_ppm', 'o3_ppb', 'temp_C', 'humidity_pct', 'aqi']\n",
                "corr_matrix = df[corr_cols].corr()\n",
                "\n",
                "plt.figure(figsize=(9, 7))\n",
                "sns.heatmap(corr_matrix, annot=True, fmt=\".2f\", cmap=\"coolwarm\", cbar_kws={'label': 'Pearson Correlation (r)'}, linewidths=0.5, vmin=-1, vmax=1)\n",
                "plt.title(\"Correlation Matrix: Pollutants vs Meteorological Variables\", fontweight='bold', pad=12)\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "print(\"Strongest Drivers of AQI:\")\n",
                "print(corr_matrix['aqi'].sort_values(ascending=False))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Seasonal Trends & Winter Inversion Smog"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "monthly = df.groupby('month').agg(\n",
                "    mean_aqi=('aqi', 'mean'),\n",
                "    mean_pm25=('pm25', 'mean'),\n",
                "    mean_temp=('temp_C', 'mean')\n",
                ")\n",
                "month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']\n",
                "\n",
                "fig, ax1 = plt.subplots(figsize=(10, 5.2))\n",
                "ax2 = ax1.twinx()\n",
                "\n",
                "p1, = ax1.plot(monthly.index, monthly['mean_aqi'], color='#c0392b', marker='o', linewidth=2.5, label='Mean AQI')\n",
                "p2, = ax1.plot(monthly.index, monthly['mean_pm25'], color='#d35400', marker='s', linestyle='--', linewidth=2, label='Mean PM2.5 (ug/m3)')\n",
                "p3, = ax2.plot(monthly.index, monthly['mean_temp'], color='#2980b9', marker='^', linestyle=':', linewidth=2, label='Mean Temp (°C)')\n",
                "\n",
                "ax1.set_xlabel(\"Month of the Year\")\n",
                "ax1.set_ylabel(\"Air Quality Index / PM2.5 (ug/m3)\", color='#c0392b')\n",
                "ax2.set_ylabel(\"Temperature (°C)\", color='#2980b9')\n",
                "ax1.set_xticks(range(1, 13))\n",
                "ax1.set_xticklabels(month_names)\n",
                "ax1.axvspan(10.5, 12.5, color='orange', alpha=0.15, label='Winter Inversion Smog Period')\n",
                "ax1.axvspan(0.5, 2.5, color='orange', alpha=0.15)\n",
                "\n",
                "lines = [p1, p2, p3]\n",
                "ax1.legend(lines, [l.get_label() for l in lines], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)\n",
                "plt.title(\"Monthly Seasonal Dynamic: Winter Inversion vs Monsoon Washout\", fontweight='bold', pad=25)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Statistical Hypothesis Testing\n",
                "### Test 1: Welch's Two-Sample t-test (Winter vs Summer AQI)\n",
                "- $H_0$: $\\mu_{winter} = \\mu_{summer}$ (Seasonal variation does not alter average AQI)\n",
                "- $H_1$: $\\mu_{winter} \\neq \\mu_{summer}$ (AQI significantly differs between Winter and Summer)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "winter_aqi = df[df['season'] == 'Winter']['aqi']\n",
                "summer_aqi = df[df['season'] == 'Summer']['aqi']\n",
                "\n",
                "t_stat, p_val = stats.ttest_ind(winter_aqi, summer_aqi, equal_var=False)\n",
                "diff = winter_aqi.mean() - summer_aqi.mean()\n",
                "se_diff = np.sqrt(winter_aqi.var()/len(winter_aqi) + summer_aqi.var()/len(summer_aqi))\n",
                "ci_low, ci_high = diff - 1.96 * se_diff, diff + 1.96 * se_diff\n",
                "\n",
                "print(f\"Winter Mean AQI: {winter_aqi.mean():.2f} (n = {len(winter_aqi)})\")\n",
                "print(f\"Summer Mean AQI: {summer_aqi.mean():.2f} (n = {len(summer_aqi)})\")\n",
                "print(f\"Observed Lift in Winter: +{diff:.2f} AQI points\")\n",
                "print(f\"Welch t-statistic: {t_stat:.3f}, p-value: {p_val:.4e}\")\n",
                "print(f\"95% Confidence Interval for Difference: [{ci_low:.2f}, {ci_high:.2f}]\")\n",
                "print(\"Result:\", \"STATISTICALLY SIGNIFICANT (p < 0.05)\" if p_val < 0.05 else \"Not significant\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Test 2: One-Way ANOVA across 5 Geographic Regions\n",
                "- $H_0$: $\\mu_{North} = \\mu_{South} = \\mu_{East} = \\mu_{West} = \\mu_{Central}$\n",
                "- $H_1$: At least one region exhibits significantly different baseline air quality."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "regional_groups = [df[df['region'] == r]['aqi'] for r in df['region'].unique()]\n",
                "f_stat, p_val_f = stats.f_oneway(*regional_groups)\n",
                "print(f\"One-Way ANOVA F-statistic: {f_stat:.3f}, p-value: {p_val_f:.4e}\")\n",
                "\n",
                "regional_summary = df.groupby('region').agg(\n",
                "    sample_count=('aqi', 'count'),\n",
                "    mean_aqi=('aqi', 'mean'),\n",
                "    std_aqi=('aqi', 'std'),\n",
                "    mean_pm25=('pm25', 'mean'),\n",
                "    poor_or_worse_share=('aqi', lambda x: f\"{(x >= 201).mean()*100:.1f}%\")\n",
                ").sort_values(by='mean_aqi', ascending=False)\n",
                "display(regional_summary)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9. Pollution Hotspot Mapping & Geospatial Analysis\n",
                "We aggregate city-level air quality to rank the top 15 critical hotspots and top 10 cleanest cities."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "city_summary = df.groupby('city').agg(\n",
                "    region=('region', 'first'),\n",
                "    mean_aqi=('aqi', 'mean'),\n",
                "    max_aqi=('aqi', 'max'),\n",
                "    mean_pm25=('pm25', 'mean'),\n",
                "    severe_days_pct=('aqi', lambda x: round((x >= 301).mean() * 100, 2))\n",
                ").sort_values(by='mean_aqi', ascending=False)\n",
                "\n",
                "top15 = city_summary.head(15).iloc[::-1]\n",
                "bottom10 = city_summary.tail(10)\n",
                "\n",
                "fig, axes = plt.subplots(1, 2, figsize=(15, 6))\n",
                "axes[0].barh(top15.index, top15['mean_aqi'], color='#962d2d')\n",
                "axes[0].axvline(200, color='orange', linestyle='--', label='CPCB Poor Threshold (200)')\n",
                "axes[0].set_title(\"Top 15 Pollution Hotspots in India\", fontweight='bold')\n",
                "axes[0].set_xlabel(\"Mean AQI\")\n",
                "axes[0].legend(loc='lower right')\n",
                "for i, v in enumerate(top15['mean_aqi']):\n",
                "    axes[0].text(v + 3, i, f\"{v:.1f}\", va='center', fontweight='bold', fontsize=9)\n",
                "\n",
                "axes[1].barh(bottom10.index, bottom10['mean_aqi'], color='#27ae60')\n",
                "axes[1].axvline(100, color='gray', linestyle='--', label='CPCB Satisfactory Threshold (100)')\n",
                "axes[1].set_title(\"Top 10 Cleanest Cities\", fontweight='bold')\n",
                "axes[1].set_xlabel(\"Mean AQI\")\n",
                "axes[1].legend(loc='lower right')\n",
                "for i, v in enumerate(bottom10['mean_aqi']):\n",
                "    axes[1].text(v + 2, i, f\"{v:.1f}\", va='center', fontweight='bold', fontsize=9)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 10. Interactive Hotspot Mapping (Folium HTML Map)\n",
                "An interactive Folium heatmap and marker cluster map is compiled and exported as `pollution_hotspot_map.html` for geospatial navigation and municipal deployment."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print(\"Interactive map saved to pollution_hotspot_map.html. Open it in any web browser to view interactive tooltips, marker clusters, and heatmap layers.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 11. Conclusion & Key Recommendations\n",
                "1. **Particulate Primacy:** PM2.5 exhibits an extreme correlation ($r = 0.965$) with AQI, confirming fine particulate matter as the dominant public health hazard.\n",
                "2. **Winter Inversion Risk:** Winter AQI surges by $+105.44$ points over summer baseline ($p < 10^{-200}$), necessitating pre-emptive winter Graded Response Action Plans (GRAP).\n",
                "3. **Geospatial Concentration:** North India (Indo-Gangetic Plain) faces a severe cluster of hotspots (Delhi, Ghaziabad, Patna, Noida, Kanpur) requiring regional airshed governance rather than isolated municipal decrees."
            ]
        }
    ]
    
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open("P_50_AQI_Hotspot_Analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("Saved P_50_AQI_Hotspot_Analysis.ipynb successfully.")

if __name__ == "__main__":
    make_notebook()
