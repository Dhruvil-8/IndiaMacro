# IndiaMacro: Research Architecture
---

## 1. Executive Summary
This project implements an end-to-end **Macro Research System** designed for economic analysis this framework focuses on **Leading Indicators**, **Structural Liquidity**, and **Financial Conditions**.

The system ingests raw economic data, transforms it into structured signal-processing modules, and visualizes it in an interactive dashboard (`dashboard.py`).

---

## 2. Data Sources

### A. Reserve Bank of India (RBI)
*   **Source**: [RBI Database on Indian Economy (DBIE)](https://data.rbi.org.in/DBIE/#/dbie/home)
*   **Usage**: Primary source for Balance of Payments (BoP), Money Supply (M3/M0), Credit Growth, and Banking Statistics.

### B. Index Data (Nifty 50)
*   **Source**: Kaggle (Nifty 50 Minute Data)
*   **Code for Ingestion**:
    ```python
    import kagglehub
    # Download latest version
    path = kagglehub.dataset_download("debashis74017/nifty-50-minute-data")
    print("Path to dataset files:", path)
    ```

---

## 3. Core Architecture
The system is built on a 7-Layer Pipeline:

1.  **Layer 0 (Data Foundation)**: Ingestion of 100+ RBI series and Global tickers, handling point-in-time accuracy and publication lags.
2.  **Layer 1 (Frequency Alignment)**: A "Decision Matrix" that maps disparate data (Daily Market, Monthly Trade, Quarterly GDP) to a unified timeframe.
3.  **Layer 2-4 (Signal Generation)**: Transformation of raw data into Z-Scores, YoY Deltas, and Regime Classifications.
4.  **Layer 5-6 (Attribution & Dashboard)**: Factor exposure analysis and visualization.

---

## 4. Analysis Modules

We have enhanced the standard economic model with three specialized research modules:

### A. The "Flows & Positioning" Module
*   **Methodology**: Tracks Net Portfolio Investment (BoP) and FDI via a **Rolling 3-Year Liquidity Z-Score**.
*   **Insight**: Helps distinguish between flow-driven market regimes and fundamental trends.

### B. The "Nowcasting" Module 
*   **Methodology**: A **Financial Conditions Index (FCI)** aggregating Cost of Capital (10Y Yields), Banking Stress (Call Rates), and External Vulnerability (FX Reserves).
*   **Insight**: Acts as a weekly gauge for overall financial system stress.

### C. The "Monetary & Banking" Module
*   **Methodology**:
    *   **Credit Impulse**: The *change in the change* of credit flow.
    *   **Fiscal Dominance**: Monitoring Government vs. Private sector credit usage.
    *   **Money Multiplier**: Assessing the banking transmission mechanism.

---

## 5. Usage

1.  **Install Dependencies**:
    ```bash
    pip install pandas numpy streamlit plotly yfinance kagglehub
    ```

2.  **Run the Pipeline**:
    Execute the notebooks in order:
    - `00D_flow_data_loader.ipynb`
    - `00E_nowcast_fci.ipynb`
    - `00F_monetary_banking.ipynb`
    - `01A_frequency_decision_matrix.ipynb` (Alignment)

3.  **Launch Dashboard**:
    ```bash
    streamlit run notebooks/dashboard.py
    ```

---

## 6. Technology Stack
- **Core**: Python 3.10+
- **Data**: Pandas, Parquet (for speed/compression)
- **Vis**: Plotly Interactive, Streamlit
- **Quant**: NumPy, SciPy (Z-Scores, Rolling Statistics)
---

## 7. Development Story
This project represents a hybrid AI-Human collaboration:
*   **Phase 1 (Planning)**: Conceptualization and architectural design were brainstormed using **ChatGPT**.
*   **Phase 2 (Execution)**: The entire codebase, logic implementation, and debugging were autonomously executed by **Antigravity** (Google DeepMind's Advanced Agentic Coding Assistant)

> [!IMPORTANT]
> **Educational Purpose Only**: This project is for educational and research purposes. It does not constitute financial advice. The models and signals generated are experimental.
