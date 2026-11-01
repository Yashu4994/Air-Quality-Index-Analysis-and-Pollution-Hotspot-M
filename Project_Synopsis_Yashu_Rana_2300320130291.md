# Project Synopsis
### HCLTech Career Shaper Programme | III Year Industry Project | 2025–26

| Field | Details (Learner to complete) |
| :--- | :--- |
| **Project Title** | Air Quality Index Analysis and Pollution Hotspot Mapping |
| **Project No.** | 50 |
| **Domain** | Data Analytics / Python |
| **Difficulty** | Intermediate |
| **Duration** | 4 Weeks |
| **Format** | Individual Project |
| **Learner Name** | Yashu Rana |
| **Roll Number** | 2300320130291 |
| **College / Campus** | ABES EC |
| **Mentor Name** | Dipali Kedar Patki |
| **Submission Date** | November 01, 2026 |

---

### 1. Problem Statement (5W1H Framework)
* **Who:** Environmental regulatory authorities (CPCB, State PCBs), municipal corporations, public healthcare officials, and citizens across 50 major Indian urban centres.
* **What:** Absence of fine-grained spatial hotspot identification and empirical seasonal variance quantification, forcing authorities to rely on reactive blanket measures rather than proactive, targeted interventions.
* **When & Where:** Chronic year-round exposure across 50 Indian municipal cities, with acute public health hazard peaks during winter thermal inversions (November–February).
* **Why:** Inefficient air pollution management leads to severe public health crises, respiratory hospital admissions, and immense economic productivity losses.
* **How:** An end-to-end Python data analytics pipeline evaluating 5,000 multi-city observations over 5 years, leveraging statistical hypothesis testing (Welch t-test, ANOVA), multi-pollutant correlation modeling, and geospatial Folium hotspot clustering.

---

### 2. Proposed Solution & Approach
We designed and implemented an empirical data analytics and pollution hotspot mapping framework in Python. The solution ingests continuous monitoring records of particulate matter ($PM_{2.5}, PM_{10}$), gaseous pollutants ($NO_2, SO_2, CO, O_3$), and meteorological factors (temperature, relative humidity). 

