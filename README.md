# 🔶 FitSync — Personal Health Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

FitSync is an end-to-end personal health analytics web application built with **Streamlit**, **Pandas**, and **Plotly**. It ingests longitudinal wearable biometrics (steps, sleep duration, resting heart rate, active minutes, and calories burned), imputes missing sensor telemetry, computes an algorithmic **Recovery Score** (0–100), and presents actionable insights across a multipage dashboard.

---

## 📅 Project Milestones & Progress

| Status | Milestone | Deliverable / Highlights | State |
| :---: | :--- | :--- | :---: |
| ✅ | **Week 1** | Project scaffolding, git repo setup, and synthetic dataset generator (`generate_data.py`) | **Done** |
| ✅ | **Week 2** | Python data cleaning pipeline & algorithmic `Recovery_Score` engine (`modules/processor.py`) | **Done** |
| ✅ | **Week 3** | Multipage Streamlit UI structure, landing hero page, and core KPI metrics | **Done** |
| ✅ | **Week 4** | Interactive Plotly data visualizations & `@st.cache_data` performance optimizations | **Done** |
| ✅ | **Week 5** | Final documentation, automated test suite (`pytest`), and live cloud deployment | **Done** |

---

## 🏛️ Repository Structure

```text
fitsync-project/
├── .streamlit/
│   └── config.toml             # Streamlit native theme & server configuration
├── data/
│   ├── .gitkeep                # Git tracking placeholder
│   └── health_data.csv         # 365-day wearable biometric dataset
├── modules/
│   ├── __init__.py             # Module package initializer
│   ├── processor.py            # Data loading, imputation, & Recovery_Score logic
│   └── theme.py                # Theme helpers, CSS injection, & Plotly chart styling
├── pages/
│   ├── 1_Dashboard.py          # Primary dashboard (KPI metric cards & trend charts)
│   ├── 2_Trends.py             # Statistical distributions, monthly views & correlation
│   └── __init__.py             # Pages package initializer
├── tests/
│   └── test_processor.py       # Pytest unit tests for processor module
├── generate_data.py            # Synthetic dataset generator script
├── main.py                     # Landing / marketing page (Hero, features, overview)
├── requirements.txt            # Project dependencies for local & cloud environments
├── sample_data.py              # Quick inspection & null analysis helper
├── test.py                     # Smoke test for data pipeline loading
├── test1.py                    # Smoke test for recovery scoring logic
└── README.md                   # Complete project documentation & deployment guide
```

---

## ⚙️ Data Pipeline & Recovery Score Logic

### 1. Missing Value Imputation (`modules/processor.py`)
Wearable sensors frequently miss data due to battery depletion or movement artifacts. FitSync cleanses incoming data using clinical and statistical heuristics:
- **`Steps`**: Imputed with the column median.
- **`Sleep_Hours`**: Imputed with healthy baseline default of **7.0 hours**.
- **`Heart_Rate_bpm`**: Imputed with resting baseline default of **68.0 bpm**.
- **`Calories_Burned`** & **`Active_Minutes`**: Imputed with their respective medians.
- **`Date`**: Parsed to `datetime64[ns]` and sorted chronologically.

### 2. Recovery Score Algorithm
The composite score starts at a baseline of **50 points** and evaluates three physiological pillars, strictly clipped to $[0, 100]$:

$$\text{Recovery Score} = \text{clip}\left(50 + \Delta_{\text{sleep}} + \Delta_{\text{HR}} + \Delta_{\text{steps}},\, 0,\, 100\right)$$

* **Sleep Hours Factor ($\Delta_{\text{sleep}}$)**:
  * $\ge 7.0$ hours: $+20$ points (optimal recovery)
  * $< 6.0$ hours: $-20$ points (sleep deficit)
* **Resting Heart Rate Factor ($\Delta_{\text{HR}}$)**:
  * $< 60$ bpm: $+10$ points (athletic / low strain)
  * $> 80$ bpm: $-10$ points (elevated cardiovascular strain)
