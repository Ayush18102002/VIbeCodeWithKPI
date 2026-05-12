"""
generate_data.py — Create a small synthetic orders CSV for the ETL pipeline.

The dataset intentionally includes some messy rows (missing values, duplicates,
negative quantities) so the ETL cleaning step has something meaningful to do.
"""

import csv
import os
import random

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "orders.csv")
NUM_ROWS = 50
SEED = 42

PRODUCTS = [
    ("Widget A", 9.99),
    ("Widget B", 19.99),
    ("Gadget X", 49.99),
    ("Gadget Y", 29.99),
    ("Gizmo Z", 14.99),
]

# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_orders(num_rows: int = NUM_ROWS, seed: int = SEED) -> list[dict]:
    """Return a list of synthetic order dicts, including some dirty rows."""
    random.seed(seed)
    orders: list[dict] = []

    for i in range(1, num_rows + 1):
        product, price = random.choice(PRODUCTS)
        quantity = random.randint(1, 20)

        row = {
            "order_id": i,
            "product": product,
            "quantity": quantity,
            "unit_price": round(price, 2),
        }

        # ---- Inject dirty data (~10 % of rows) ----
        roll = random.random()
        if roll < 0.04:
            # Missing product name
            row["product"] = ""
        elif roll < 0.08:
            # Negative quantity (invalid)
            row["quantity"] = -abs(row["quantity"])
        elif roll < 0.10:
            # Duplicate of the previous row (if any)
            if orders:
                row = dict(orders[-1])

        orders.append(row)

    return orders


def write_csv(orders: list[dict], path: str = OUTPUT_FILE) -> None:
    """Write the list of order dicts to a CSV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    fieldnames = ["order_id", "product", "quantity", "unit_price"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)

    print(f"[OK] Generated {len(orders)} rows -> {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    data = generate_orders()
    write_csv(data)
