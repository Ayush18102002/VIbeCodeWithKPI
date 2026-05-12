# 📊 Mini ETL Pipeline — Orders KPI Dashboard

A beginner-friendly Python mini-project that demonstrates a simple **Extract → Transform → Load** (ETL) pipeline. The script ingests a synthetic CSV of e-commerce orders, cleans the data, and prints three Key Performance Indicators (KPIs).

## Project Structure

```
vibecode3/
├── data/
│   └── orders.csv          # Synthetic dataset (generated)
├── src/
│   ├── __init__.py
│   ├── generate_data.py    # Script to create the synthetic CSV
│   └── etl.py              # ETL pipeline + KPI computation
├── tests/
│   ├── __init__.py
│   └── test_etl.py         # 2 pytest tests for the ETL logic
├── .gitignore
├── requirements.txt
└── README.md               # ← You are here
```

## Quick Start

```bash
# 1. Clone the repo & enter it
git clone <your-repo-url>
cd vibecode3

# 2. Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the synthetic dataset
python src/generate_data.py

# 5. Run the ETL pipeline
python src/etl.py

# 6. Run the tests
pytest -q
```

## KPIs Produced

| # | KPI            | Description                              |
|---|----------------|------------------------------------------|
| 1 | Total Orders   | Count of valid (cleaned) order records   |
| 2 | Total Revenue  | Sum of `quantity × unit_price`           |
| 3 | Top Product    | Product with the highest total revenue   |

## Tech Stack

- **Python 3.10+**
- **pandas** — data manipulation
- **pytest** — testing

## Contributing

1. Create a feature branch: `git checkout -b feature/my-change`
2. Make your changes and add tests
3. Open a Pull Request against `main`

## License

This project is for educational purposes. Feel free to use and modify.
