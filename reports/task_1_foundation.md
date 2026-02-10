# Task 1: Laying the Foundation for Analysis

## 1. Data Analysis Workflow
This workflow outlines the systematic process for analyzing Brent oil price fluctuations and identifying structural breaks over the period of 1987 to 2022.

1.  **Data Acquisition and Preprocessing**:
    *   Load raw Brent oil price data.
    *   Perform data cleaning: handle missing values, normalize date formats, and ensure temporal consistency.
2.  **Exploratory Data Analysis (EDA)**:
    *   Visualize historical price trends.
    *   Identify seasonal patterns and cycle components.
    *   Calculate moving averages and rolling standard deviations to visualize volatility.
3.  **Time Series Property Analysis**:
    *   **Trend Analysis**: Identify long-term directions.
    *   **Stationarity Testing**: Conduct Augmented Dickey-Fuller (ADF) and Kwiatkowski-Phillips-Schmidt-Shin (KPSS) tests.
    *   **Volatility Clustering**: Analyze the "GARCH" like behavior of returns.
4.  **Change Point Modeling**:
    *   Apply statistical models (e.g., PELT, Binary Segmentation) to detect structural breaks in mean and variance.
    *   Optimize model hyperparameters (e.g., penalty values) to avoid over/under-segmentation.
5.  **Geopolitical Event Mapping**:
    *   Overlay detected change points with the compiled "Key Events" dataset.
    *   Analyze the lead/lag relationship between events and price reactions.
6.  **Synthesis and Insight Generation**:
    *   Evaluate the magnitude of impact for different event categories (geopolitical vs. economic).
    *   Develop conclusions regarding market resilience and reactivity.
7.  **Reporting and Visualization**:
    *   Compile findings into a comprehensive report.
    *   Develop an interactive dashboard for stakeholder exploration.

## 2. Assumptions and Limitations

### Assumptions:
*   **Market Efficiency**: We assume that Brent oil prices reflect all publicly available information, including geopolitical risks, though with varying degrees of efficiency.
*   **Data Integrity**: The historical price data is assumed to be an accurate representation of the global Brent benchmark.
*   **Stationarity of Differences**: While raw prices are non-stationary, their first differences (returns) are assumed to be stationary for modeling purposes.

### Limitations:
*   **Model Sensitivity**: Change point models are sensitive to penalty parameters; minor adjustments can lead to different sets of detected points.
*   **Data Frequency**: Daily data may miss intra-day volatility peaks or be subject to "noise" that obscures long-term structural shifts.
*   **Omitted Variables**: Many factors beyond compiled events (e.g., technological breakthroughs in extraction, changes in interest rates) influence prices but may not be explicitly modeled.

### Correlation vs. Causation: The "Post Hoc" Fallacy
A critical distinction in this analysis is the difference between **statistical correlation in time** and **causal impact**.
*   **Temporal Correlation**: Identifying that a structural break (a "change point") occurred within a specific window of a geopolitical event. This is a necessary but insufficient condition for establishing impact.
*   **Causal Inference**: Proving that the event *directly necessitated* the price shift. In complex global markets, a price spike during a war may be partially caused by unrelated interest rate hikes or shipping strikes occurring simultaneously.
*   **Our Approach**: We recognize that change point models are "event-agnostic"—they find shifts based purely on data variance. By overlaying events, we hypothesize causation, but we remain cautious not to commit the *post hoc ergo propter hoc* (after this, therefore because of this) fallacy. Our findings will be presented as "consistent with" or "suggestive of" impact rather than definitive proof of singular causation.

## 3. Data Description and Exploration
The primary dataset consists of daily Brent Crude Oil prices from May 20, 1987, to 2022.

*   **Source**: Raw CSV containing `Date` and `Price` (USD per barrel).
*   **Sample Size**: ~9,000 observations.
*   **Preliminary Observations**:
    *   **Trend**: The series exhibits "stochastic trend" behavior. A long-term upward trajectory is visible, but punctuated by dramatic mean-reverting shocks.
    *   **Stationarity**: In line with financial time series theory, the price level is I(1)—integrated of order one—while the log-returns are I(0) (stationary).
    *   **Volatility**: Significant "fat-tailed" distributions in returns indicate that extreme price jumps (crises) are more common than a normal distribution would predict.

