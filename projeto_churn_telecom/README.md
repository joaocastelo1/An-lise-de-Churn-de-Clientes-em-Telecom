# Telecom Customer Churn Analysis

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat&logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-1.8K+)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Complete customer churn analysis project for a telecommunications company. Demonstrates end-to-end data analytics skills including data cleaning, exploratory data analysis (EDA), insight generation, visualization, and interactive dashboard development.

## Key Performance Indicators

| Metric | Value |
|--------|-------|
| Churn Rate | 35.94% |
| Total Customers | 64 |
| Churned Customers | 23 |
| Average Monthly Ticket | $64.49 |
| Average Customer Tenure | 28.2 months |

## Key Insights

### Contract Type (Critical Risk Factor)
- **Month-to-Month**: 65.7% churn rate (highest risk)
- **One Year**: 0% churn rate
- **Two Year**: 0% churn rate

**Recommendation**: Offer 15-20% discount for annual contracts

### Internet Service
- **Fiber Optic**: 40% churn rate
- **DSL**: 26.7% churn rate
- **No Internet**: 75% churn rate (technical issues likely)

**Recommendation**: Prioritize fiber infrastructure maintenance

### Payment Method (Highest Risk)
- **Electronic Check**: 73.7% churn rate (critical)
- **Mailed Check**: 45.5% churn rate
- **Credit Card**: 20% churn rate
- **Bank Transfer**: 0% churn rate (most stable)

**Recommendation**: Incentivize automatic payment methods

## Business Impact

| Metric | Value |
|--------|-------|
| Current Churn Rate | 35.94% |
| Lost Customers | 23 |
| Monthly Revenue Lost | $8,064.65 |
| Annual Revenue Lost | $96,775.80 |
| **Potential Savings (20% reduction)** | **$19,355.16/year** |

## Technologies & Skills

### Data Analysis
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations
- **Data Cleaning** - Missing value handling, feature engineering
- **EDA** - Statistical analysis and pattern detection

### Visualization
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical graphics
- **Correlation Matrix** - Feature relationships

### Dashboard & API
- **Streamlit** - Interactive dashboard
- **Flask** - REST API
- **Local Deployment** - Development server

## Project Structure

```
projeto_churn_telecom/
├── data/
│   ├── raw/telco_churn.csv          # Raw data
│   ├── processed/                   # Cleaned data
│   ├── telecom_limpo.csv            # Primary dataset
│   └── telecom_clientes.csv           # Customer data
├── src/
│   ├── analysis/eda_analysis.py      # EDA module
│   ├── data/data_cleaning.py          # Data cleaning module
│   ├── insights.py                  # Insight generation
│   ├── visualizacoes.py             # Visualizations
│   └── limpeza_eda.py              # Combined EDA
├── reports/
│   ├── figures/                     # Generated charts
│   │   ├── churn_distribution.png
│   │   ├── churn_by_contract.png
│   │   ├── churn_by_internet.png
│   │   ├── churn_by_payment.png
│   │   ├── correlation_matrix.png
│   │   └── tenure_distribution.png
│   └── insights.csv               # Exported insights
��── notebooks/
│   └── analysis.ipynb              # Jupyter analysis
├── dashboard_streamlit.py        # Interactive dashboard
├── api_flask.py                 # REST API
├── main.py                     # Main pipeline
└── requirements.txt            # Dependencies
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run full analysis pipeline
python main.py

# Run interactive dashboard
streamlit run dashboard_streamlit.py

# Run API
python api_flask.py
```

## Dashboard Features

- **Overview Tab**: KPI metrics and churn distribution pie chart
- **Plans Tab**: Churn analysis by contract type and plan
- **Satisfaction Tab**: Churn correlation with satisfaction score and complaints
- **Regional Tab**: Geographic churn analysis
- **Filters**: Interactive region and plan filters

## Future Improvements

- [ ] Machine Learning models (Random Forest, XGBoost)
- [ ] Customer churn prediction scoring
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Docker containerization
- [ ] CI/CD pipeline integration

## Contact

<div>
  <a href="mailto:jcrocap2@gmail.com">
    <img src="https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=gmail&logoColor=white" alt="Gmail"/>
  </a>
  <a href="https://linkedin.com/in/joaocastelo1">
    <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
</div>

---

*Project developed to demonstrate data analytics and Python competencies for professional opportunities.*