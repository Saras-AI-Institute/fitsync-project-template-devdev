# 🔶 FitSync — Personal Health Analytics

| Status | Week | Description | State |
| :---: | :---: | :--- | :---: |
| ✅ | Week 1 | Setup and created dataset using generator | Done |
| ✅ | Week 2 | Process Dataset using Python | Done |
| ✅ | Week 3 | Build Streamlit UI and KPI metrics | Done |
| ✅ | Week 4 | Add Plotly visualizations & caching optimizations | Done |
| ✅ | Week 5 | Finalize documentation and deploy live | Done |

## Repository structure
* `main.py` — Landing / marketing page (hero, features, how it works, preview, CTA)
* `pages/1_Dashboard.py` — Primary dashboard page (KPIs + charts)
* `pages/2_Trends.py` — Trends and statistical views
* `modules/processor.py` — Data loading, cleaning and Recovery_Score logic
* `modules/theme.py` — Theme helpers and Plotly styling utility
* `generate_data.py` — Synthetic dataset generator (writes `data/health_data.csv`)
* `data/health_data.csv` — Sample dataset used by the app
* `.streamlit/config.toml` — Streamlit native theme settings
* `requirements.txt` — Python dependencies
* `README.md` — This file

## Quick start (local)

Create and activate a Python virtual environment (Windows example):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

(Optional) regenerate the sample dataset:
```bash
python generate_data.py
```

Run the app with Streamlit from the repo root:
```bash
streamlit run main.py
```

Or open the dashboard pages directly:
```bash
streamlit run pages/1_Dashboard.py
streamlit run pages/2_Trends.py
```

## Notes for developers
* **Data pipeline:** `modules/processor.py` reads `data/health_data.csv`, fills missing values, converts `Date` to datetime, and computes `Recovery_Score`.
* **Caching:** pages now use `@st.cache_data` (see `pages/1_Dashboard.py` and `pages/2_Trends.py`) to cache processed data for faster UI responsiveness. Cached results are `.copy()`-ed before per-page filtering to avoid mutating the cached object.
* **Plotly styling:** a helper `style_plotly_chart(fig)` is available in `modules/theme.py` to ensure charts respect the active theme.
* **Theme:** `.streamlit/config.toml` sets the native Streamlit theme; `modules/theme.py` applies minimal CSS overrides and a sidebar toggle that persists in `st.session_state['theme']`.

## Tests & validation
Simple smoke tests are available in `test.py` / `test1.py` which demonstrate data loading and basic checks. Use `pytest` to run unit tests in `tests/test_processor.py`:
```bash
pytest tests/test_processor.py -v
```
