# 🌤️ Weather Data Pipeline

A data engineering portfolio project that fetches 48 hours of real weather data for multiple cities, cleans it, and saves it — with a live Streamlit dashboard and GitHub Actions automation.

> **Free. No API key. No account. Just Python.**

---

## 🚀 Live Dashboard

👉 **[View Live Dashboard](https://your-username-weather-pipeline.streamlit.app)**
*(Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) for free)*

---

## 📦 Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| `requests` | API calls |
| `pandas` | Data cleaning |
| `pyarrow` | Parquet storage |
| `streamlit` | Live dashboard |
| `plotly` | Interactive charts |
| [open-meteo.com](https://open-meteo.com) | Free weather API |
| GitHub Actions | Pipeline automation |

---

## 🗂️ Project Structure

```
weather-data-pipeline/
├── config.py         # All settings in one place
├── logger.py         # Logs to terminal + file
├── geocode.py        # City name → coordinates
├── fetch.py          # API call → raw JSON
├── clean.py          # Clean & transform data
├── save.py           # Save to Parquet + CSV
├── run.py            # Pipeline entry point
├── dashboard.py      # Streamlit dashboard
├── requirements.txt
├── .github/
│   └── workflows/
│       └── pipeline.yml   # GitHub Actions
└── data/                  # Auto-created on first run
    ├── weather.parquet
    └── weather.csv
```

---

## ⚡ Quick Start

```bash
# 1. Clone & install
git clone https://github.com/YOUR_USERNAME/weather-data-pipeline.git
cd weather-data-pipeline
pip install -r requirements.txt

# 2. Run pipeline (uses default cities: Lahore, London, New York)
python run.py

# 3. Run for specific cities
python run.py --cities Lahore London "New York" Tokyo Dubai Karachi

# 4. Launch dashboard
streamlit run dashboard.py
```

---

## 🤖 GitHub Actions

Every push to `main` automatically runs the pipeline and commits fresh data back to the repo.

### Manual trigger with custom cities:
1. Go to **Actions** tab on GitHub
2. Click **Weather Data Pipeline**
3. Click **Run workflow**
4. Type your cities → Click **Run workflow**

```
Cities: Lahore London "New York" Tokyo
```

---

## 📊 Dashboard Features

- 4 KPI cards (temperature, humidity, precipitation, wind)
- 4 interactive charts (line, bar, area)
- Filter by city and date range
- Raw data table with CSV download

---

## 🧠 What This Project Demonstrates

- Real API integration (geocoding + weather)
- Modular Python architecture
- Data cleaning with pandas
- Parquet storage format
- CI/CD with GitHub Actions
- Data visualization with Streamlit + Plotly

---

## 📄 License

MIT
