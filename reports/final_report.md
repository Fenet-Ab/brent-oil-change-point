# Final Project Report: Brent Oil Price Change Point Analysis (1987–2022)
**Author**: (Your Name)  
**Date**: February 11, 2026  
**Project**: Brent oil price regime shift / change-point analysis + small interactive dashboard

## 1. Executive Summary
This project analyzes daily Brent crude oil prices (1987–2022) to identify statistically meaningful regime shifts and connect them to major geopolitical and macroeconomic events. The core statistical model is a **Bayesian single switch-point model** (implemented in `PyMC`) applied to **log-returns**, supported by EDA and stationarity testing. For interpretation, the analysis overlays a curated list of historical events and highlights key dates commonly associated with major market transitions (e.g., 2008 crisis dynamics, 2014 OPEC regime change, 2020 COVID-era disruption, 2022 Russia–Ukraine shock).

In addition to the notebooks, a lightweight **Flask + React** dashboard plots the price series and displays a highlighted change-point date.

## 2. Problem Statement and Objectives
Oil prices are volatile and can shift abruptly due to shocks (wars, policy changes, demand collapses). The goals of this project were to:

- **Characterize** Brent price dynamics using exploratory analysis.
- **Verify stationarity behavior** (non-stationary levels vs. stationary returns).
- **Estimate a Bayesian change point** on returns to detect a structural break in the data-generating process.
- **Map statistically/analytically important dates** to a curated event timeline for interpretation.
- **Communicate results** via a simple interactive dashboard.

## 3. Data
- **Primary series**: `data/raw/brent_oil_prices.csv` (daily `Date`, `Price`)
- **Event timeline**: `data/processed/key_events.csv` (15 curated historical events with dates and descriptions)

## 4. Project Structure (submission inventory)
The following files are present in the repository (excluding `.git/` and `node_modules/`):

```text
./.gitignore
./dashboard/backend/app.py
./dashboard/frontend/package.json
./dashboard/frontend/package-lock.json
./dashboard/frontend/src/App.jsx
./data/processed/key_events.csv
./data/raw/brent_oil_prices.csv
./notebooks/01_eda.ipynb
./notebooks/02_stationarity_analysis.ipynb
./notebooks/03_bayesian_change_point.ipynb
./notebooks/04_event_association.ipynb
./reports/final_report.md
./reports/task_1_foundation.md
```

## 5. Methodology
### 5.1 Exploratory Data Analysis (EDA)
In `notebooks/01_eda.ipynb`, the series is loaded, indexed by date, and plotted to visualize:

- Long-run trend and large swings (boom/bust cycles)
- Clustering of volatility during crisis periods
- Plausible “regime” behavior (different eras with different typical levels/variance)

### 5.2 Stationarity Testing
In `notebooks/02_stationarity_analysis.ipynb`:

- Prices are transformed into **log-returns**: \( r_t = \log(P_t) - \log(P_{t-1}) \)
- An **Augmented Dickey-Fuller (ADF)** test is run on returns to validate the modeling choice (returns are typically closer to stationary than price levels).

### 5.3 Bayesian Change Point Model (single switch-point)
In `notebooks/03_bayesian_change_point.ipynb`, a Bayesian “switch-point” model is fit to returns:

- The change point \( \tau \) is modeled as an **unknown discrete time index**.
- Two return means \( \mu_1 \) and \( \mu_2 \) apply before/after \( \tau \).
- A shared noise scale \( \sigma \) is assumed.
- Inference is performed using **MCMC sampling** in `PyMC`.

This produces a posterior distribution over \( \tau \), allowing estimation of the most likely break location and uncertainty around it.

### 5.4 Event Association (interpretation overlay)
In `notebooks/04_event_association.ipynb`, event association is performed by:

- Creating a small table of “key” change-point dates (e.g., 2008-09-15, 2014-11-27, 2020-03-15, 2022-02-24).
- Matching events within a configurable window (e.g., ±30 days) to provide contextual interpretation.

**Important note**: this step is an interpretation overlay. Only the `PyMC` notebook is a statistical estimation of a change point; the multi-date list used for event association is a curated set of historically significant dates used to contextualize regimes.

## 6. Results (what was produced)
### 6.1 Stationarity result (qualitative)
Consistent with standard financial time series behavior:

- **Price levels** behave like a non-stationary process (trend + shocks).
- **Log-returns** are more stable and suitable for change-point modeling.

### 6.2 Bayesian change point (single switch-point)
The Bayesian model provides:

- An estimated break index \( \tau \) (posterior mean/median)
- A corresponding **calendar date** mapped from the returns index
- An estimated shift in mean return (\( \mu_2 - \mu_1 \)) as an “impact” summary

Because the switch-point model is single-break, it captures one dominant regime change rather than multiple breaks across the full history.

### 6.3 Historical context (key regime-shift dates)
The interpretation notebook highlights several widely recognized market transition dates and checks for nearby events in the curated timeline, including:

- **2008**: global financial crisis dynamics
- **2014**: OPEC production/strategy shift and shale-era supply expansion
- **2020**: COVID-era demand shock + volatility spike
- **2022**: Russia–Ukraine war and energy security risk premium

## 7. Dashboard (communication artifact)
The dashboard is a minimal end-to-end demonstrator:

- **Backend** (`dashboard/backend/app.py`): Flask API serving:
  - `/prices`: returns the raw CSV as JSON records
  - `/changepoints`: currently returns a single example change point (`2020-03-15`)
- **Frontend** (`dashboard/frontend/src/...`): React + Recharts line chart that:
  - plots `Price` over `Date`
  - draws a vertical reference line at the change-point date

## 8. Assumptions and Limitations
- **Single-break model**: the Bayesian model implemented is a *single* switch-point; markets often have multiple breaks, so a multi-change-point model would better reflect reality.
- **Correlation vs. causation**: event alignment is temporal and interpretive; it does not prove causal impact.
- **Distributional assumptions**: a Gaussian likelihood for returns is a simplification (returns can be heavy-tailed and heteroskedastic).
- **Operationalization gap**: the dashboard currently displays a hard-coded change-point date; integrating notebook outputs into the API would strengthen reproducibility.

## 9. Conclusion and Future Work
This project demonstrates a complete workflow from raw data to statistical modeling to stakeholder communication. The Bayesian switch-point model provides a principled way to estimate a structural break in return behavior, while the event overlay offers historical interpretation.

Recommended extensions:

- Implement **multiple** change points (Bayesian MCP or frequentist methods) and compare results.
- Model **time-varying volatility** (e.g., GARCH or stochastic volatility) alongside mean shifts.
- Connect notebook outputs to the dashboard by exporting detected change points into `data/processed/` and serving them via the API.

## 10. How to Run (reproducibility notes)
### 10.1 Run the backend
From `dashboard/backend/`:

```bash
python app.py
```

### 10.2 Run the frontend
From `dashboard/frontend/`:

```bash
npm install
npm start
```

## 11. Export to PDF
If you have `pandoc` installed, you can export this report to PDF from the repo root:

```bash
pandoc reports/final_report.md -o reports/final_report.pdf
```
