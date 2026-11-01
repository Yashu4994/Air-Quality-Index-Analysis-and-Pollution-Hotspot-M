# 🚀 Step-by-Step GitHub Upload Guide for Yashu Rana

This guide walks you through uploading your completed **Air Quality Index Analysis and Pollution Hotspot Mapping** project directly to your GitHub repository.

---

### Step 1: Open Your Terminal
Open the Terminal application on your Mac (or in your IDE terminal). Ensure you are inside the project directory:
```bash
cd "/Users/yashurana/Documents/HCL Career Shaper"
```

---

### Step 2: Initialize Git Repository
Run the following commands to initialize Git and create your initial commit:

```bash
# 1. Initialize a new git repository
git init

# 2. Add all project files (dataset, code, figures, docs, notebook)
git add .

# 3. Check what is staged (you should see all project files, .venv is ignored by .gitignore)
git status

# 4. Create your initial commit
git commit -m "Initial commit: Air Quality Index Analysis and Pollution Hotspot Mapping project"
```

---

### Step 3: Create a Repository on GitHub
1. Open your browser and go to: **[https://github.com/new](https://github.com/new)**
2. In **Repository name**, enter:
   ```
   Air_Quality_Index_Analysis_and_Pollution_Hotspot_Mapping
   ```
   *(or `HCL_Career_Shaper_AQI_Project` if you prefer a shorter name)*
3. Choose **Public** (recommended for evaluation and portfolio submission).
4. **DO NOT** check "Add a README file", "Add .gitignore", or "Choose a license" (we already created all of these files locally!).
5. Click the green **Create repository** button.

---

### Step 4: Link Your Local Code to GitHub & Push
GitHub will display your repository URL (e.g. `https://github.com/YOUR_USERNAME/Air_Quality_Index_Analysis_and_Pollution_Hotspot_Mapping.git`).

Run the following commands in your terminal (replace `YOUR_USERNAME` with your real GitHub username):

```bash
# 1. Rename default branch to main
git branch -M main

# 2. Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/Air_Quality_Index_Analysis_and_Pollution_Hotspot_Mapping.git

# 3. Push all files to GitHub
git push -u origin main
```

*(If prompted for credentials, use your GitHub Personal Access Token or sign in via GitHub CLI / browser).*

---

### Step 5: Verification Checklist
Once pushed, open your repository link on GitHub and verify:
- [x] `README.md` renders cleanly with badges, tables, and embedded figures.
- [x] `dataset.csv` (5,000 rows) and `data_dictionary.csv` are present.
- [x] `P_50_AQI_Hotspot_Analysis.ipynb` is viewable directly in GitHub's notebook viewer.
- [x] `Project_Report_Yashu_Rana_2300320130291.docx` and `Project_Synopsis_Yashu_Rana_2300320130291.docx` are ready for download.
- [x] `pollution_hotspot_map.html` is present for geospatial demonstration.
- [x] All 6 chart PNG files are located in `figures/`.

---

### 📁 Files Ready for HCLTech Submission Portal:
When submitting on your college / HCLTech portal, upload:
1. **Synopsis:** `Project_Synopsis_Yashu_Rana_2300320130291.docx`
2. **Report:** `Project_Report_Yashu_Rana_2300320130291.docx`
3. **Dataset & Schema:** `dataset.csv` and `data_dictionary.csv`
4. **Notebook:** `P_50_AQI_Hotspot_Analysis.ipynb`
5. **Interactive Map:** `pollution_hotspot_map.html`
6. **GitHub Link:** Your GitHub repository URL
