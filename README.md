\# AI in Healthcare: Disease Trend Analysis and Early-Warning Dashboard



\## Project Overview



An educational healthcare analytics and machine-learning prototype developed using Python, PostgreSQL, Pandas, Scikit-learn, and Streamlit.



The application analyzes synthetic weekly malaria reporting data, visualizes disease trends, identifies unusual increases for review, and displays statistical and machine-learning forecasts.



\*\*Disclaimer:\*\* All data is synthetic. This project is for education and demonstration only. It is not a validated disease-outbreak detection or clinical decision-support system.



\## Objectives



\- Store and query structured healthcare reports.

\- Analyze weekly disease trends.

\- Identify unusual increases in reported cases.

\- Estimate future reported cases using a moving average.

\- Train and evaluate a Random Forest regression model.

\- Present results in an interactive dashboard.



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Application and analysis programming |

| PostgreSQL | Relational database |

| Pandas | Data processing and analysis |

| NumPy | Numerical operations and synthetic data generation |

| SQLAlchemy and psycopg | PostgreSQL connectivity |

| Scikit-learn | Machine-learning training and evaluation |

| Matplotlib | Exploratory visualization |

| Streamlit | Interactive web dashboard |



\## System Architecture



The current prototype uses two separate data paths.



\*\*Analytics path:\*\*



`health\_cases.csv → import\_data.py → PostgreSQL → dashboard.py → Streamlit`



\*\*Machine-learning path:\*\*



`health\_cases\_long.csv → train\_model.py → ai\_forecast\_results.csv → Streamlit`



The two paths are displayed together in the dashboard but use different synthetic data histories.



\## Project Files



\- `analyze.py` — Exploratory analysis and visualization.

\- `import\_data.py` — Imports original synthetic reports into PostgreSQL.

\- `generate\_sample.py` — Generates a longer synthetic time series.

\- `train\_model.py` — Trains and evaluates a Random Forest regression model.

\- `dashboard.py` — Interactive Streamlit application.

\- `data/health\_cases.csv` — Original synthetic reporting dataset.

\- `data/health\_cases\_long.csv` — Longer synthetic training dataset.

\- `reports/ai\_forecast\_results.csv` — Saved AI prediction and evaluation results.



\## Dashboard Features



\- Region and disease selection

\- Total reported cases

\- Latest weekly cases

\- Number of reporting facilities

\- Weekly disease trend chart

\- Four-week moving-average forecast

\- Example alerts for weekly increases greater than 30%

\- Random Forest prediction and model evaluation metrics



\## Machine-Learning Method



The Random Forest model uses the previous four weeks of case counts and seasonal features derived from the week of the year.



The model is evaluated using a chronological split, with the final 16 available weeks reserved for testing.



\### Example Results



| Metric | Value |

|---|---:|

| Random Forest MAE | 7.22 |

| Previous-week baseline MAE | 8.19 |

| Random Forest forecast | 126.8 cases |

| AI forecast week | 2025-12-29 |



These results are based entirely on synthetic data and should not be interpreted as evidence of real-world forecasting performance.



\## Run Locally



\### 1. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 2. Configure PostgreSQL



Create a local PostgreSQL database named `health\_db` and a table named `health\_cases` using the project's expected schema.



The local prototype uses PostgreSQL port `5433`. The database must be populated with the original synthetic records before starting the dashboard.



\### 3. Set the database password



In Git Bash:



```bash

read -s -p "PostgreSQL password: " PG\_PASSWORD

export PG\_PASSWORD

```



Never commit or share the password.



\### 4. Run the dashboard



```bash

python -m streamlit run dashboard.py

```



Open `http://localhost:8501`.



\## Limitations



\- The project uses synthetic data only.

\- The AI model is trained separately from the PostgreSQL reporting dataset.

\- The moving-average and Random Forest forecasts cover different dates.

\- The example 30% increase threshold is not a validated outbreak definition.

\- The application requires additional configuration for cloud deployment.

\- Real-world use would require stronger data governance, validation, security, monitoring, and expert review.



\## Future Improvements



\- Connect the machine-learning model to the same validated data source used by the dashboard.

\- Add multi-region forecasting and model comparison.

\- Improve temporal validation and uncertainty reporting.

\- Add data-quality checks and appropriate public-health alerting methods.

\- Deploy the dashboard with secure cloud-hosted data storage.



\## Project Status



Working local educational prototype. GitHub publication and cloud deployment are planned.