* **Daily Steps Factor ($\Delta_{\text{steps}}$)**:
  * $8,000 \le \text{steps} \le 12,000$: $+10$ points (optimal movement target)
  * $< 4,000$: $-5$ points (sedentary day)
  * $> 16,000$: $-5$ points (excessive strain / overexertion)

---

## 🌟 Key Application Features

1. **Landing & Marketing Page (`main.py`)**:
   - Polished hero banner, value proposition, and feature grid.
   - Quick KPI summary snapshot across the full dataset.
   - 3-step walkthrough and expandable processed data preview.
2. **Primary Health Dashboard (`pages/1_Dashboard.py`)**:
   - Interactive time window filters: *Last 7 Days*, *Last 30 Days*, *Last 90 Days*, *All Time*.
   - Dynamic KPI metric cards with status deltas against healthy benchmarks.
   - Dual-axis interactive line chart tracking Recovery Score alongside Sleep Duration.
   - Scatter plot correlating daily steps against recovery, sized by active minutes.
   - Energy expenditure analysis and resting heart rate distribution.
   - Filtered dataset preview with one-click **CSV export**.
3. **Trends & Statistical Insights (`pages/2_Trends.py`)**:
   - Five-number statistical summary across all biometric variables.
   - Histograms for steps and calories with annotated mean reference lines.
   - Sleep duration longitudinal trend with 7-hour baseline target.
   - Monthly aggregated recovery score bar chart (formatted to avoid serialization bugs).
   - Pearson correlation heatmap between all biometric features.
   - Day-of-week behavioral analysis (weekday vs. weekend patterns).
4. **Performance & Theme System (`modules/theme.py`)**:
   - Native caching via `@st.cache_data` ensures instantaneous page transitions.
   - Defensively applies `.copy()` on cached DataFrames before filtering.
   - Dark 🌙 and Light ☀️ theme switcher with persistent session state.
   - Helper function `style_plotly_chart(fig)` unifies chart backgrounds, axes, fonts, and hover tooltips.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/Saras-AI-Institute/fitsync-project-firstname-lastname.git
cd fitsync-project-firstname-lastname
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Regenerate Synthetic Data
```bash
python generate_data.py
```

### 5. Launch the Streamlit Application
```bash
streamlit run main.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Testing & Validation

FitSync includes smoke tests and a complete `pytest` test suite:

### Run Smoke Tests
```bash
# Test data ingestion & cleaning
python test.py

# Test recovery score algorithm
python test1.py
```

### Run Pytest Suite
```bash
pytest tests/test_processor.py -v
```

---

## 🌐 Live Cloud Deployment Guide

Deploy your FitSync app live to **Streamlit Community Cloud** (100% free) in 3 simple steps:

### Step 1: Push Code to GitHub
Ensure all your project changes are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Finalize Week 5: Documentation, tests, and live deployment setup"
git push origin main
```

### Step 2: Connect to Streamlit Community Cloud
1. Navigate to [share.streamlit.io](https://share.streamlit.io/) and click **Sign In** (use your GitHub account).
2. Click the **"New app"** button in your dashboard.
3. Select your repository: `fitsync-project-<firstname>-<lastname>`.
4. Set the **Branch** to `main`.
5. Set the **Main file path** to `main.py`.
6. (Optional) Customize the App URL if desired (e.g. `fitsync-analytics.streamlit.app`).

### Step 3: Click "Deploy!"
Streamlit Cloud will automatically detect `requirements.txt`, install dependencies, and launch your application. Your live URL will be active immediately!

> **Live Application URL:** `https://share.streamlit.io/` *(Update with your deployed link)*

---

## 🛠️ Tech Stack & Libraries

- **Language:** Python 3.10+
- **Frontend / App Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive Visualizations:** [Plotly Express & Graph Objects](https://plotly.com/python/)
- **Testing:** [Pytest](https://docs.pytest.org/)

---

## 🎓 Course & Academic Credits

- **Course:** Code with AI
- **Institution:** [Saras AI Institute](https://sarasai.org/)
- **Instructor / Curriculum:** Personal Health Analytics Module
