<div align="center">

# 🛍️ RetailPulse
### AI-Powered Customer Analytics & Demand Forecasting

**Turning retail transaction data into practical business insights.**

[![Live App](https://img.shields.io/badge/🚀_Live_Dashboard-Open_Streamlit-FF4B4B?style=for-the-badge)](https://govind99603-retailpulse-app-yqxrxq.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

[🌐 **Try the live dashboard**](https://govind99603-retailpulse-app-yqxrxq.streamlit.app/) · [📓 Notebook](RetailPulse_End_to_End.ipynb)

</div>

---

## 👋 About the project

RetailPulse started with a simple question: *what can a retailer learn from the transactions they already have?*

This project takes the Online Retail II dataset and works through the data science process—from checking and cleaning the raw data to exploring sales, understanding customers, looking at demand patterns, and turning the results into an interactive dashboard.

I built RetailPulse as an end-to-end project, not just a notebook with charts. The dashboard brings different areas of retail analysis together so a user can explore the business from multiple angles.

> **Want to explore it yourself?** The app is deployed and can be opened here:  
> **[https://govind99603-retailpulse-app-yqxrxq.streamlit.app/](https://govind99603-retailpulse-app-yqxrxq.streamlit.app/)**

## ✨ What you can explore

| Dashboard area | What it covers |
|---|---|
| 🧭 Command Center | A high-level view of retail performance and key metrics |
| 💷 Revenue Studio | Revenue trends and sales performance |
| 📦 Product Intelligence | Product-level performance and insights |
| 👥 Customer Segments | Customer grouping and RFM-based analysis |
| 🌍 Geo & Market View | Market and country-level views where data is available |
| 📅 Seasonality Lab | Time-based patterns in sales |
| 🧺 Basket Behavior | Transaction and basket-related analysis |
| 💎 Revenue Quality | Revenue composition and quality checks |
| 🏬 Inventory Control | Demand summaries and reorder recommendation prototype |
| 🚚 Order Operations | Order and transaction operations views |
| 🔮 Forecast Lab | Demand forecasting exploration |
| 🧪 Analytics Workbench | Additional analytical views and tools |

## 📊 A few visuals from the notebook

The charts below are exported from the project notebook outputs. They provide a quick look at the analysis behind RetailPulse.

### Revenue over time
![Monthly revenue trend](README_Assets/monthly-revenue-trend.png)

### Countries contributing the most revenue
![Top countries by revenue](README_Assets/top-countries-revenue.png)

### Customer segments
![Customer RFM segments](README_Assets/customer-rfm-segments.png)

### Quantity and unit-price distributions
![Quantity and unit price distributions](README_Assets/quantity-price-distribution.png)

### Daily demand baseline
![Daily demand baseline forecast](README_Assets/daily-demand-baseline-forecast.png)

### Prophet forecast
![Prophet forecast](README_Assets/prophet-forecast.png)

### Product demand view
![Product average daily demand](README_Assets/product-average-daily-demand.png)

### Churn-risk proxy evaluation
![Churn-risk proxy evaluation](README_Assets/churn-risk-proxy-evaluation.png)

## 🧰 Tech stack

- **Python** — project programming language
- **Pandas & NumPy** — data handling and numerical analysis
- **Matplotlib & Seaborn** — charts and exploratory analysis
- **Scikit-learn** — preprocessing and machine learning workflows
- **Prophet** — optional time-series forecasting
- **TensorFlow / Keras** — optional LSTM forecasting experiment
- **MLflow** — optional experiment tracking
- **Streamlit** — interactive dashboard
- **Jupyter Notebook** — analysis and experimentation

## 🔄 Project workflow — step by step

Here is how the project is organized from raw data to dashboard:

1. **Load the data**  
   Read both sheets of the Online Retail II workbook and combine the records.

2. **Check data quality**  
   Inspect data types, missing values, duplicate rows, date coverage, and unusual values.

3. **Clean the transactions**  
   Remove exact duplicates, parse dates, convert numeric columns, and keep records that meet the notebook’s analytical criteria.

4. **Explore the data (EDA)**  
   Look at sales distributions, monthly revenue, country-level revenue, and product patterns.

5. **Create useful features**  
   Prepare transaction and customer-level features for downstream analysis.

6. **Analyze customers**  
   Use Recency, Frequency, and Monetary (RFM) measures to build customer segments.

7. **Explore churn risk**  
   Test a historical inactivity proxy. This is a dataset-derived label, not a confirmed business churn label.

8. **Explore demand forecasting**  
   Establish a chronological daily-demand baseline, with optional Prophet and LSTM experiments.

9. **Build inventory recommendations**  
   Estimate product demand and calculate prototype reorder recommendations using configurable assumptions.

10. **Export analytical artifacts**  
    Save processed tables that the dashboard can use.

11. **Explore the results in Streamlit**  
    Navigate the dashboard pages and interact with the analytical views.

## 🗂️ Repository structure

```text
RetailPulse/
├── app.py
├── pages/
│   ├── 01_Command_Center.py
│   ├── 02_Revenue_Studio.py
│   ├── 03_Product_Intelligence.py
│   └── ... (other dashboard pages)
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx
│   └── processed/
│       ├── cleaned_sales.csv
│       ├── customer_rfm_segments.csv
│       ├── churn_proxy_features.csv
│       ├── daily_total_demand.csv
│       ├── monthly_sales_summary.csv
│       └── inventory_reorder_recommendations.csv
├── notebooks/
│   └── RetailPulse_End_to_End.ipynb
├── README_Assets/
│   └── (notebook chart images used in this README)
├── requirements.txt
└── README.md
```

*Folder and filename details may differ slightly between local versions of the project.*

## 🚀 Run it locally

Want to run RetailPulse on your own machine? Follow these steps.

### 1. Clone the repository

```bash
git clone https://github.com/Govind99603/RetailPulse.git
cd RetailPulse
```

### 2. Create a virtual environment

**Windows (PowerShell / Command Prompt):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Make sure the data files are available

The app expects the project’s processed data files in the configured data directory. If you are running the full notebook workflow, place the Online Retail II workbook in the expected raw-data location and update the notebook’s `DATA_PATH` if needed.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will print a local URL in your terminal—open it in your browser.

## 🧠 Analysis and modeling notes

A few details worth keeping in mind:

- **RFM segmentation** is used to summarize customer purchasing behavior.
- **Churn risk** is explored using a 90-day inactivity proxy. It should not be interpreted as a verified churn outcome.
- **Forecasting** begins with a simple chronological baseline. The notebook notes that a production-grade forecast should use rolling-origin backtesting and more granular product/store data.
- **Inventory recommendations** are a prototype based on estimated demand and user-defined assumptions. They should be reviewed before being used for real purchasing decisions.
- Some notebook components—such as Prophet, TensorFlow, and MLflow—are optional dependencies.

## 🎯 What I learned

Building RetailPulse gave me hands-on practice connecting the different stages of a data science project. I worked on data cleaning, exploratory analysis, feature engineering, customer segmentation, forecasting experiments, and presenting results through a dashboard.

The biggest takeaway for me was that analysis becomes more useful when people can actually explore the results instead of only reading a notebook.

## 🛣️ Future improvements

- Add stronger forecasting evaluation with rolling-origin backtesting
- Validate inventory recommendations against edge cases and business rules
- Add deeper product- and customer-level drilldowns
- Improve automated data-quality checks
- Expand dashboard testing across pages and user interactions

## 🙋‍♂️ Author

**Govind Suthar**

Data Science & Analytics | Python | Machine Learning | Data Visualization

- GitHub: [@Govind99603](https://github.com/Govind99603)
- Project repository: [RetailPulse](https://github.com/Govind99603/RetailPulse)
- Live dashboard: [Open RetailPulse](https://govind99603-retailpulse-app-yqxrxq.streamlit.app/)

---

<div align="center">

**Thanks for checking out RetailPulse!** ⭐

If you find the project interesting, feel free to explore the live dashboard or take a look at the notebook.

</div>
