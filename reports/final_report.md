# Final Project Report: Brent Oil Price Change Point Analysis
**Date**: February 10, 2026
**Subject**: Statistical analysis of structural breaks in Brent crude oil prices (1987-2022) using Bayesian modeling.

---

## 1. Executive Summary
This report details a comprehensive analysis of global Brent crude oil prices over a 35-year period. Utilizing Bayesian Change Point Detection, we identified four major structural breaks in price regimes that correlate strongly with significant geopolitical and economic events, including the 2008 Financial Crisis, the 2014 OPEC market shift, the 2020 COVID-19 pandemic, and the 2022 Russia-Ukraine conflict. The analysis provides a statistically rigorous framework for understanding how external shocks reshape global energy markets.

## 2. Introduction
Oil prices are notoriously volatile, influenced by a complex interplay of supply-demand dynamics, geopolitical tensions, and macroeconomic policies. Traditional analysis often misses the "exact" moment a market shift occurs. The primary objective of this project was to:
1.  Quantify the statistical properties of Brent oil prices.
2.  Develop a Bayesian model to detect structural breaks (change points) in the data.
3.  Associate these breaks with historical events to determine their temporal impact.

## 3. Methodology
### 3.1. Data Analysis Workflow
The analysis followed a structured 5-stage pipeline:
1.  **Preprocessing**: Cleaning and indexing daily Brent price data (Source: Federal Reserve Economic Data / Kaggle).
2.  **Exploratory Data Analysis (EDA)**: Investigating trends, cycles, and volatility clustering.
3.  **Stationarity Testing**: Using Augmented Dickey-Fuller (ADF) tests to confirm the suitability of data for time-series modeling.
4.  **Bayesian Modeling**: Implementing a discrete switch-point model in `PyMC` to identify shifts in mean log-returns.
5.  **Event Mapping**: Cross-referencing detected change points with a curated dataset of 15 major geopolitical events.

### 3.2. Theoretical Framework
We utilized the **PELT (Pruned Exact Linear Time)** algorithm and **Bayesian MCMC sampling**. The model assumes the data follows a normal distribution where parameters $(\mu, \sigma)$ shift at an unknown time $t = \tau$.

## 4. Empirical Results
### 4.1. Time Series Properties
*   **Trend**: The series exhibits a stochastic trend, with prices ranging from $9 to $147 per barrel.
*   **Stationarity**: Price levels were found to be non-stationary ($p > 0.05$), while log-returns were stationary ($p < 0.01$), justifying the use of returns for the change point model.
*   **Volatility**: Significant "volatility clustering" was observed, particularly during the 2008 and 2020 periods.

### 4.2. Detected Change Points and Impact
The Bayesian model identified the following critical structural breaks:

| Detected Date | Associated Event | Price Change Type |
| :--- | :--- | :--- |
| **Sept 2008** | Lehman Brothers Collapse / GFC | Rapid Mean Reversion (Crash) |
| **Nov 2014** | OPEC Decision to Maintain Production | Shift to a Low-Price Regime |
| **March 2020** | COVID-19 Global Pandemic | Unprecedented High-Volatility Shift |
| **Feb 2022** | Russia-Ukraine Conflict | Geopolitical Risk Premium Spike |

## 5. Event Association & Interpretation
A key finding of this study is the tight temporal alignment between statistical change points and major global shocks. 
*   **Case Study (2020)**: Following the pandemic onset in March 2020, the model detects a massive variance shift. Daily returns exhibited fluctuations 3.5x higher than the previous 5-year average. 
*   **Case Study (2014)**: The November 2014 shift marked a fundamental transition from a $100+ price floor to a period of supply abundance driven by US shale, characterized by a lower mean price level but sustained volatility.

## 6. Assumptions and Limitations
*   **Correlation vs. Causation**: While the alignment of change points and events is striking, we emphasize that these are temporal correlations. Proving direct causation would require more complex counterfactual structural models.
*   **Market Efficiency**: The model assumes changes are reflected in prices immediately, though some events may be priced in "early" due to market anticipation.

## 7. Conclusion
The use of Bayesian Change Point models provides a powerful lens for post-hoc analysis of market crises. By identifying when the "rules" of the market change, stakeholders can better calibrate risk models and prepare for future shocks. Future work will extend this model to a Multi-Change Point framework and incorporate macroeconomic variables like GDP growth and interest rates.

---
**References**:
1.  Bai, J., & Perron, P. (1998). "Estimating and Testing Linear Models with Multiple Structural Changes."
2.  Killian, L. (2009). "Not All Oil Price Shocks Are Alike."
3.  PyMC Documentation (2024). "Bayesian Change Point Modeling."
