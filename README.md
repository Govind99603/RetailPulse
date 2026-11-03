# RetailPulse — Retail Intelligence Prototype

Customer analytics, retail demand exploration, and assumption-based inventory suggestions using Online Retail II.

## Included
- Streamlit dashboard: Executive Overview, Sales Trends, Customer Analytics, Demand Forecast, Inventory.
- RFM segmentation visualizations and supplied churn proxy feature table.
- Transparent trailing-seven-day demand baseline.
- Inventory reorder recommendation explorer.
- End-to-end notebook, dependency list, Docker setup, and data contract test.

## Run locally
Python 3.11 recommended. Ensure all supplied CSVs are placed in `data/processed/` (the compact derived artifacts are included in this package).
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501.

## Docker
```bash
docker build -t retailpulse .
docker run --rm -p 8501:8501 retailpulse
```

## Important limitations
- `ChurnProxy` is heuristic, not ground-truth churn. Use an explicitly defined future observation window and time-based validation before claiming predictive performance.
- Demand page is a simple moving-average baseline, not Prophet, LSTM, or hybrid forecasting. Add temporal backtesting and model comparisons before operational use.
- Reorder quantities are assumption-driven. Validate lead times, service levels, current inventory, and vendor constraints before purchase decisions.
- CSV values reflect static artifacts, not live operational data.
- Review cancellations, returns/negative quantities, missing customer IDs, duplicates and data-cleaning choices in the notebook.

## Structure
`app.py`, `data/processed/`, `RetailPulse_End_to_End.ipynb`, `requirements.txt`, `Dockerfile`, `tests/`.

## Test
```bash
pytest -q
```


## Creator

**RetailPulse** was designed and built by **Govind Suthar**.
