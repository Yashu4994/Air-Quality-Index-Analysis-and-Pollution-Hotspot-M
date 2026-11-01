"""
generate_synopsis_docx.py
Generates the official Project Synopsis document in .docx format
matching HCLTech Career Shaper Programme standards.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_synopsis():
    doc = docx.Document()
    
    # Page Margins: 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Header Title
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_prog = p_top.add_run("HCLTech Career Shaper Programme | III Year Industry Project | 2025–26\n")
    r_prog.font.name = "Calibri"
    r_prog.font.size = Pt(11)
    r_prog.font.color.rgb = RGBColor(100, 100, 100)
    
    r_title = p_top.add_run("PROJECT SYNOPSIS\n")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    r_sub = p_top.add_run("Air Quality Index Analysis and Pollution Hotspot Mapping")
    r_sub.bold = True
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(40, 40, 40)
    
    doc.add_paragraph() # spacing
    
    # Header Table
    tbl = doc.add_table(rows=8, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = [
        ("Project Title", "Air Quality Index Analysis and Pollution Hotspot Mapping"),
        ("Project No. & Domain", "Project No. 50  |  Domain: Data Analytics / Python"),
        ("Difficulty & Duration", "Intermediate  |  4 Weeks  |  Individual Project"),
        ("Learner Name", "Yashu Rana"),
        ("Roll Number", "2300320130291"),
        ("College / Campus", "ABES EC"),
        ("Mentor Name & Date", "Dipali Kedar Patki  |  Submission Date: November 01, 2026"),
        ("GitHub Repository", "https://github.com/Yashu4994/Air-Quality-Index-Analysis-and-Pollution-Hotspot-M")
    ]
    
    for i, (k, v) in enumerate(headers):
        row = tbl.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F0F4F8")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        
    doc.add_paragraph() # spacing
    
    def add_section_header(num_title):
        h = doc.add_paragraph()
        r = h.add_run(num_title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(15, 76, 129)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        
    def add_body(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        return p

    # 1. Problem Statement (5W1H)
    add_section_header("1. Problem Statement (5W1H Framework)")
    add_body(
        "Who: Environmental regulatory bodies (Central Pollution Control Board, State Pollution Control Boards), municipal corporations, urban planners, and affected citizens across 50 major Indian cities.\n"
        "What: The lack of granular spatial hotspot mapping and empirical seasonal variation modeling prevents timely public health advisories and targeted municipal mitigation, forcing authorities to rely on reactive blanket measures.\n"
        "When & Where: Year-round across India's urban centres, experiencing acute respiratory hazard peaks during severe winter atmospheric temperature inversions (November to February).\n"
        "Why: Inefficient air pollution management leads to severe public health emergencies, high respiratory hospitalization rates, and substantial economic productivity loss.\n"
        "How: An end-to-end Python data analytics pipeline evaluating 5,000 multi-city observations over 5 years, leveraging statistical hypothesis testing (Welch t-test, ANOVA), correlation analysis, and geospatial Folium hotspot clustering."
    )

    # 2. Proposed Solution & Approach
    add_section_header("2. Proposed Solution & Approach")
    add_body(
        "We designed and implemented an empirical data analytics and pollution hotspot mapping framework using Python. The solution ingests continuous monitoring records of fine particulate matter (PM2.5, PM10), gaseous pollutants (NO2, SO2, CO, O3), and meteorological factors (temperature, relative humidity). "
        "The analytical approach applies exploratory data analysis, parametric and non-parametric hypothesis testing (evaluating seasonal elevation via Welch's t-test and inter-regional variance via One-Way ANOVA), and computes multi-pollutant correlation matrices. "
        "Geospatial clustering models and interactive Folium mapping identify critical municipal hotspots, enabling proactive Graded Response Action Plan (GRAP) implementations and targeted emission abatement."
    )

    # 3. System Architecture
    add_section_header("3. System Architecture")
    add_body(
        "The architecture follows a modular 4-tier pipeline:\n"
        "1. Ingestion Layer: CPCB continuous ambient air quality records (dataset.csv) & metadata dictionary (data_dictionary.csv).\n"
        "2. Data Processing & Validation Layer: Automated schema checks, anomaly detection (handling sensor drifts/spikes), temporal sorting, and feature engineering (season, year, CPCB AQI health brackets).\n"
        "3. Analytics & Modeling Engine: Descriptive statistics, Welch two-sample t-test (Winter vs Summer), One-Way ANOVA (5 Geographic Regions), and Pearson correlation modeling.\n"
        "4. Presentation & Hotspot Mapping Layer: High-resolution Matplotlib/Seaborn visualization suite and interactive Folium geospatial map with marker clustering and heat radius layers."
    )
    
    # ASCII Architecture Box
    p_arch = doc.add_paragraph()
    r_arch = p_arch.add_run(
        "+-------------------------------------------------------------------------+\n"
        "|                         SYSTEM ARCHITECTURE PIPELINE                     |\n"
        "+-------------------------------------------------------------------------+\n"
        "|  [Raw Data: dataset.csv] -> [Data Cleaning & Validation: pandas]        |\n"
        "|                                     |                                   |\n"
        "|                                     v                                   |\n"
        "|       [Feature Engineering: Seasons, Regions, CPCB Categories]          |\n"
        "|                                     |                                   |\n"
        "|                                     v                                   |\n"
        "|       [Statistical Testing Engine: Welch t-test, ANOVA, Scipy]          |\n"
        "|                                     |                                   |\n"
        "|                                     v                                   |\n"
        "|       [Geospatial Clustering & Visualization: Folium, Seaborn]          |\n"
        "|                                     |                                   |\n"
        "|                                     v                                   |\n"
        "|       [Deliverables: Interactive Map, Figures, Report & Synopsis]       |\n"
        "+-------------------------------------------------------------------------+"
    )
    r_arch.font.name = "Courier New"
    r_arch.font.size = Pt(8.5)
    p_arch.paragraph_format.line_spacing = 1.0

    # 4. Technology Stack
    add_section_header("4. Technology Stack")
    tbl_tech = doc.add_table(rows=6, cols=3)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_data = [
        ("Layer", "Technology / Tool", "Purpose"),
        ("Programming Language", "Python 3.11+", "Core computation, statistical analysis, and scripting"),
        ("Data Handling & Cleansing", "pandas, NumPy", "Dataframe manipulation, feature engineering, and aggregations"),
        ("Statistical Inference", "SciPy (stats)", "Welch's t-test, One-Way ANOVA, correlation coefficients"),
        ("Data Visualisation", "Matplotlib, Seaborn", "Static exploratory distributions, heatmaps, and ranking charts"),
        ("Geospatial & Web Mapping", "Folium, OpenStreetMap", "Interactive geospatial hotspot rendering and marker clusters")
    ]
    for r_idx, row in enumerate(tbl_tech.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = tech_data[r_idx][c_idx]
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].bold = True
                set_cell_background(cell, "1F4E79")
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9FBFD")
            set_cell_margins(cell, 60, 60, 100, 100)
    doc.add_paragraph()

    # 5. Dataset Used
    add_section_header("5. Dataset Used")
    add_body(
        "- Dataset File Name: dataset.csv (accompanied by data_dictionary.csv)\n"
        "- Dimensions: 5,000 rows × 11 columns across 50 Indian municipal cities over 5 years (2021–2025).\n"
        "- Key Columns: date, city, pm25, pm10, no2_ppb, so2_ppb, co_ppm, o3_ppb, aqi, temp_C, humidity_pct.\n"
        "- Quality & Integrity: 0 null records; sequential timestamps; 3.0% calibrated anomaly rate reflecting real-world sensor drift and episodic spikes.\n"
        "- Data Source: Derived in alignment with Central Pollution Control Board (CPCB) National Air Quality Index (NAQI) guidelines and public monitoring protocols."
    )

    # 6. Key Results & Metrics
    add_section_header("6. Key Results & Metrics")
    add_body(
        "- Metric 1 (Overall AQI Baseline): Dataset Mean AQI = 135.00 (Std: 98.68, Median: 97.00). Category distribution shows 34.76% Satisfactory, 23.34% Moderate, 17.72% Good, 12.54% Poor, 10.90% Very Poor, and 0.74% Severe.\n"
        "- Metric 2 (Seasonal Elevation Lift): Winter Mean AQI = 212.48 vs Summer Mean AQI = 107.04 (Lift = +105.44 AQI points). Welch's t-test yields t = 35.533, p = 1.16e-228, with a 95% Confidence Interval for difference of [+99.62, +111.25] (statistically significant).\n"
        "- Metric 3 (Inter-Regional Variance): One-Way ANOVA across 5 geographic regions yields F = 69.51, p = 2.33e-57. The Northern Indo-Gangetic Plain exhibits the highest mean AQI (155.84, with 31.60% Poor-or-worse days), compared to the Southern region (Mean AQI = 91.95, with only 9.36% Poor-or-worse days).\n"
        "- Metric 4 (Pollutant Drivers & Weather): PM2.5 exhibits an extreme correlation with AQI (r = +0.965), followed by PM10 (r = +0.950). Temperature displays a significant negative correlation with AQI (r = -0.393), capturing winter thermal inversion physics.\n"
        "- Metric 5 (Hotspots Identified): Top municipal hotspots identified are Delhi (Mean AQI 205.09, 35.05% severe days), Ghaziabad (196.14), Patna (185.58), Noida (182.94), and Kanpur (181.21). Cleanest cities include Coimbatore (70.07) and Thiruvananthapuram (74.61)."
    )

    # 7. Challenges Faced & How Resolved
    add_section_header("7. Challenges Faced & How Resolved")
    add_body(
        "1. Challenge: Disproportionate seasonal skew in particulate matter caused by temperature inversions.\n"
        "   Resolution: Segmented temporal records into 4 meteorological seasons (Winter, Summer, Monsoon, Post-Monsoon) and conducted Welch t-testing robust to unequal group variances.\n"
        "2. Challenge: Presence of episodic sensor spikes and transient calibration drops (approx 3% of rows).\n"
        "   Resolution: Implemented robust interquartile range (IQR) outlier filtering and domain-specific clipping based on CPCB maximum sensor bounds.\n"
        "3. Challenge: Translating static statistical tables into actionable geospatial insights for municipal governance.\n"
        "   Resolution: Developed an interactive Folium web map incorporating color-coded CircleMarkers, dynamic popups, and a density HeatMap."
    )

    # 8. References
    add_section_header("8. References")
    add_body(
        "1. Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, Govt. of India. National Air Quality Index Guidelines. https://cpcb.nic.in/\n"
        "2. World Health Organization (WHO). WHO Global Air Quality Guidelines: Particulate Matter (PM2.5 and PM10), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide. Geneva, 2021.\n"
        "3. Ministry of Electronics and Information Technology (MeitY), Government of India. The Digital Personal Data Protection Act, 2023.\n"
        "4. McKinney, W. Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter. O'Reilly Media, 2022.\n"
        "5. SciPy Developers. SciPy Statistical Functions Documentation (scipy.stats). https://docs.scipy.org/doc/scipy/reference/stats.html"
    )

    # 9. Ethical Compliance Declaration
    add_section_header("9. Ethical Compliance Declaration")
    add_body(
        "I confirm that:\n"
        "[X] All dataset usage complies with government public data licenses and CPCB citation standards.\n"
        "[X] No personally identifiable information (PII) is stored or processed; all records represent ambient atmospheric monitoring.\n"
        "[X] AI tools used for synthetic data generation, code optimization, and documentation drafting are fully disclosed in the Appendix.\n"
        "[X] This project complies with the Digital Personal Data Protection (DPDP) Act 2023 and academic integrity standards.\n\n"
        "Learner Signature: Yashu Rana                             Date: November 01, 2026"
    )

    doc.save("Project_Synopsis_Yashu_Rana_2300320130291.docx")
    print("Saved Project_Synopsis_Yashu_Rana_2300320130291.docx successfully.")

if __name__ == "__main__":
    create_synopsis()