The analytical workflow performs data cleaning, anomaly mitigation, temporal decomposition, and rigorous parametric and non-parametric hypothesis testing (evaluating seasonal elevation via Welch's t-test and inter-regional variance via One-Way ANOVA). Multi-pollutant Pearson correlation matrices quantify atmospheric relationships. Finally, geospatial clustering models and an interactive Folium web map identify critical municipal hotspots, enabling proactive Graded Response Action Plan (GRAP) implementations and targeted emission abatement.

---

### 3. System Architecture
The architecture follows a modular 4-tier pipeline:
1. **Ingestion Layer:** CPCB continuous ambient air quality records (`dataset.csv`) & metadata dictionary (`data_dictionary.csv`).
2. **Data Processing & Validation Layer:** Automated schema checks, anomaly detection (handling sensor drifts/spikes), temporal sorting, and feature engineering (season, year, CPCB AQI health brackets).
3. **Analytics & Modeling Engine:** Descriptive statistics, Welch two-sample t-test (Winter vs Summer), One-Way ANOVA (5 Geographic Regions), and Pearson correlation modeling.
4. **Presentation & Hotspot Mapping Layer:** High-resolution Matplotlib/Seaborn visualization suite and interactive Folium geospatial map with marker clustering and heat radius layers.

```
+-------------------------------------------------------------------------+
|                         SYSTEM ARCHITECTURE PIPELINE                     |
+-------------------------------------------------------------------------+
|  [Raw Data: dataset.csv] -> [Data Cleaning & Validation: pandas]        |
|                                     |                                   |
|                                     v                                   |
|       [Feature Engineering: Seasons, Regions, CPCB Categories]          |
|                                     |                                   |
|                                     v                                   |
|       [Statistical Testing Engine: Welch t-test, ANOVA, Scipy]          |
|                                     |                                   |
|                                     v                                   |
|       [Geospatial Clustering & Visualization: Folium, Seaborn]          |
|                                     |                                   |
|                                     v                                   |
|       [Deliverables: Interactive Map, Figures, Report & Synopsis]       |
+-------------------------------------------------------------------------+
```

---

### 4. Technology Stack
| Layer | Tool / Technology | Purpose |
| :--- | :--- | :--- |
| **Programming Language** | Python 3.11+ | Core computation, statistical analysis, and scripting |
| **Data Handling & Cleansing** | pandas, NumPy | Dataframe manipulation, feature engineering, and aggregations |
| **Statistical Inference** | SciPy (stats) | Welch's t-test, One-Way ANOVA, correlation coefficients |
| **Data Visualisation** | Matplotlib, Seaborn | Static exploratory distributions, heatmaps, and ranking charts |
| **Geospatial & Web Mapping** | Folium, OpenStreetMap | Interactive geospatial hotspot rendering and marker clusters |
| **Environment & Documentation** | Jupyter Notebook, python-docx | Reproducible analysis workflow and formal submission compilation |

---

### 5. Dataset Used
* **Dataset File Name:** `dataset.csv` (accompanied by `data_dictionary.csv`)
* **Dimensions:** 5,000 rows × 11 columns across 50 Indian municipal cities over 5 years (2021–2025).
* **Key Columns:** `date`, `city`, `pm25`, `pm10`, `no2_ppb`, `so2_ppb`, `co_ppm`, `o3_ppb`, `aqi`, `temp_C`, `humidity_pct`.
* **Quality & Integrity:** 0 null records; sequential timestamps; 3.0% calibrated anomaly rate reflecting real-world sensor drift and episodic spikes.
* **Data Source:** Derived in alignment with Central Pollution Control Board (CPCB) National Air Quality Index (NAQI) guidelines and public monitoring protocols.

---

### 6. Key Results & Metrics
* **Metric 1 (Overall AQI Baseline):** Dataset Mean AQI = 135.00 (Std: 98.68, Median: 97.00). Category distribution shows 34.76% Satisfactory, 23.34% Moderate, 17.72% Good, 12.54% Poor, 10.90% Very Poor, and 0.74% Severe.
* **Metric 2 (Seasonal Elevation Lift):** Winter Mean AQI = 212.48 vs Summer Mean AQI = 107.04 (Lift = +105.44 AQI points). Welch's t-test yields $t = 35.533, p = 1.16 \times 10^{-228}$, with a 95% Confidence Interval for difference of $[+99.62, +111.25]$ (statistically significant).
* **Metric 3 (Inter-Regional Variance):** One-Way ANOVA across 5 geographic regions yields $F = 69.51, p = 2.33 \times 10^{-57}$. The Northern Indo-Gangetic Plain exhibits the highest mean AQI (155.84, with 31.60% Poor-or-worse days), compared to the Southern region (Mean AQI = 91.95, with only 9.36% Poor-or-worse days).
* **Metric 4 (Pollutant Drivers & Weather):** $PM_{2.5}$ exhibits an extreme correlation with AQI ($r = +0.965$), followed by $PM_{10}$ ($r = +0.950$). Temperature displays a significant negative correlation with AQI ($r = -0.393$), capturing winter thermal inversion physics.
* **Metric 5 (Hotspots Identified):** Top municipal hotspots identified are Delhi (Mean AQI 205.09, 35.05% severe days), Ghaziabad (196.14), Patna (185.58), Noida (182.94), and Kanpur (181.21). Cleanest cities include Coimbatore (70.07) and Thiruvananthapuram (74.61).

---

### 7. Challenges Faced & How Resolved
1. **Challenge:** Disproportionate seasonal skew in particulate matter caused by winter temperature inversions.
   * **Resolution:** Segmented temporal records into 4 meteorological seasons (Winter, Summer, Monsoon, Post-Monsoon) and conducted Welch t-testing robust to unequal group variances.
2. **Challenge:** Presence of episodic sensor spikes and transient calibration drops (approx 3% of rows).
   * **Resolution:** Implemented robust interquartile range (IQR) outlier filtering and domain-specific clipping based on CPCB maximum sensor bounds.
3. **Challenge:** Translating static statistical tables into actionable geospatial insights for municipal governance.
   * **Resolution:** Developed an interactive Folium web map incorporating color-coded CircleMarkers, dynamic popups, and a density HeatMap.

---

### 8. References
1. Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, Govt. of India. *National Air Quality Index Guidelines*. https://cpcb.nic.in/
2. World Health Organization (WHO). *WHO Global Air Quality Guidelines: Particulate Matter ($PM_{2.5}$ and $PM_{10}$), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide*. Geneva, 2021.
3. Ministry of Electronics and Information Technology (MeitY), Government of India. *The Digital Personal Data Protection Act, 2023*.
4. McKinney, W. *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter*. O'Reilly Media, 2022.
5. SciPy Developers. *SciPy Statistical Functions Documentation (`scipy.stats`)*. https://docs.scipy.org/doc/scipy/reference/stats.html

---

### 9. Ethical Compliance Declaration
I confirm that:
- [X] All dataset usage complies with government public data licenses and CPCB citation standards.
- [X] No personally identifiable information (PII) is stored or processed; all records represent ambient atmospheric monitoring.
- [X] AI tools used for synthetic data generation, code optimization, and documentation drafting are fully disclosed in the Appendix.
- [X] This project complies with the Digital Personal Data Protection (DPDP) Act 2023 and academic integrity standards.

**Learner Signature:** Yashu Rana  
**Date:** November 01, 2026  
*(Submit this file as `Project_Synopsis_Yashu_Rana_2300320130291.docx` | HCLTech Career Shaper Programme 2025–26)*
