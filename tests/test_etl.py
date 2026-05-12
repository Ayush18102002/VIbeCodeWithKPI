"""
test_etl.py — Two pytest tests for the ETL pipeline.

Test 1: ``transform`` removes dirty rows (blanks, negatives, dupes).
Test 2: ``compute_kpis`` returns the correct KPI values.
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so `from src.etl import ...`
# works when running this file directly: python tests/test_etl.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import pytest

from src.etl import compute_kpis, transform


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def raw_orders() -> pd.DataFrame:
    """A small, hand-crafted DataFrame with known dirty rows."""
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 5],
            "product": ["Widget A", "", "Gadget X", "Widget A", "Gizmo Z", "Gizmo Z"],
            "quantity": [2, 3, -1, 5, 4, 4],
            "unit_price": [9.99, 19.99, 49.99, 9.99, 14.99, 14.99],
        }
    )


# ---------------------------------------------------------------------------
# Test 1 — transform removes dirty rows
# ---------------------------------------------------------------------------

def test_transform_removes_dirty_rows(raw_orders: pd.DataFrame) -> None:
    """After cleaning, only valid, unique rows should remain.

    Dirty rows in the fixture:
    - order_id 2: blank product  → removed
    - order_id 3: negative qty   → removed
    - order_id 5 (dup): duplicate → removed

    Expected survivors: order_id 1, 4, 5 (first occurrence) → 3 rows.
    """
    cleaned = transform(raw_orders)

    assert len(cleaned) == 3, f"Expected 3 clean rows, got {len(cleaned)}"
    assert set(cleaned["order_id"].tolist()) == {1, 4, 5}
    assert (cleaned["quantity"] > 0).all(), "All quantities should be positive"
    assert cleaned["product"].str.strip().ne("").all(), "No blank products"


# ---------------------------------------------------------------------------
# Test 2 — compute_kpis returns correct values
# ---------------------------------------------------------------------------

def test_compute_kpis_values() -> None:
    """Given a known clean DataFrame, verify the three KPI values."""
    clean = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Alpha", "Beta", "Alpha"],
            "quantity": [10, 5, 3],
            "unit_price": [2.00, 10.00, 2.00],
            "revenue": [20.00, 50.00, 6.00],
        }
    )

    kpis = compute_kpis(clean)

    assert kpis["total_orders"] == 3
    assert kpis["total_revenue"] == 76.00
    assert kpis["top_product"] == "Beta", (
        f"Expected 'Beta' (revenue $50), got '{kpis['top_product']}'"
    )
