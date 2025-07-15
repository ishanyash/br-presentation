# BR Presentation

This repository contains notebooks and a Streamlit dashboard for analysing UK property investment opportunities.

## Running the Streamlit dashboard

The dashboard lives under `streamlit_app/` and can be run either locally or via Docker.

### Using Docker

   ```bash
   docker build -t br-dashboard .
   ```
2. Run the container:
   ```bash
   docker run --rm -p 8501:8501 br-dashboard
   ```
3. Open [http://localhost:8501](http://localhost:8501) in your browser.

### Local Python execution


pip install -r requirements.txt
streamlit run streamlit_app/app.py
```


## Repository structure

- `streamlit_app/` – Streamlit code and dataset
- `*.ipynb` – analysis notebooks
- `dataset*.csv` – data used during the analysis

The dataset used in the dashboard is located at `streamlit_app/data/investment_analysis_phase3.csv`.
