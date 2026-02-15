# Brent Oil Change Point Analysis

A comprehensive analysis project for detecting structural breaks in Brent oil prices and associating them with major geopolitical and economic events.

## Project Overview

This project implements Bayesian change point detection to identify significant shifts in Brent oil price behavior from 1987 to 2022. The analysis quantifies the impact of major events such as wars, OPEC decisions, economic crises, and geopolitical tensions on oil market dynamics.

## Project Structure

```
brent-oil-change-point/
├── data/
│   ├── raw/                    # Original Brent oil price data
│   └── processed/              # Processed data and event associations
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_eda.ipynb           # Exploratory Data Analysis
│   ├── 02_stationarity_analysis.ipynb  # Stationarity testing
│   ├── 03_bayesian_change_point.ipynb  # Bayesian change point detection
│   └── 04_event_association.ipynb     # Event association analysis
├── src/                        # Utility functions and modules
├── dashboard/
│   ├── backend/               # Flask API server
│   └── frontend/              # React dashboard application
└── reports/                    # Analysis reports and documentation
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip3 install -r requirements.txt
# OR if you have pip installed:
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies (for Dashboard)

```bash
cd dashboard/frontend
npm install
```

### 3. Run Analysis Notebooks

Start Jupyter notebook:
```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and run notebooks in order:
1. `01_eda.ipynb` - Exploratory Data Analysis
2. `02_stationarity_analysis.ipynb` - Stationarity Testing
3. `03_bayesian_change_point.ipynb` - Change Point Detection
4. `04_event_association.ipynb` - Event Association

### 4. Run Dashboard

**Backend (Flask):**
```bash
cd dashboard/backend
python3 app.py
# OR use the helper script:
./run.sh
```

The API will be available at `http://localhost:5000`

**Frontend (React):**
```bash
cd dashboard/frontend
npm start
```

The dashboard will be available at `http://localhost:3000`

## Key Features

### Analysis Components

1. **Exploratory Data Analysis**: Comprehensive visualization and summary statistics
2. **Stationarity Testing**: ADF and KPSS tests to understand time series properties
3. **Bayesian Change Point Detection**: PyMC-based model to identify structural breaks
4. **Event Association**: Temporal correlation analysis between change points and events

### Dashboard Features

- Interactive price charts with change point indicators
- Event highlighting and filtering
- Date range selection
- Volatility metrics visualization
- Impact quantification displays

## API Endpoints

- `GET /prices` - Historical Brent oil price data
- `GET /changepoints` - Detected change points with metadata
- `GET /events` - Key geopolitical and economic events
- `GET /associations` - Change point-event associations
- `GET /metrics` - Summary statistics and impact metrics

## Methodology

### Change Point Detection

We use Bayesian inference with PyMC to detect structural breaks in the oil price time series. The model:

- Defines a discrete uniform prior for the change point location (τ)
- Models pre- and post-change point parameters (μ₁, μ₂, σ)
- Uses MCMC sampling to estimate posterior distributions
- Identifies change points with high posterior probability

### Event Association

Change points are associated with events using temporal windows (±30 days). We emphasize correlation, not causation, recognizing that multiple factors influence oil prices simultaneously.

## Deliverables

- ✅ Task 1: Foundation document and event dataset
- ✅ Task 2: Bayesian change point analysis with quantified impacts
- ✅ Task 3: Interactive dashboard (Flask + React)

## References

See `reports/task_1_foundation.md` for detailed references and theoretical framework.

## Authors

10 Academy - Week 11 Challenge
AI Mastery Program

## License

This project is for educational purposes as part of the 10 Academy AI Mastery program.

