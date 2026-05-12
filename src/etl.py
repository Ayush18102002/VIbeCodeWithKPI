"""
etl.py — Extract, Transform, Load pipeline for the orders dataset.

Workflow
--------
1. **Extract**  — Read the raw CSV from ``data/orders.csv``.
2. **Transform** — Clean the data (drop blanks, remove negative quantities,
   deduplicate, compute revenue).
3. **Load / Report** — Print three KPIs to stdout.
"""

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "orders.csv"

# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------

def extract(path: Path = DATA_FILE) -> pd.DataFrame:
    """Read the raw orders CSV into a DataFrame."""
    df = pd.read_csv(path)
    print(f"[EXTRACT] Loaded {len(df)} rows from {path.name}")
    return df

# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw data and add a revenue column.

    Steps
    -----
    - Drop rows with missing or empty product names.
    - Drop rows where quantity ≤ 0.
    - Remove duplicate rows (based on order_id).
    - Add a ``revenue`` column = quantity × unit_price.
    """
    initial = len(df)

    # Drop missing / blank product names
    df = df[df["product"].astype(str).str.strip().ne("")]

    # Drop non-positive quantities
    df = df[df["quantity"] > 0]

    # Deduplicate on order_id
    df = df.drop_duplicates(subset=["order_id"])

    # Compute revenue
    df = df.copy()
    df["revenue"] = df["quantity"] * df["unit_price"]

    removed = initial - len(df)
    print(f"[TRANSFORM] Kept {len(df)} rows, removed {removed} dirty rows")
    return df

# ---------------------------------------------------------------------------
# Load — compute & print KPIs
# ---------------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> dict:
    """Return the three KPIs as a dictionary."""
    total_orders = len(df)
    total_revenue = round(df["revenue"].sum(), 2)

    top_product = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "top_product": top_product,
    }


def load(kpis: dict) -> None:
    """Pretty-print the KPIs to stdout."""
    print("\n" + "=" * 44)
    print("   KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 44)
    print(f"  1. Total Orders  : {kpis['total_orders']}")
    print(f"  2. Total Revenue : ${kpis['total_revenue']:,.2f}")
    print(f"  3. Top Product   : {kpis['top_product']}")
    print("=" * 44 + "\n")

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(path: Path = DATA_FILE) -> dict:
    """Execute the full ETL pipeline and return the KPIs dict."""
    raw = extract(path)
    clean = transform(raw)
    kpis = compute_kpis(clean)
    load(kpis)
    return kpis


if __name__ == "__main__":
    run_pipeline()
