# Marketing Spend Optimizer & Sales Forecaster

A data science project that uses regression-based modeling to analyze marketing spend across channels, forecast revenue, and optimize budget allocation for maximum ROI.

## 🔗 Live Demos
-  **Optimization App** → https://marketing-spend-optimizer-sales-forecaster.streamlit.app/
-  **Analytics Dashboard** → https://public.tableau.com/app/profile/divyam.goyal3253/viz/MarketingSpendOptimizer-AnalyticsDashboard/MarketingAnalyticsDashboard?publish=yes

##  What It Does
- Generates a marketing dataset with 4 spend channels and revenue
- Stores data in SQLite with a versioned migration system
- Trains a Linear Regression model (R² = 0.985)
- Simulates revenue under different budget scenarios
- Uses SciPy optimization to find the ideal budget allocation
- Visualizes insights via an interactive Streamlit dashboard and Tableau analytics dashboard

##  Tech Stack
| Layer | Tools |
|---|---|
| Language | Python |
| Data | Pandas, NumPy, SQLite |
| ML | Scikit-learn, SciPy |
| Visualization | Matplotlib, Seaborn, Tableau |
| Dashboard | Streamlit |
| Database | SQLite + custom migration system |

##  Project Structure
```
marketing-spend-optimizer/
│
├── src/                  # Modular Python package
│   ├── data_generator.py
│   ├── database.py
│   ├── visualizer.py
│   ├── model.py
│   ├── simulator.py
│   └── optimizer.py
│
├── migrations/           # Versioned DB schema migrations
│   ├── 001_initial_schema.sql
│   └── migrate.py
│
├── app/                  # Streamlit web app
│   └── dashboard.py
│
└── main.py               # CLI pipeline
```

## 🚀 Run Locally
```bash
pip install -r requirements.txt
python main.py              # run full pipeline
streamlit run app/dashboard.py  # launch dashboard
```