## 4. Understanding the Modeling Approach

### Time Series Properties
*   **Trend**: The Brent oil price series is characterized by significant long-term trends, including a period of relative stability in the 1990s, a sustained "super-cycle" increase from 2002 to 2008, and high-frequency fluctuations thereafter.
*   **Stationarity**: Statistical tests (ADF and KPSS) typically reveal that oil prices are **non-stationary** in levels (containing a unit root) but become **stationary** after first-differencing (log returns).
*   **Volatility Patterns**: The data exhibits "volatility clustering," where periods of high variance (market shocks) are followed by further high-variance days. This suggests that the distribution's variance is time-dependent.

### Informing Modeling Choices
*   **Difference-Based Input**: Since prices are non-stationary, the change point model will likely be applied to **log returns** or **squared returns** to identify shifts in mean return and volatility regimes, respectively.
*   **Choice of Model**: Given the presence of multiple historical shocks, "Multiple Change Point Detection" (MCPD) algorithms like **PELT (Pruned Exact Linear Time)** or **Binary Segmentation** are preferred over single-point models.
*   **Penalty Selection**: The non-stationary and volatile nature of the data necessitates a robust penalty (e.g., Modified BIC) to distinguish true structural breaks from transient noise.

### Change Point Models
**Purpose**: Change point models are designed to identify moments in a time series where the underlying probability distribution changes. In the context of oil prices, this means detecting when the market shifts from one "regime" (e.g., stable low prices) to another (e.g., high volatility or new price floor).

**How they help**: They allow us to move beyond simple event-observation and provide a statistically rigorous way to say "the market behavior fundamentally changed at this specific point in time," enabling a objective mapping between geopolitical events and market reactions.

### Expected Outputs
*   **Break Dates**: Precise dates of statistical shifts within the time series.
*   **Regime Parameters**: Average price levels, mean returns, and variance estimates for each segment defined by the breaks.
*   **Model Fit Metrics**: Evaluation of how much the segmented model improves upon a single-regime model (e.g., Log-Likelihood gains).

## 5. Key References & Theoretical Framework
The following research forms the theoretical and empirical foundation for this analysis:

1.  **Bai, J., & Perron, P. (1998)**: *Estimating and Testing Linear Models with Multiple Structural Changes*.
    *   *Contribution*: Provides the core statistical framework for detecting *multiple* unknown breakpoints in a time series simultaneously, rather than testing for a single shift.
2.  **Lee, J., & Strazicich, M. C. (2003)**: *Minimum Lagrange Multiplier Unit Root Test with Two Structural Breaks*.
    *   *Contribution*: Prevents "false non-stationarity" results. Standard tests (like ADF) often fail to reject the unit root if structural breaks are present; this paper provides a robust alternative.
3.  **Killian, L. (2009)**: *Not All Oil Price Shocks Are Alike*.
    *   *Contribution*: Establishes the taxonomy of shocks (Supply vs. Demand vs. Precautionary demand), helping us interpret *why* a detected change point occurred.
4.  **RePEc (2020)**: *Brent crude oil spot and futures prices: structural break insights*.
    *   *Contribution*: Offers recent empirical benchmarks for how COVID-19 and other modern crises affected the Brent market specifically.

## 6. Communication Strategy
To ensure effective dissemination of insights to stakeholders (e.g., policy makers, energy analysts), we have defined the following channels:

*   **Executive Summary (PDF/Deck)**: A high-level synthesis of major "regime shifts" and their historical context.
*   **Interactive Analytics Dashboard**: A tool allowing users to click on detected change points to see the associated geopolitical events and statistical parameters.
*   **Data API/Feeds**: Cleaned change point data for integration into secondary risk models.
